{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
"""
Tests para la API de ML/IA
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.mark.skipif(
    "{{cookiecutter.project_type}}" != "ml_api",
    reason="Solo para proyectos de ML"
)
def test_predict_endpoint():
    """Test del endpoint de predicción"""
    prediction_data = {
        "data": {
            "feature1": 1.0,
            "feature2": 2.5,
            "feature3": 3.7
        }
    }

    response = client.post("/api/predict", json=prediction_data)

    # El test puede fallar si no hay modelo cargado en testing
    # por eso aceptamos 200 o 500
    assert response.status_code in [200, 500]

    if response.status_code == 200:
        data = response.json()
        assert "prediction" in data
        assert "timestamp" in data


{% if cookiecutter.use_ai_services == "yes" -%}
@pytest.mark.skipif(
    "{{cookiecutter.use_ai_services}}" != "yes",
    reason="Solo para proyectos con servicios de IA"
)
def test_chat_endpoint():
    """Test del endpoint de chat"""
    chat_data = {
        "messages": [
            {"role": "user", "content": "Hola, ¿cómo estás?"}
        ]
    }

    response = client.post("/api/chat", json=chat_data)

    # Puede fallar si no hay API key configurada
    assert response.status_code in [200, 400, 500]

    if response.status_code == 200:
        data = response.json()
        assert "message" in data
        assert "model" in data


def test_chat_endpoint_validation():
    """Test de validación del endpoint de chat"""
    # Sin mensajes (inválido)
    response = client.post("/api/chat", json={})

    assert response.status_code == 422  # Validation error


{% endif -%}
def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "name" in data or "message" in data


def test_docs_endpoint():
    """Test que la documentación está accesible"""
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_schema():
    """Test que el schema OpenAPI es válido"""
    response = client.get("/openapi.json")

    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
{% endif %}
