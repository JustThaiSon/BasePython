from typing import Optional, TypeVar, Generic
from pydantic import BaseModel
from app.schemas.response_code_enum import ResponseCodeEnum, get_message

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    code: str = ''
    message: str = ''

    @classmethod
    def custom_response(cls, code: str, lang: str = "en", data: Optional[T] = None):
        msg = get_message(code, lang)
        resp = {"code": code, "message": msg}
        if data is not None:
            resp["data"] = data
        return resp

    @classmethod
    def success_response(cls, data: Optional[T] = None, lang: str = "en"):
        return cls.custom_response(ResponseCodeEnum.SUCCESS, lang, data)


class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
