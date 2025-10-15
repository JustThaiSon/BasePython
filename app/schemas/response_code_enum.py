from enum import IntEnum
from typing import Dict
import json
import os
from app.core.config import settings

# Load messages from JSON resource file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGES_PATH = os.path.join(BASE_DIR, "resources", "messages.json")
with open(MESSAGES_PATH, encoding="utf-8") as f:
    RESPONSE_MESSAGES: Dict[str, Dict[str, str]] = json.load(f)


class ResponseCodeEnum(IntEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERROR = 500
    SYSTEM_ERROR = 500
    MAINTENANCE = 990
    MAINTENANCE_LONG = 991
    SYSTEM_ERROR_CONTACT_ADMIN = 992


def get_message(code: int, lang: str = None) -> str:
    if lang is None:
        lang = settings.DEFAULT_LANG
    str_code = str(code)
    messages = RESPONSE_MESSAGES.get(str_code, {})
    return messages.get(lang, messages.get("en", ""))
