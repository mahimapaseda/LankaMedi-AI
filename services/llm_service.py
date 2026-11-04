"""Multi-provider LLM orchestration service supporting NVIDIA NIM, Google Gemini, and OpenAI-compatible endpoints."""

import json
import logging
import re
from typing import Dict, Any, Tuple
import requests

from core.config import Config
from core.constants import STATUS_COLORS, MEDICAL_DISCLAIMER_TEXT
from core.security import PIIScrubber
from schemas.analysis_schema import (
    AnalysisResponse,
    TreatmentPlan,
)
from services.biomarker_service import BiomarkerEngine

logger = logging.getLogger(__name__)


def _build_system_prompt(language: str = "en") -> str:
    lang_instruction = "Respond in English."
    if language == "si":
        lang_instruction = "IMPORTANT: Provide all text inside 'conditions', 'medications', 'lifestyle', and 'notes' in natural, respectful, and accurate SINHALA (සිංහල). Keep medical terminology understandable for Sri Lankan patients."
    elif language == "ta":
        lang_instruction = "IMPORTANT: Provide all text inside 'conditions', 'medications', 'lifestyle', and 'notes' in natural, respectful, and accurate TAMIL (தமிழ்). Keep medical terminology understandable for Sri Lankan patients."

    return f"""You are LankaMedi AI, an advanced clinical decision-support and educational assistant specialized in Sri Lankan healthcare.
Analyze the provided medical report and respond with ONLY valid JSON (no markdown backticks, no markdown formatting, no preamble).

JSON schema:
{{
  "status": "Critical" | "Needs Attention" | "Good",
  "critical_issues": <non-negative integer>,
  "warning_issues": <non-negative integer>,
  "positive_indicators": <non-negative integer>,
  "treatment_plan": {{
    "conditions": ["concise observed findings or differential conditions"],
    "medications": ["educational medication topics/classes to discuss with a doctor, NOT definite prescriptions"],
    "lifestyle": ["dietary, activity, hydration, or habit recommendations tailored to Sri Lankan diet/context"],
    "notes": ["clinical monitoring guidance, red flags, and follow-up consultation notes"]
  }}
}}

Rules:
- {lang_instruction}
- Infer ONLY from verified evidence in the report text. Do not invent diagnoses for normal lab results.
- 'status': Use 'Critical' strictly for acute emergencies, life-threatening values, or dangerous red-flags. Use 'Needs Attention' for abnormal out-of-range values or chronic conditions requiring physician consultation. Use 'Good' when findings are predominantly normal.
- 'medications': Never prescribe exact dosages or treat as an authoritative prescription. Frame as points of discussion with a licensed physician.
- Include a reminder note in 'notes' that this analysis is an educational summary and requires review by a registered doctor/consultant.
- Keep each point clear, concise (1-2 sentences), and actionable.
"""


