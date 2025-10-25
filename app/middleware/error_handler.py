import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from app.schemas.response_code_enum import ResponseCodeEnum, get_message
from app.schemas.sche_base import ResponseSchemaBase

# Lấy logger (theo logging.ini)
logger = logging.getLogger(__name__)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Tiếp tục luồng xử lý request
            response = await call_next(request)
            return response

        except RequestValidationError as e:
            # 🚨 Ghi log lỗi validate
            logger.warning(f"Validation error: {e.errors()}")

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ResponseSchemaBase.custom_response(
                    code=ResponseCodeEnum.BAD_REQUEST
                ),
            )

        except Exception as e:
            # 🚨 Ghi log lỗi hệ thống (stack trace)
            logger.exception(f"Unhandled exception: {str(e)}")

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ResponseSchemaBase.custom_response(
                    code=ResponseCodeEnum.SERVER_ERROR
                ),
            )
