from pydantic import BaseModel
from typing import Optional

class NoteRequest(BaseModel):
    note: str
    patient_age: Optional[int] = None
    patient_sex: Optional[str] = None

class RiskFlag(BaseModel):
    category: str        # e.g. "medication", "vital signs", "symptom"
    detail: str          # e.g. "Metformin + contrast dye interaction"
    severity: str        # "high", "medium", "low"

class SummaryResponse(BaseModel):
    summary: str
    key_findings: list[str]
    risk_flags: list[RiskFlag]
    recommended_actions: list[str]