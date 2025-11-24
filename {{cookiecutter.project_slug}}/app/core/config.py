import logging
import sys
from typing import Optional

from core.logging import InterceptHandler
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación con validación Pydantic"""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

    # Configuración de la API
    API_PREFIX: str = "/api"
    PROJECT_NAME: str = "{{cookiecutter.project_name}}"
    VERSION: str = "{{cookiecutter.version}}"
    DEBUG: bool = False
    APP_ENV: str = "dev"
    APP_PORT: int = 8000

    # Seguridad
    SECRET_KEY: str = "changeme-in-production"

    {% if cookiecutter.use_database == "yes" -%}
    # Configuración de Base de Datos
    {% if cookiecutter.database_type == "postgresql" -%}
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/{{cookiecutter.project_slug}}"
    {% elif cookiecutter.database_type == "sqlserver" -%}
    DATABASE_URL: str = "mssql+pyodbc://sa:YourPassword123@localhost:1433/{{cookiecutter.project_slug}}?driver=ODBC+Driver+17+for+SQL+Server"
    {% else -%}
    DATABASE_URL: str = "sqlite:///./{{cookiecutter.project_slug}}.db"
    {% endif -%}
    MAX_CONNECTIONS_COUNT: int = 10
    MIN_CONNECTIONS_COUNT: int = 10
    {% endif %}

    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    # Configuración de ML/IA
    MODEL_PATH: str = "{{cookiecutter.machine_learn_model_path}}"
    MODEL_NAME: str = "{{cookiecutter.machine_learn_model_name}}"
    INPUT_EXAMPLE: str = "{{cookiecutter.input_example_path}}"
    MEMOIZATION_FLAG: bool = True
    {% endif %}

    {% if cookiecutter.use_ai_services == "yes" -%}
    # Configuración de Servicios de IA
    {% if cookiecutter.ai_provider == "openai" -%}
    OPENAI_API_KEY: Optional[str] = None
    DEFAULT_MODEL_CHAT: str = "gpt-4o-mini"
    DEFAULT_MODEL_EMB: str = "text-embedding-3-small"
    {% elif cookiecutter.ai_provider == "gemini" -%}
    GEMINI_API_KEY: Optional[str] = None
    DEFAULT_MODEL_CHAT: str = "gemini-1.5-flash"
    DEFAULT_MODEL_EMB: str = "text-embedding-004"
    {% elif cookiecutter.ai_provider == "huggingface" -%}
    HUGGINGFACE_API_KEY: Optional[str] = None
    DEFAULT_MODEL: str = "meta-llama/Llama-2-7b-hf"
    {% endif %}
    {% endif %}

    {% if cookiecutter.use_redis == "yes" -%}
    # Configuración de Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    {% endif %}

    {% if cookiecutter.use_workers == "yes" -%}
    # Configuración de Workers
    {% if cookiecutter.worker_type == "celery" -%}
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    {% elif cookiecutter.worker_type == "rq" -%}
    RQ_REDIS_URL: str = "redis://localhost:6379/0"
    QUEUE_NAME: str = "default"
    {% endif %}
    {% endif %}

    {% if cookiecutter.use_storage == "yes" -%}
    # Configuración de Almacenamiento
    {% if cookiecutter.storage_type == "minio" -%}
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "{{cookiecutter.project_slug}}"
    MINIO_SECURE: bool = False
    {% elif cookiecutter.storage_type == "s3" -%}
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "{{cookiecutter.project_slug}}"
    {% elif cookiecutter.storage_type == "local" -%}
    UPLOAD_DIR: str = "./uploads"
    {% endif %}
    {% endif %}

    # Configuración de CORS
    CORS_ORIGINS: str = "*"  # Lista separada por comas


settings = Settings()

# Configuración de logging
LOGGING_LEVEL = logging.DEBUG if settings.DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

# Exportar variables para compatibilidad con imports directos
API_PREFIX = settings.API_PREFIX
PROJECT_NAME = settings.PROJECT_NAME
VERSION = settings.VERSION
DEBUG = settings.DEBUG

{% if cookiecutter.use_database == "yes" -%}
DATABASE_URL = settings.DATABASE_URL
{% endif -%}

{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
MODEL_PATH = settings.MODEL_PATH
MODEL_NAME = settings.MODEL_NAME
INPUT_EXAMPLE = settings.INPUT_EXAMPLE
MEMOIZATION_FLAG = settings.MEMOIZATION_FLAG
{% endif %}
