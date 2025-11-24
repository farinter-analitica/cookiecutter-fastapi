from typing import Callable

from fastapi import FastAPI
from loguru import logger
{% if cookiecutter.use_database == "yes" -%}
from sqlalchemy.exc import OperationalError
from db import Base, engine
{% endif -%}
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
import joblib
from core.config import MEMOIZATION_FLAG
{% endif %}

{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
def preload_model():
    """
    In order to load model on memory to each worker
    """
    from services.predict import MachineLearningModelHandlerScore

    MachineLearningModelHandlerScore.get_model(joblib.load)
{% endif %}


def create_start_app_handler(app: FastAPI) -> Callable:
    def start_app() -> None:
        {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
        if MEMOIZATION_FLAG:
            preload_model()
        {% endif -%}
        {% if cookiecutter.use_database == "yes" -%}
        try:
            Base.metadata.create_all(bind=engine)
        except OperationalError:
            logger.exception("failed to initialize database")
        {% endif %}
    return start_app
