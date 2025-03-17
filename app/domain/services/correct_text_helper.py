from fastapi import Depends

from app.infrastructure.clients.llm.alibaba.qwen_client import correct_text
from app.domain.services.pattern_matching import validate_correction
from app.common.utils.logger import get_logger
from domain.command.correct_command import CorrectionCommand

from infrastructure.clients.llm.llm_client import get_llm_client

logger = get_logger(__name__)

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
        
        return validated_result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise e