class LLMOrchestrator:
    """Manages requests across available LLM providers with automated cascading fallback."""

    @classmethod
    def analyze_medical_text(cls, raw_text: str, language: str = "en") -> AnalysisResponse:
        """Sanitizes PII, runs rule-based biomarker analysis, and generates clinical synthesis."""
        # 1. PII/PHI De-identification
        sanitized_text = PIIScrubber.redact_text(raw_text)

        # 2. Extract structured biomarkers & check emergency triggers via BiomarkerEngine
        biomarkers, emergency_alert = BiomarkerEngine.evaluate_text(sanitized_text)

        # 3. Truncate oversized text to respect LLM context budgets
        truncated = sanitized_text.strip()
        if len(truncated) > 12000:
            truncated = truncated[:12000] + "\n\n[Report truncated for token safety limits]"

        # 4. Attempt analysis using configured providers in priority order
        llm_data, provider_used = cls._dispatch_llm_request(truncated, language)

        # 5. Harmonize status: If BiomarkerEngine detected an emergency, elevate status to 'Critical'
        status = llm_data.get("status", "Needs Attention")
        if emergency_alert and emergency_alert.is_emergency:
            status = "Critical"
        if status not in STATUS_COLORS:
            status = "Needs Attention"

        critical_count = max(0, int(llm_data.get("critical_issues", 0)))
        warning_count = max(0, int(llm_data.get("warning_issues", 0)))
        positive_count = max(0, int(llm_data.get("positive_indicators", 0)))

        # If rule-based emergency occurred, ensure critical count reflects at least 1
        if emergency_alert and emergency_alert.is_emergency and critical_count == 0:
            critical_count = 1

        plan_raw = llm_data.get("treatment_plan") or {}
        treatment_plan = TreatmentPlan(
            conditions=[str(c).strip() for c in plan_raw.get("conditions", []) if str(c).strip()],
            medications=[str(m).strip() for m in plan_raw.get("medications", []) if str(m).strip()],
            lifestyle=[str(l).strip() for l in plan_raw.get("lifestyle", []) if str(l).strip()],
            notes=[str(n).strip() for n in plan_raw.get("notes", []) if str(n).strip()],
        )

        if not treatment_plan.notes:
            treatment_plan.notes.append(
                "Informational AI analysis only — please consult a licensed medical practitioner to confirm diagnoses."
            )

        return AnalysisResponse(
            status=status,
            color=STATUS_COLORS[status],
            critical_issues=critical_count,
            warning_issues=warning_count,
            positive_indicators=positive_count,
            treatment_plan=treatment_plan,
            biomarkers=biomarkers,
            emergency_alert=emergency_alert,
            language=language,
            provider_used=provider_used,
            disclaimer=MEDICAL_DISCLAIMER_TEXT,
        )

    @classmethod
    def _dispatch_llm_request(cls, prompt_text: str, language: str) -> Tuple[Dict[str, Any], str]:
        """Tries NVIDIA NIM, Google Gemini, and OpenAI-compatible endpoints with automated fallback."""
        system_prompt = _build_system_prompt(language)
        errors = []

        # 1. NVIDIA NIM
        if Config.NVIDIA_API_KEY:
            try:
                res = cls._call_nvidia_nim(prompt_text, system_prompt)
                return res, f"NVIDIA NIM ({Config.NVIDIA_MODEL})"
            except Exception as exc:
                logger.warning("NVIDIA NIM provider failed: %s", exc)
                errors.append(f"NVIDIA: {exc}")

        # 2. Google Gemini
        if Config.GEMINI_API_KEY:
            try:
                res = cls._call_gemini_api(prompt_text, system_prompt)
                return res, f"Google Gemini ({Config.GEMINI_MODEL})"
            except Exception as exc:
                logger.warning("Gemini provider failed: %s", exc)
                errors.append(f"Gemini: {exc}")

        # 3. OpenAI / Groq / Ollama
        if Config.OPENAI_API_KEY:
            try:
                res = cls._call_openai_compatible(prompt_text, system_prompt)
                return res, f"OpenAI/Compatible ({Config.OPENAI_MODEL})"
            except Exception as exc:
                logger.warning("OpenAI-compatible provider failed: %s", exc)
                errors.append(f"OpenAI: {exc}")

        if not errors:
            raise ValueError(
                "No AI model provider is configured. Please provide an NVIDIA_API_KEY, GEMINI_API_KEY, or OPENAI_API_KEY in your .env file."
            )

        raise ValueError("All configured AI providers failed: " + "; ".join(errors))

    @classmethod
    def _call_nvidia_nim(cls, text: str, system_prompt: str) -> Dict[str, Any]:
        """Calls NVIDIA NIM OpenAI-compatible API."""
        headers = {
            "Authorization": f"Bearer {Config.NVIDIA_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        payload = {
            "model": Config.NVIDIA_MODEL,
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1400,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Medical Report:\n\n{text}"},
            ],
        }
        resp = requests.post(
            f"{Config.NVIDIA_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=Config.LLM_TIMEOUT,
        )
        if resp.status_code >= 400:
            raise ValueError(f"Status {resp.status_code}: {resp.text[:300]}")

        body = resp.json()
        choice = body["choices"][0]["message"]
        content = choice.get("content") or choice.get("reasoning_content") or ""
        return cls._parse_json(content)

    @classmethod
    def _call_gemini_api(cls, text: str, system_prompt: str) -> Dict[str, Any]:
        """Calls Google Gemini REST API directly."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{Config.GEMINI_MODEL}:generateContent?key={Config.GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": f"{system_prompt}\n\nMedical Report to analyze:\n{text}"}
                    ],
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1400,
                "responseMimeType": "application/json",
            },
        }
        resp = requests.post(url, json=payload, timeout=Config.LLM_TIMEOUT)
        if resp.status_code >= 400:
            raise ValueError(f"Gemini API Error {resp.status_code}: {resp.text[:300]}")

        body = resp.json()
        candidate = body["candidates"][0]["content"]["parts"][0]["text"]
        return cls._parse_json(candidate)

    @classmethod
    def _call_openai_compatible(cls, text: str, system_prompt: str) -> Dict[str, Any]:
        """Calls generic OpenAI-compatible API (OpenAI, Groq, DeepSeek, Local Ollama)."""
        headers = {
            "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": Config.OPENAI_MODEL,
            "temperature": 0.2,
            "max_tokens": 1400,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Medical Report:\n\n{text}"},
            ],
        }
        resp = requests.post(
            f"{Config.OPENAI_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=Config.LLM_TIMEOUT,
        )
        if resp.status_code >= 400:
            raise ValueError(f"OpenAI API Error {resp.status_code}: {resp.text[:300]}")

        body = resp.json()
        content = body["choices"][0]["message"]["content"]
        return cls._parse_json(content)

    @classmethod
    def _parse_json(cls, raw: str) -> Dict[str, Any]:
        """Strips markdown code blocks and deserializes JSON safely."""
        text = (raw or "").strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise ValueError("Model output did not contain a valid JSON object.")
            return json.loads(match.group(0))

