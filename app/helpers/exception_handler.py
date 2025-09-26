import enum

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.schemas.sche_base import ResponseSchemaBase
from app.schemas.response_code_enum import ResponseCodeEnum, get_message


class ExceptionType(enum.Enum):
    MS_UNAVAILABLE = 500, '990'
    MS_INVALID_API_PATH = 500, '991'
    DATA_RESPONSE_MALFORMED = 500, ResponseCodeEnum.SERVER_ERROR.value
    VALIDATION_ERROR = 400, ResponseCodeEnum.SERVER_ERROR.value

    def __new__(cls, http_code, code):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code):
        self.http_code = http_code
        self.code = code


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, ""))
    )


async def validation_exception_handler(request, exc):
    code = ExceptionType.VALIDATION_ERROR.code
    lang = getattr(request, 'lang', None) or None
    base_message = get_message(code, lang)
    detail_message = get_message_validation(exc)
    message = f"{base_message}: {detail_message}" if detail_message else base_message
    return JSONResponse(
        status_code=ExceptionType.VALIDATION_ERROR.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(code, lang, message))
    )


async def fastapi_error_handler(request, exc):
    code = ExceptionType.DATA_RESPONSE_MALFORMED.code
    lang = getattr(request, 'lang', None) or None
    message = get_message(code, lang)
    return JSONResponse(
        status_code=ExceptionType.DATA_RESPONSE_MALFORMED.http_code,
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response(
                code,
                lang,
                message
            )
        )
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + str(error.get("loc")[1]) + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message
