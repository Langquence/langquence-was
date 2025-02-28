from fastapi import APIRouter, HTTPException
from app.dto.schemas import CorrectionRequest, CorrectionResponse, ErrorResponse
from app.services.correct_text_helper import process_correction_request
from app.services.pattern_matching import validate_correction
from app.services.feedback_generator import generate_feedback
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/correct", response_model=CorrectionResponse, responses={500: {"model": ErrorResponse}})
async def correct_english_text(request: CorrectionRequest):
    try:
        # 1. 텍스트 교정
        logger.info(f"Processing correction request: {request.text}")
        result = await process_correction_request(request.text)
        
        # 2. 피드백 생성
        final_result = await generate_feedback(result)
        
        return final_result
    except Exception as e:
        logger.error(f"Error processing request: {e}")

        raise HTTPException(
            status_code=500,
            message={"error": "Failed to process correction request", "details": str(e)}
        )