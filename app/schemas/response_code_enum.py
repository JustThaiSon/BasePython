from enum import Enum
from typing import Dict
import json
import os
from app.core.config import settings

# Load messages from JSON resource file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESSAGES_PATH = os.path.join(BASE_DIR, "resources", "messages.json")
with open(MESSAGES_PATH, encoding="utf-8") as f:
    RESPONSE_MESSAGES: Dict[str, Dict[str, str]] = json.load(f)

class ResponseCodeEnum(str, Enum):
    SUCCESS = "200"
    NOT_FOUND = "404"
    SERVER_ERROR = "500"


def get_message(code: str, lang: str = None) -> str:
    if lang is None:
        lang = settings.DEFAULT_LANG
    messages = RESPONSE_MESSAGES.get(code, {})
    return messages.get(lang, messages.get("en", ""))
