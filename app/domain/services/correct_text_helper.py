from fastapi import Depends

from infrastructure.clients.llm.alibaba.qwen_client import correct_text
from domain.services.pattern_matching import validate_correction
from common.utils.logger import get_logger

from infrastructure.clients.llm.llm_client import get_llm_client

from pydantic import BaseModel
from typing import List

logger = get_logger(__name__)

class CorrectionCommand(BaseModel):
    original: bytes

class CorrectionResult(BaseModel):
    original: str
    needs_correction: bool
    corrected: str
    explanation: str
    alternatives: List[str] = []

async def process_correction_request(
        command: CorrectionCommand,
        llm_client=Depends(get_llm_client)
    ):
    
    try:
        # 1. STT 결과 추출
        text = command.original.decode("utf-8")

        # 1. 텍스트 교정 (API 호출)
        logger.info(f"Processing correction request: {text}")
        correction_result = await llm_client.correct_text(text)
        
        # 2. 패턴 매칭 검증
        validated_result = await validate_correction(correction_result)
        
        return CorrectionResult(
            original=validated_result.original,
            needs_correction=validated_result.needs_correction,
            corrected=validated_result.corrected,
            explanation=validated_result.explanation,
            alternatives=validated_result.alternatives
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise e
