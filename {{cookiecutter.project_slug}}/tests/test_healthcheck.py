"""
Tests para el endpoint de healthcheck
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_healthcheck_endpoint():
    """Test del endpoint /api/healthcheck"""
    response = client.get("/api/healthcheck")

    assert response.status_code in [200, 503]  # 200 si todo está bien, 503 si hay componentes degradados
    data = response.json()

    assert "status" in data
    assert "timestamp" in data
    assert "service" in data
    assert "components" in data
    assert "summary" in data


def test_liveness_endpoint():
    """Test del endpoint /api/liveness"""
    response = client.get("/api/liveness")

    assert response.status_code == 200
    data = response.json()

    assert data["alive"] is True
    assert "timestamp" in data


def test_readiness_endpoint():
    """Test del endpoint /api/readiness"""
    response = client.get("/api/readiness")

    assert response.status_code in [200, 503]
    data = response.json()

    assert "ready" in data
    assert "checks" in data
    assert "timestamp" in data


{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
def test_healthcheck_includes_ml_model():
    """Test que verifica que el healthcheck incluye el modelo ML"""
    response = client.get("/api/healthcheck")
    data = response.json()

    assert "ml_model" in data["components"]


{% endif -%}
{% if cookiecutter.use_ai_services == "yes" -%}
def test_healthcheck_includes_ai_api():
    """Test que verifica que el healthcheck incluye la API de IA"""
    response = client.get("/api/healthcheck")
    data = response.json()

    assert "ai_api" in data["components"]


{% endif -%}
{% if cookiecutter.use_database == "yes" -%}
def test_healthcheck_includes_database():
    """Test que verifica que el healthcheck incluye la base de datos"""
    response = client.get("/api/healthcheck")
    data = response.json()

    assert "database" in data["components"]


{% endif -%}
{% if cookiecutter.use_redis == "yes" -%}
def test_healthcheck_includes_redis():
    """Test que verifica que el healthcheck incluye Redis"""
    response = client.get("/api/healthcheck")
    data = response.json()

    assert "redis" in data["components"]
{% endif %}
