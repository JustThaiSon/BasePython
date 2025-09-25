from fastapi import APIRouter
from app.schemas.sche_base import DataResponse
from app.schemas.response_code_enum import ResponseCodeEnum, get_message

router = APIRouter()


@router.get("", response_model=DataResponse[dict])
async def get():
    return DataResponse[dict](
        code=ResponseCodeEnum.SUCCESS,
        message=get_message(ResponseCodeEnum.SUCCESS),
        data={"status": "ok"},
    )
