"""REST API endpoints for medical report analysis, health checking, and de-identification."""

import logging
from pathlib import Path
from flask import Blueprint, request, jsonify
from core.config import Config
from core.constants import CLINICAL_REFERENCE_RANGES, SRI_LANKA_EMERGENCY_CONTACTS
from core.security import FileSecurityValidator, PIIScrubber
from services.document_service import DocumentService
from services.ocr_service import OCRService
from services.llm_service import LLMOrchestrator

logger = logging.getLogger(__name__)

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route("/health", methods=["GET"])
def health_check():
    """System health and active model provider status."""
    return jsonify({
        "status": "healthy",
        "service": "LankaMedi AI",
        "version": "2.0.0",
        "active_providers": Config.get_active_providers(),
        "sri_lanka_emergency_ambulance": "1990",
    })


@api_bp.route("/reference-ranges", methods=["GET"])
def get_reference_ranges():
    """Returns established Sri Lankan clinical laboratory reference intervals and helplines."""
    return jsonify({
        "reference_ranges": CLINICAL_REFERENCE_RANGES,
        "emergency_contacts": SRI_LANKA_EMERGENCY_CONTACTS,
    })


@api_bp.route("/deidentify", methods=["POST"])
def preview_deidentification():
    """Sanitizes sensitive patient identifiers (NIC, phone numbers, lab names)."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    sanitized = PIIScrubber.redact_text(text)
    return jsonify({
        "original_length": len(text),
        "sanitized_length": len(sanitized),
        "sanitized_text": sanitized,
    })


@api_bp.route("/analyze", methods=["POST"])
def analyze_report():
    """Primary analysis endpoint accepting multipart file or direct text payload."""
    try:
        language = "en"
        report_text = ""

        if "report_file" in request.files:
            file = request.files["report_file"]
            if not file or file.filename == "":
                return jsonify({"error": "No file selected for analysis."}), 400

            file_bytes = file.read()
            is_valid, err_msg = FileSecurityValidator.validate_file(file.filename, file_bytes)
            if not is_valid:
                return jsonify({"error": err_msg}), 400

            ext = Path(file.filename).suffix.lower()
            language = request.form.get("language", "en").lower().strip()

            if ext == ".pdf":
                report_text = DocumentService.extract_text_from_pdf(file_bytes)
            else:
                report_text = OCRService.extract_text(file_bytes)

        else:
            data = request.get_json(silent=True) or {}
            report_text = data.get("report_text", "")
            language = data.get("language", "en").lower().strip()

        if language not in ("en", "si", "ta"):
            language = "en"

        if not str(report_text).strip():
            return jsonify({"error": "Please provide medical report text or upload a valid file."}), 400

        analysis_result = LLMOrchestrator.analyze_medical_text(report_text, language=language)
        return jsonify(analysis_result.model_dump())

    except ValueError as val_err:
        logger.warning("Clinical analysis validation error: %s", val_err)
        return jsonify({"error": str(val_err)}), 400
    except Exception as exc:
        logger.error("Internal processing error: %s", exc, exc_info=True)
        return jsonify({"error": f"Analysis failed: {str(exc)}"}), 500

