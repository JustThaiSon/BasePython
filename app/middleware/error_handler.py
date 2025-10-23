from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from app.schemas.response_code_enum import ResponseCodeEnum
from app.schemas.sche_base import ResponseSchemaBase


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Tiếp tục xử lý request
            response = await call_next(request)
            return response

        except RequestValidationError as e:
            # Lỗi validate từ FastAPI (body/query params)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=ResponseSchemaBase.custom_response(
                    code=ResponseCodeEnum.BAD_REQUEST,
                    data=str(e)
                ),
            )

        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ResponseSchemaBase.custom_response(
                    code=ResponseCodeEnum.SERVER_ERROR,
                    data=str(e)
                ),
            )
