import os
import logging
import logging.config
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Load logging config at startup
logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.ini'), disable_existing_loggers=False)
logger = logging.getLogger('myapp')
logger.info('Logging system initialized!')

class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default='FASTAPI BASE')
    SECRET_KEY: str = Field(default='')
    API_PREFIX: str = Field(default='')
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=lambda: ['*'])
    DATABASE_URL: str = Field(default='')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = Field(default=60 * 60 * 24 * 7)
    SECURITY_ALGORITHM: str = Field(default='HS256')
    LOGGING_CONFIG_FILE: str = Field(default=os.path.join(BASE_DIR, 'logging.ini'))
    DEFAULT_LANG: str = Field(default='en')  # Thêm cấu hình ngôn ngữ mặc định

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, '.env'), extra='ignore')


settings = Settings()
