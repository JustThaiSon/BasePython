import os
from typing import Optional, TypeVar, Generic

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict
from app.schemas.response_code_enum import ResponseCodeEnum, get_message

load_dotenv()
T = TypeVar("T")

class ResponseSchemaBase(BaseModel):
    code: int = 0
    message: str = ''

    @classmethod
    def custom_response(cls, code: int, lang: Optional[str] = None, data: Optional[T] = None):
        lang = lang or os.getenv("DEFAULT_LANG", "en")
        msg = get_message(code, lang)
        return {"code": code, "message": msg, "data": data}

    @classmethod
    def success_response(cls, data: Optional[T] = None, lang: Optional[str] = None):
        lang = lang or os.getenv("DEFAULT_LANG", "en")
        return cls.custom_response(ResponseCodeEnum.SUCCESS, lang, data)


class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
