import logging.config

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.api.router.api_router import router
from app.api.api_auth import router as auth_router
from app.models import Base
from app.db.base import engine
from app.core.config import settings
from app.helpers.exception_handler import CustomException, http_exception_handler
from app.schemas.sche_base import ResponseSchemaBase
from app.schemas.response_code_enum import ResponseCodeEnum, get_message

logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)
Base.metadata.create_all(bind=engine)


def http_error_handler(request: Request, exc: HTTPException):
    code = str(exc.status_code)
    lang = getattr(request, 'lang', 'en')
    message = exc.detail if hasattr(exc, 'detail') and exc.detail else get_message(code, lang)
    resp = ResponseSchemaBase.custom_response(code, lang, data=None)
    if message:
        resp["message"] = message
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(resp)
    )


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, docs_url="/docs", redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='''
        Base frame with FastAPI micro framework + Postgresql
            - Login/Register with JWT
            - Permission
            - CRUD User
            - Unit testing with Pytest
            - Dockerize
        '''
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(router, prefix=settings.API_PREFIX)
    application.include_router(auth_router, prefix="/auth")
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(HTTPException, http_error_handler)

    return application


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Please enter a valid JWT token"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = get_application()
app.openapi = custom_openapi
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
