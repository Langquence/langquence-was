from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class CorrectionRequest(BaseModel):
    text: str
    
class Alternative(BaseModel):
    text: str
    
class CorrectionResponse(BaseModel):
    original: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []
    
class ErrorResponse(BaseModel):
    error: str
    message: Optional[Dict[str, Any]] = None