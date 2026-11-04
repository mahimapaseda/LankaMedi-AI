"""Clinical biomarker extraction and Sri Lankan reference range evaluation engine."""

import re
import logging
from typing import List, Optional, Tuple
from core.constants import CLINICAL_REFERENCE_RANGES, SRI_LANKA_EMERGENCY_CONTACTS
from schemas.analysis_schema import BiomarkerResult, EmergencyAlert

logger = logging.getLogger(__name__)


# Regular expression patterns for extracting diagnostic parameters from typical Sri Lankan lab formats
BIOMARKER_EXTRACTION_PATTERNS = {
    "platelets": [
        re.compile(r"(?i)(?:platelet\s*count|platelets?|plt)\s*[:=\-]?\s*(\d{2,3}(?:,\d{3})+|\d{4,6})", re.IGNORECASE),
        re.compile(r"(?i)(?:platelet\s*count|platelets?|plt)\s*[:=\-]?\s*(\d{1,3}(?:\.\d+)?)\s*(?:x\s*10\^?[39]|k/u[lL]|lakh)", re.IGNORECASE),
    ],
    "hemoglobin": [
        re.compile(r"(?i)(?:ha?emoglobin|hgb|hb)\s*[:=\-]?\s*(\d{1,2}(?:\.\d+)?)\s*(?:g/d[lL]|g/L|gm%)?", re.IGNORECASE),
    ],
    "fbs": [
        re.compile(r"(?i)(?:fasting\s*blood\s*sugar|fbs|fasting\s*glucose|f\.b\.s)\s*[:=\-]?\s*(\d{2,3}(?:\.\d+)?)\s*(?:mg/d[lL]|mmol/L)?", re.IGNORECASE),
    ],
    "hba1c": [
        re.compile(r"(?i)(?:glycated\s*ha?emoglobin|hba1c|hb\s*a1c)\s*[:=\-]?\s*(\d{1,2}(?:\.\d+)?)\s*%", re.IGNORECASE),
    ],
    "creatinine": [
        re.compile(r"(?i)(?:serum\s*creatinine|s\.?\s*creatinine|creatinine)\s*[:=\-]?\s*(\d{1,2}(?:\.\d+)?)\s*(?:mg/d[lL]|umol/L)?", re.IGNORECASE),
    ],
    "total_cholesterol": [
        re.compile(r"(?i)(?:total\s*cholesterol|s\.?\s*cholesterol)\s*[:=\-]?\s*(\d{2,3}(?:\.\d+)?)\s*(?:mg/d[lL])?", re.IGNORECASE),
    ],
    "ldl": [
        re.compile(r"(?i)(?:ldl\s*cholesterol|ldl)\s*[:=\-]?\s*(\d{2,3}(?:\.\d+)?)\s*(?:mg/d[lL])?", re.IGNORECASE),
    ],
    "hdl": [
        re.compile(r"(?i)(?:hdl\s*cholesterol|hdl)\s*[:=\-]?\s*(\d{2,3}(?:\.\d+)?)\s*(?:mg/d[lL])?", re.IGNORECASE),
    ],
    "triglycerides": [
        re.compile(r"(?i)(?:serum\s*triglycerides|triglycerides?|tg)\s*[:=\-]?\s*(\d{2,4}(?:\.\d+)?)\s*(?:mg/d[lL])?", re.IGNORECASE),
    ],
    "sgpt_alt": [
        re.compile(r"(?i)(?:sgpt\s*/\s*alt|alt\s*/\s*sgpt|sgpt|alt)\s*[:=\-]?\s*(\d{1,4}(?:\.\d+)?)\s*(?:u/L|IU/L)?", re.IGNORECASE),
    ],
    "sgot_ast": [
        re.compile(r"(?i)(?:sgot\s*/\s*ast|ast\s*/\s*sgot|sgot|ast)\s*[:=\-]?\s*(\d{1,4}(?:\.\d+)?)\s*(?:u/L|IU/L)?", re.IGNORECASE),
    ],
}


