"""Pydantic schemas for request validation, structured biomarker data, and clinical analysis output."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class BiomarkerResult(BaseModel):
    """Structured clinical biomarker evaluation."""
    key: str
    display_name: str
    observed_value: float
    unit: str
    reference_interval: str
    status: Literal["Normal", "Low", "High", "Critical"]
    interpretation: str
    category: str


class TreatmentPlan(BaseModel):
    """Clinical educational recommendations and monitoring items."""
    conditions: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    lifestyle: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class EmergencyAlert(BaseModel):
    """Emergency alert details when critical life-threatening markers are detected."""
    is_emergency: bool = False
    trigger_reason: str = ""
    hotline: str = "1990"
    hotline_name: str = "1990 Suwa Seriya Emergency Ambulance"
    action_plan: str = ""


class AnalysisResponse(BaseModel):
    """Comprehensive analysis response payload returned to the client."""
    status: Literal["Good", "Needs Attention", "Critical"]
    color: str
    critical_issues: int = 0
    warning_issues: int = 0
    positive_indicators: int = 0
    treatment_plan: TreatmentPlan
    biomarkers: List[BiomarkerResult] = Field(default_factory=list)
    emergency_alert: Optional[EmergencyAlert] = None
    language: str = "en"
    provider_used: str = "Unknown"
    disclaimer: str = ""


class AnalysisRequest(BaseModel):
    """Validation for incoming text-based analysis requests."""
    report_text: str = Field(..., min_length=5, description="Medical report text or clinical note")
    language: Literal["en", "si", "ta"] = Field(default="en", description="Preferred response language")

