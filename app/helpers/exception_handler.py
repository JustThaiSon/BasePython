from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.schemas.response_code_enum import ResponseCodeEnum, get_message
from sqlalchemy.exc import SQLAlchemyError
from typing import Union, Optional
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


class CustomException(Exception):
    def __init__(self, http_code: int, code: int = ResponseCodeEnum.SERVER_ERROR, message: Optional[str] = None):
        self.http_code = http_code
        self.code = code
        self.message = message


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content={
            "code": exc.code,
            "message": exc.message or get_message(exc.code),
            "data": None
        }
    )


async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": ResponseCodeEnum.BAD_REQUEST,
            "message": str(exc),
            "data": None
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ResponseCodeEnum.SERVER_ERROR,
            "message": get_message(ResponseCodeEnum.SERVER_ERROR),
            "data": None
        }
    )


async def http_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ResponseCodeEnum.SERVER_ERROR,
            "message": get_message(ResponseCodeEnum.SERVER_ERROR),
            "data": None
        }
    )
