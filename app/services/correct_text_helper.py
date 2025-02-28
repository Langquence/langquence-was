from app.clients.alibaba.llm.qwen_client import correct_text
from app.services.pattern_matching import validate_correction
from app.services.feedback_generator import generate_feedback
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def process_correction_request(text: str):
    try:
        # 1. 텍스트 교정 (API 호출)
        logger.info(f"Processing correction request: {text}")
        correction_result = await correct_text(text)
        
        # 2. 패턴 매칭 검증
        validated_result = await validate_correction(correction_result)
        
        return validated_result
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise e
