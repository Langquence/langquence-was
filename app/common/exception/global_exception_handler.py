from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE

from app.common.exception.base_exception import BaseException
from app.common.utils.logger import get_logger

logger = get_logger(__name__)

async def base_exception_handler(request: Request, ex: BaseException):
    """Base 예외 처리"""
    
    return JSONResponse(
        status_code=ex.status_code,
        content={"message": ex.message}
    )

async def http_exception_handler(request: Request, ex: StarletteHTTPException):
    """HTTP 예외 처리"""
    logger.warn(f'{{"status_code": {ex.status_code}, "detail": "{ex.detail}"}}')
    
    if ex.status_code == HTTP_415_UNSUPPORTED_MEDIA_TYPE:
        return JSONResponse(
            status_code=ex.status_code,
            content={"message": "지원하지 않는 미디어 타입입니다."}
        )
    
    return JSONResponse(
        status_code=ex.status_code,
        content={"message": ex.detail}
    )

async def validation_exception_handler(request: Request, ex: RequestValidationError):
    """422 Unprocessable Entity 예외 처리"""
    logger.warn(f'{{"status_code": 422, "detail": "{str(ex)}"}}')
    
    return JSONResponse(
        status_code=422,
        content={"message": "입력 데이터 검증 오류", "detail": ex.errors()}
    )

async def global_exception_handler(request: Request, ex: Exception):
    """서버에서 예상치 못한 오류가 발생했을 때 500 예외 처리"""
    logger.error(f'{{"status_code": 500, "detail": "서버에서 예상치 못한 오류가 발생했습니다."}}')
    
    return JSONResponse(
        status_code=500,
        content={"message": "서버에서 예상치 못한 오류가 발생했습니다."}
    )