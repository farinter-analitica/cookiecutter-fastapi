"""
Schemas para API básica de tareas (TODO app)
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Schema base para tareas"""
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada")
    completed: bool = Field(default=False, description="Estado de completado")
    priority: Optional[int] = Field(default=1, ge=1, le=5, description="Prioridad (1-5)")


class TaskCreate(TaskBase):
    """Schema para crear nueva tarea"""
    pass


class TaskUpdate(BaseModel):
    """Schema para actualizar tarea existente"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[int] = Field(None, ge=1, le=5)


class TaskResponse(TaskBase):
    """Schema para respuesta de tarea"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Completar documentación",
                "description": "Escribir README y ejemplos",
                "completed": False,
                "priority": 3,
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00"
            }
        }
