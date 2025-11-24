"""
Router para gestión de tareas (API básica)
"""
from fastapi import APIRouter, HTTPException, status{% if cookiecutter.use_database == "yes" %}, Depends
from sqlalchemy.orm import Session
from app.deps import get_db{% endif %}
from typing import List
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

{% if cookiecutter.use_database == "no" -%}
# Almacenamiento en memoria (solo para desarrollo)
tasks_db = []
task_id_counter = 1
{% endif %}


@router.get("/", response_model=List[TaskResponse], summary="Listar todas las tareas")
async def list_tasks(
    skip: int = 0,
    limit: int = 100{% if cookiecutter.use_database == "yes" %},
    db: Session = Depends(get_db){% endif %}
):
    """
    Obtiene la lista de todas las tareas con paginación.
    """
    {% if cookiecutter.use_database == "yes" -%}
    from app.models.task import Task
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks
    {% else -%}
    return tasks_db[skip : skip + limit]
    {% endif %}


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Crear nueva tarea")
async def create_task(
    task: TaskCreate{% if cookiecutter.use_database == "yes" %},
    db: Session = Depends(get_db){% endif %}
):
    """
    Crea una nueva tarea.
    """
    {% if cookiecutter.use_database == "yes" -%}
    from app.models.task import Task
    from datetime import datetime

    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        created_at=datetime.now()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
    {% else -%}
    global task_id_counter
    from datetime import datetime

    new_task = {
        "id": task_id_counter,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "priority": task.priority or 1,
        "created_at": datetime.now(),
        "updated_at": None
    }
    tasks_db.append(new_task)
    task_id_counter += 1
    return new_task
    {% endif %}


@router.get("/{task_id}", response_model=TaskResponse, summary="Obtener tarea por ID")
async def get_task(
    task_id: int{% if cookiecutter.use_database == "yes" %},
    db: Session = Depends(get_db){% endif %}
):
    """
    Obtiene una tarea específica por su ID.
    """
    {% if cookiecutter.use_database == "yes" -%}
    from app.models.task import Task

    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task
    {% else -%}
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task
    {% endif %}


@router.put("/{task_id}", response_model=TaskResponse, summary="Actualizar tarea")
async def update_task(
    task_id: int,
    task_update: TaskUpdate{% if cookiecutter.use_database == "yes" %},
    db: Session = Depends(get_db){% endif %}
):
    """
    Actualiza una tarea existente.
    """
    {% if cookiecutter.use_database == "yes" -%}
    from app.models.task import Task
    from datetime import datetime

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    # Actualizar solo campos proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.now()
    db.commit()
    db.refresh(db_task)
    return db_task
    {% else -%}
    from datetime import datetime

    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    # Actualizar solo campos proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        task[field] = value

    task["updated_at"] = datetime.now()
    return task
    {% endif %}


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar tarea")
async def delete_task(
    task_id: int{% if cookiecutter.use_database == "yes" %},
    db: Session = Depends(get_db){% endif %}
):
    """
    Elimina una tarea por su ID.
    """
    {% if cookiecutter.use_database == "yes" -%}
    from app.models.task import Task

    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    db.delete(db_task)
    db.commit()
    {% else -%}
    global tasks_db
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )

    tasks_db = [t for t in tasks_db if t["id"] != task_id]
    {% endif %}
