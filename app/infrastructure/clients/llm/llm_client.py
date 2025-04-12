from typing import Protocol
from pydantic import BaseModel, Field
from typing import List

class CorrectionDetail(BaseModel):
    error: str
    correct: str
    reason: str

class SentenceCorrection(BaseModel):
    original: str
    boundary_corrected: str
    needs_correction: bool
    corrected: str = ""
    explanation: List[CorrectionDetail] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)

class LlmResponse(BaseModel):
    sentences: List[SentenceCorrection]

class LlmClient(Protocol):
    async def correct_text(self, input_text: str) -> LlmResponse:
        """입력 텍스트에 대한 교정을 수행합니다."""
        ...