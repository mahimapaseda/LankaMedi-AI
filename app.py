from flask import Flask, render_template, request, jsonify
from io import BytesIO
from dotenv import load_dotenv
import base64
import json
import os
import re
import requests
import PyPDF2

load_dotenv()

app = Flask(__name__)

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "").strip()
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").rstrip("/")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "nvidia/nemotron-3.5-bolt-e4b").strip()
OCR_SPACE_API_KEY = os.getenv("OCR_SPACE_API_KEY", "").strip()

STATUS_COLORS = {
    "Critical": "#dc3545",
    "Needs Attention": "#ffc107",
    "Good": "#28a745",
}

ANALYSIS_SYSTEM_PROMPT = """You are LankaMedi AI, a clinical decision-support assistant for educational use in Sri Lanka.
Analyze the medical report text and respond with ONLY valid JSON (no markdown fences, no extra text).

JSON schema:
{
  "status": "Critical" | "Needs Attention" | "Good",
  "critical_issues": <non-negative integer>,
  "warning_issues": <non-negative integer>,
  "positive_indicators": <non-negative integer>,
  "treatment_plan": {
    "conditions": ["..."],
    "medications": ["..."],
    "lifestyle": ["..."],
    "notes": ["..."]
  }
}

Rules:
- Infer only from evidence in the report. Do NOT invent diagnoses for normal findings (e.g. normal glucose is not diabetes).
- status Critical only for emergency / life-threatening language or clearly severe findings.
- medications must be general discussion points for a physician visit; do NOT prescribe exact drug doses as definitive treatment.
- Keep each list item concise (1-2 sentences). Use empty arrays when nothing applies.
- Prefer Sri Lanka / South Asia healthcare context when relevant.
- Always include at least one notes item reminding the user to consult a licensed clinician."""


def cloud_ocr(image_bytes):
    """Extract text from an image via OCR.space. Returns text or raises ValueError."""
    api_key = OCR_SPACE_API_KEY or "helloworld"
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    payload = {
        "base64Image": f"data:image/png;base64,{image_b64}",
        "apikey": api_key,
        "language": "eng",
        "OCREngine": "2",
    }
    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            data=payload,
            timeout=45,
        )
        response.raise_for_status()
        result = response.json()
    except requests.RequestException as exc:
        raise ValueError(f"OCR request failed: {exc}") from exc

    if result.get("IsErroredOnProcessing"):
        message = result.get("ErrorMessage") or result.get("ErrorDetails") or "OCR processing failed"
        if isinstance(message, list):
            message = "; ".join(str(m) for m in message)
        raise ValueError(str(message))

    parsed = result.get("ParsedResults") or []
    if not parsed:
        raise ValueError("OCR returned no text. Use a clearer image or paste the report as text.")

    text = (parsed[0].get("ParsedText") or "").strip()
    if not text:
        raise ValueError("OCR returned empty text. Use a clearer image or paste the report as text.")
    return text


def extract_pdf_text(file_bytes):
    pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    parts = []
    for page in pdf_reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            parts.append(page_text)
    text = "\n".join(parts).strip()
    if not text:
        raise ValueError("Could not extract text from PDF. Try another file or paste the text.")
    return text


def _extract_json_object(raw_text):
    text = (raw_text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("Model did not return valid JSON")
        return json.loads(match.group(0))


def _normalize_analysis(data):
    status = data.get("status", "Needs Attention")
    if status not in STATUS_COLORS:
        status = "Needs Attention"

    plan = data.get("treatment_plan") or {}
    for key in ("conditions", "medications", "lifestyle", "notes"):
        items = plan.get(key) or []
        if not isinstance(items, list):
            items = [str(items)]
        plan[key] = [str(item).strip() for item in items if str(item).strip()]

    if not plan["notes"]:
        plan["notes"].append(
            "Informational AI summary only — confirm all findings and treatment with a licensed clinician."
        )

    def as_int(value):
        try:
            return max(0, int(value))
        except (TypeError, ValueError):
            return 0

    return {
        "status": status,
        "color": STATUS_COLORS[status],
        "critical_issues": as_int(data.get("critical_issues")),
        "warning_issues": as_int(data.get("warning_issues")),
        "positive_indicators": as_int(data.get("positive_indicators")),
        "treatment_plan": plan,
    }


class MedicalAnalyzer:
    def analyze_report(self, text):
        if not NVIDIA_API_KEY:
            raise ValueError(
                "NVIDIA_API_KEY is not configured. Add it to your .env file."
            )

        truncated = text.strip()
        if len(truncated) > 12000:
            truncated = truncated[:12000] + "\n\n[Report truncated for analysis length limits]"

        payload = {
            "model": NVIDIA_MODEL,
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1200,
            "messages": [
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Analyze this medical report and return JSON only:\n\n"
                        f"{truncated}"
                    ),
                },
            ],
        }
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.post(
                f"{NVIDIA_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=90,
            )
        except requests.RequestException as exc:
            raise ValueError(f"NVIDIA API request failed: {exc}") from exc

        if response.status_code >= 400:
            detail = response.text[:400]
            raise ValueError(f"NVIDIA API error ({response.status_code}): {detail}")

        body = response.json()
        try:
            content = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("Unexpected NVIDIA API response format") from exc

        if not content:
            # Some NVIDIA models put text in reasoning_content
            content = body["choices"][0]["message"].get("reasoning_content")
        if not content:
            raise ValueError("NVIDIA API returned an empty response")

        parsed = _extract_json_object(content)
        return _normalize_analysis(parsed)


analyzer = MedicalAnalyzer()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if "report_file" in request.files:
            file = request.files["report_file"]
            if not file or file.filename == "":
                return jsonify({"error": "No file selected"}), 400

            filename = file.filename.lower()
            file_bytes = file.read()

            if filename.endswith(".pdf"):
                report_text = extract_pdf_text(file_bytes)
            elif filename.endswith((".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp")):
                report_text = cloud_ocr(file_bytes)
            else:
                return jsonify(
                    {"error": "Unsupported file type. Please upload PDF or image files."}
                ), 400
        else:
            data = request.get_json(silent=True) or {}
            report_text = data.get("report_text", "")

        if not str(report_text).strip():
            return jsonify({"error": "Please provide report text or upload a file"}), 400

        analysis = analyzer.analyze_report(report_text)
        return jsonify(analysis)

    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Analysis failed: {exc}"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug, port=port)
