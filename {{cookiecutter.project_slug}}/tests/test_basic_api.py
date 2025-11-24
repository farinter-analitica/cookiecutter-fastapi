{% if cookiecutter.project_type == "basic_api" -%}
"""
Tests para la API básica de tareas
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task():
    """Test para crear una nueva tarea"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "priority": 3
    }

    response = client.post("/api/tasks/", json=task_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
    assert "created_at" in data


def test_list_tasks():
    """Test para listar todas las tareas"""
    response = client.get("/api/tasks/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_task():
    """Test para obtener una tarea específica"""
    # Primero crear una tarea
    task_data = {
        "title": "Get Test Task",
        "description": "Task to test GET",
        "completed": False
    }
    create_response = client.post("/api/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Obtener la tarea
    response = client.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]


def test_update_task():
    """Test para actualizar una tarea"""
    # Crear tarea
    task_data = {
        "title": "Update Test Task",
        "completed": False
    }
    create_response = client.post("/api/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Actualizar tarea
    update_data = {
        "completed": True
    }
    response = client.put(f"/api/tasks/{task_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_delete_task():
    """Test para eliminar una tarea"""
    # Crear tarea
    task_data = {
        "title": "Delete Test Task"
    }
    create_response = client.post("/api/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Eliminar tarea
    response = client.delete(f"/api/tasks/{task_id}")

    assert response.status_code == 204

    # Verificar que no existe
    get_response = client.get(f"/api/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_task():
    """Test para obtener una tarea que no existe"""
    response = client.get("/api/tasks/99999")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
{% endif %}