class BiomarkerEngine:
    """Extracts, standardizes, and evaluates laboratory markers against reference intervals."""

    @classmethod
    def evaluate_text(cls, text: str) -> Tuple[List[BiomarkerResult], Optional[EmergencyAlert]]:
        """Parses biomarkers from clinical text and checks for emergency triage conditions."""
        biomarkers: List[BiomarkerResult] = []
        emergency_triggers: List[str] = []

        for key, patterns in BIOMARKER_EXTRACTION_PATTERNS.items():
            ref_info = CLINICAL_REFERENCE_RANGES.get(key)
            if not ref_info:
                continue

            value = cls._extract_value(text, patterns, key)
            if value is None:
                continue

            status, interpretation = cls._assess_value(value, ref_info)

            # Check emergency red-flag criteria
            if key == "platelets" and value <= ref_info.get("critical_low", 50000):
                emergency_triggers.append(
                    f"Critically low Platelets ({int(value):,} /uL) — Urgent hospital evaluation required for Dengue or bleeding risk."
                )
            elif key == "fbs" and (value < 50.0 or value > 350.0):
                emergency_triggers.append(
                    f"Severe blood glucose derangement (FBS: {value} mg/dL) — Risk of acute diabetic crisis."
                )
            elif key == "hemoglobin" and value <= ref_info.get("critical_low", 7.0):
                emergency_triggers.append(
                    f"Severe Anemia (Hb: {value} g/dL) — Life-threatening oxygen perfusion risk."
                )
            elif key == "creatinine" and value >= ref_info.get("critical_high", 3.0):
                emergency_triggers.append(
                    f"Significantly elevated Creatinine ({value} mg/dL) — Acute/severe kidney injury."
                )

            low_str = f"{ref_info['low']}" if ref_info.get("low") is not None else "0"
            high_str = f"{ref_info['high']}" if ref_info.get("high") is not None else "N/A"
            ref_interval_str = f"{low_str} - {high_str} {ref_info['unit']}"

            biomarkers.append(
                BiomarkerResult(
                    key=key,
                    display_name=ref_info["display_name"],
                    observed_value=value,
                    unit=ref_info["unit"],
                    reference_interval=ref_interval_str,
                    status=status,
                    interpretation=interpretation,
                    category=ref_info["category"],
                )
            )

        emergency_alert = None
        if emergency_triggers:
            emergency_alert = EmergencyAlert(
                is_emergency=True,
                trigger_reason=" | ".join(emergency_triggers),
                hotline=SRI_LANKA_EMERGENCY_CONTACTS["ambulance"]["number"],
                hotline_name=SRI_LANKA_EMERGENCY_CONTACTS["ambulance"]["name"],
                action_plan=(
                    "Critical physiological markers detected. If the patient has warning signs (bleeding, "
                    "fainting, abdominal pain, persistent vomiting, chest pain), seek emergency hospital "
                    "admission or dial 1990 Suwa Seriya immediately."
                ),
            )

        return biomarkers, emergency_alert

    @classmethod
    def _extract_value(cls, text: str, patterns: list, key: str) -> Optional[float]:
        """Tries regular expressions against text to extract numerical values."""
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                raw_val = match.group(1).replace(",", "")
                try:
                    val = float(raw_val)
                    # Heuristic normalization for platelets (e.g. if reported as '1.2 lakh' or '120 k')
                    if key == "platelets":
                        if val < 1000:
                            val = val * 1000.0  # e.g., 150 -> 150,000
                    return round(val, 2)
                except (ValueError, TypeError):
                    continue
        return None

    @classmethod
    def _assess_value(cls, val: float, ref_info: dict) -> Tuple[str, str]:
        """Evaluates value against low, high, and critical boundaries."""
        low = ref_info.get("low")
        high = ref_info.get("high")
        crit_low = ref_info.get("critical_low")
        crit_high = ref_info.get("critical_high")

        if crit_low is not None and val <= crit_low:
            return "Critical", f"Critically below safe reference limits ({val} {ref_info['unit']}). Immediate clinical attention required."
        if crit_high is not None and val >= crit_high:
            return "Critical", f"Critically elevated above safe limits ({val} {ref_info['unit']}). Urgent specialist evaluation advised."
        if low is not None and val < low:
            return "Low", f"Lower than standard reference interval ({val} < {low} {ref_info['unit']})."
        if high is not None and val > high:
            return "High", f"Higher than standard reference interval ({val} > {high} {ref_info['unit']})."

        return "Normal", f"Within normal physiological reference interval ({val} {ref_info['unit']})."

