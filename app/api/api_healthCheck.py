from fastapi import APIRouter, Depends
from app.schemas.sche_base import DataResponse
from app.schemas.response_code_enum import ResponseCodeEnum, get_message
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("", response_model=DataResponse[dict],dependencies=[Depends(get_current_user)])
async def get():
    return DataResponse[dict](
        code=ResponseCodeEnum.SUCCESS,
        message=get_message(ResponseCodeEnum.SUCCESS),
        data={"status": "ok"},
    )
