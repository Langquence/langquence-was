from app.common.utils.logger import get_logger
from typing import Any, Callable, Dict

from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

logger = get_logger(__name__)

class ApiLogRouter(APIRoute):
    def get_route_handler(self) -> Callable:
        """API 요청과 응답을 로깅하는 라우터 핸들러를 반환합니다."""
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            await self._request_log(request)
            response: Response = await original_route_handler(request)
            self._response_log(request, response)
            return response

        return custom_route_handler
    
    async def _request_log(self, request: Request) -> None:
        extra: Dict[str, Any] = {
            "httpMethod": request.method,
            "path": request.url.path,
            "headers": request.headers,
            "queryParameters": request.query_params
        }

        if self._should_log_body(request):
            request_body = await request.body()
            extra["body"] = request_body.decode("utf-8")

        logger.info(f"API Request:\n{extra}")

    @staticmethod
    def _should_log_body(request: Request) -> bool:
        """요청 본문을 로깅해야 하는지 확인합니다."""
        return request.method in ("POST", "PUT", "PATCH") and request.headers.get("content-type") == "application/json"

    @staticmethod
    def _response_log(request: Request, response: Response) -> None:
        extra: Dict[str, str] = {
            "httpMethod": request.method,
            "path": request.url.path,
            "statusCode": response.status_code
        }

        logger.info(f"API Response:\n{extra}")