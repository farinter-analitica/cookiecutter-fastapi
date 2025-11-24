"""
Schemas Pydantic para validación de requests/responses
"""
{% if cookiecutter.project_type == "basic_api" -%}
from .task import TaskCreate, TaskUpdate, TaskResponse
{% elif cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
from .prediction import PredictionRequest, PredictionResponse
{% endif %}

__all__ = [
    {% if cookiecutter.project_type == "basic_api" -%}
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    {% elif cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    "PredictionRequest",
    "PredictionResponse",
    {% endif %}
]
