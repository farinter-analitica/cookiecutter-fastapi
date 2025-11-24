"""
Dependencias compartidas para los routers.
"""
{% if cookiecutter.use_database == "yes" -%}
from sqlalchemy.orm import Session
from app.db import get_db
{% endif %}
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
from app.services.ml_service import get_ml_service, MLService
{% endif %}

# Exportar para facilitar el uso
__all__ = [
    {% if cookiecutter.use_database == "yes" -%}
    "get_db",
    {% endif %}
    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    "get_ml_service",
    {% endif %}
]
