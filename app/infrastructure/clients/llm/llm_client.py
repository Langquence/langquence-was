from typing import Protocol
from pydantic import BaseModel
from typing import List

class LlmResponse(BaseModel):
    original: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []


class LlmClient(Protocol):
    async def correct_text(self, input_text: str) -> LlmResponse:
        """입력 텍스트에 대한 교정을 수행합니다."""
        ...
        