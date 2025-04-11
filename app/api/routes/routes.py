from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Header, Depends

from app.api.dto.correct_dto import CorrectionResponse, ErrorResponse
from app.common.aop.ApiLogRouter import ApiLogRouter
from app.common.utils.logger import get_logger
from app.api.usecase.correction_usecase import correct
from app.common.exception.base_exception import UnsupportedMediaTypeException

logger = get_logger(__name__)

router = APIRouter(route_class=ApiLogRouter)


def get_allowed_content_types() -> list:
    return ["application/octet-stream", "audio/wav"]


@router.post("/correct", response_model=CorrectionResponse, responses={500: {"model": ErrorResponse}})
async def correct_english_text(
        request: Request,
        content_type: Optional[str] = Header(None),
        allowed_content_types: list = Depends(get_allowed_content_types)
):
    """
    Corrects English text from audio data.

    Args:
        request (Request): The request object containing audio data.
        content_type (Optional[str]): The content type of the request header.
        allowed_content_types (list): List of allowed content types.

    Returns:
        CorrectionResponse: The response containing correction details.

    Raises:
        HTTPException: If the content type is not supported or an internal error occurs.
    """
    if content_type not in allowed_content_types:
        raise UnsupportedMediaTypeException(
            f"Unsupported media type. Only {', '.join(allowed_content_types)} are supported."
        )

    audio_data = await request.body()
    logger.info(f"Received audio data size: {len(audio_data)} bytes")

    try:
        return await correct(command=audio_data)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        import traceback
        logger.error(f"Detailed error: \n{traceback.format_exc()}")

        raise HTTPException(status_code=500, detail="Internal server error")
