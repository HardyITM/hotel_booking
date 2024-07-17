from typing import Literal

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file='.env')
    
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    
    SECRET_KEY: str
    ALGORITHM: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    
    REDIS_URL: str
    
    ADM_LOGIN: str
    ADM_PASSWORD: str
    
    MODE: Literal['DEV', 'TEST', 'PROD']
    LOG_LEVEL: Literal['INFO', 'DEBUG']
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    
    # class Config:
    #     env_file = '.env'
    
settings = Settings()