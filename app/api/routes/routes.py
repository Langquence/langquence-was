from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Header

from app.api.dto.correct_dto import CorrectionResponse, ErrorResponse
from app.common.aop.ApiLogRouter import ApiLogRouter
from app.common.utils.logger import get_logger
from app.domain.services.correct_text_helper import process_correction_request, CorrectionCommand
from app.common.exception.base_exception import UnsupportedMediaTypeException

logger = get_logger(__name__)

router = APIRouter(route_class=ApiLogRouter)


@router.post("/correct", response_model=CorrectionResponse, responses={500: {"model": ErrorResponse}})
async def correct_english_text(
        request: Request,
        content_type: Optional[str] = Header(None)
):
    allowed_content_types = ["application/octet-stream", "audio/wav"]
    if content_type not in allowed_content_types:
        raise UnsupportedMediaTypeException(f"Unsupported media type. Only {', '.join(allowed_content_types)} are supported.")

    audio_data = await request.body()
    logger.info(f"Received audio data size: {len(audio_data)} bytes")

    try:
        # 1. 텍스트 교정
        draft_result = await process_correction_request(command=CorrectionCommand(original=audio_data))
        # 2. 피드백 생성 (추후 교정)
        # final_result = await generate_feedback(result)

        return CorrectionResponse(
            original=draft_result.original,
            needs_correction=draft_result.needs_correction,
            corrected=draft_result.corrected,
            explanation=draft_result.explanation,
            alternatives=draft_result.alternatives
        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        import traceback
        logger.error(f"상세 오류: \n{traceback.format_exc()}")

        raise HTTPException(status_code=500, detail="Internal server error")
