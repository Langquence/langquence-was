from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CorrectionDetail(BaseModel):
    error: str
    correct: str
    reason: str

class SentenceCorrection(BaseModel):
    original: str
    boundary_corrected: str
    needs_correction: bool
    corrected: str = ""
    explanation: List[CorrectionDetail]
    alternatives: List[str]

class CorrectionResponse(BaseModel):
    id: int
    data: List[SentenceCorrection]

class ErrorResponse(BaseModel):
    error: str
    message: Optional[Dict[str, Any]] = None