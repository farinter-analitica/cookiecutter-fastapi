from fastapi import APIRouter
from api.routes import healthcheck
{% if cookiecutter.project_type == "basic_api" -%}
from api.routes import tasks
{% endif -%}
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
from api.routes import predictor
{% endif %}
router = APIRouter()

# Healthcheck routes (available in all project types)
router.include_router(healthcheck.router, tags=["healthcheck"])

{% if cookiecutter.project_type == "basic_api" -%}
# Tasks routes (basic_api only)
router.include_router(tasks.router, tags=["tasks"], prefix="/tasks")
{% endif -%}
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
# ML Predictor routes (ml_api and ai_rag_api only)
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
{% endif %}
