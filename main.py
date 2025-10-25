import logging.config
import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.router.api_router import router
from app.middleware.error_handler import ExceptionMiddleware
from app.models import Base
from app.db.base import engine
from app.core.config import settings
from app.helpers.exception_handler import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    http_exception_handler,
    CustomException
)
from app.schemas.sche_base import ResponseSchemaBase
from app.schemas.response_code_enum import get_message


# ---------------------- LOGGING ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(log_dir, exist_ok=True)

# Tạo logging configuration programmatically để tránh escape sequence issues
log_file = os.path.join(log_dir, "app.log")
if not os.path.exists(log_file):
    open(log_file, "a").close()  # tạo file rỗng nếu chưa có

# Configure logging programmatically
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, mode='a', encoding='utf-8')
    ]
)

logger = logging.getLogger("myapp")
logger.info("✅ Logging system initialized!")


# ---------------------- DATABASE INIT ----------------------
Base.metadata.create_all(bind=engine)


# ---------------------- HANDLERS ----------------------
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


# ---------------------- APP FACTORY ----------------------
def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/docs",
        redoc_url="/re-docs",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='''
        Base frame with FastAPI micro framework + PostgreSQL
        - Login/Register with JWT
        '''
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware DB
    app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

    # Middleware xử lý exception
    app.add_middleware(ExceptionMiddleware)

    # Routers
    app.include_router(router, prefix=settings.API_PREFIX)

    # Exception handlers
    app.add_exception_handler(CustomException, http_exception_handler)
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, http_error_handler)

    return app


# ---------------------- OPENAPI CUSTOM ----------------------
def custom_openapi(app: FastAPI):
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


# ---------------------- APP INSTANCE ----------------------
app = create_application()
app.openapi = lambda: custom_openapi(app)


# ---------------------- RUN SERVER ----------------------
if __name__ == "__main__":
    logger.info("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=9999)
