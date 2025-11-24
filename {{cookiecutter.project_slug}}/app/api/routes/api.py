from fastapi import APIRouter

{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
from api.routes import predictor
{% endif %}
router = APIRouter()
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
{% endif %}
