from fastapi import APIRouter, HTTPException
from app.dto.schemas import CorrectionRequest, CorrectionResponse, ErrorResponse
from app.domain.services.correct_text_helper import process_correction_request
from app.domain.services.feedback_generator import generate_feedback
from app.common.utils.logger import get_logger

from app.common.aop.ApiLogRouter import ApiLogRouter

logger = get_logger(__name__)

router = APIRouter(route_class=ApiLogRouter)

@router.post("/correct", response_model=CorrectionResponse, responses={500: {"model": ErrorResponse}})
async def correct_english_text(request: CorrectionRequest):
    try:
        # 1. 텍스트 교정
        result = await process_correction_request(request.text)
        
        # 2. 피드백 생성
        final_result = await generate_feedback(result)
        
        return final_result
    except Exception as e:
        logger.error(f"Error processing request: {e}")

        raise HTTPException(
            status_code=500,
            message={"error": "Failed to process correction request", "message": "Internal server error"}
        )