"""
Schemas para API de ML/IA (predicciones)
"""
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional, List
from datetime import datetime


class PredictionRequest(BaseModel):
    """Schema para solicitud de predicción"""
    data: Dict[str, Any] = Field(..., description="Datos de entrada para el modelo")
    model_version: Optional[str] = Field(None, description="Versión del modelo a usar")
    {% if cookiecutter.use_ai_services == "yes" -%}
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0, description="Temperatura para generación")
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000, description="Máximo de tokens")
    {% endif %}

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "feature1": 1.0,
                    "feature2": 2.5,
                    "feature3": "text input"
                },
                "model_version": "v1.0"
            }
        }


class PredictionResponse(BaseModel):
    """Schema para respuesta de predicción"""
    prediction: Any = Field(..., description="Resultado de la predicción")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confianza de la predicción")
    model_version: str = Field(..., description="Versión del modelo usado")
    timestamp: str = Field(..., description="Timestamp de la predicción")
    {% if cookiecutter.project_type == "ml_api" -%}
    probabilities: Optional[Dict[str, float]] = Field(None, description="Probabilidades por clase")
    {% endif %}

    class Config:
        json_schema_extra = {
            "example": {
                "prediction": "class_A",
                "confidence": 0.95,
                "model_version": "v1.0",
                "timestamp": "2024-01-01T10:00:00Z",
                {% if cookiecutter.project_type == "ml_api" -%}
                "probabilities": {
                    "class_A": 0.95,
                    "class_B": 0.05
                }
                {% endif %}
            }
        }


{% if cookiecutter.use_ai_services == "yes" -%}
class ChatMessage(BaseModel):
    """Schema para mensaje de chat"""
    role: str = Field(..., description="Rol del mensaje (system, user, assistant)")
    content: str = Field(..., description="Contenido del mensaje")


class ChatRequest(BaseModel):
    """Schema para solicitud de chat"""
    messages: List[ChatMessage] = Field(..., description="Historial de mensajes")
    model: Optional[str] = Field(None, description="Modelo a usar")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, ge=1, le=4000)

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "system", "content": "Eres un asistente útil"},
                    {"role": "user", "content": "¿Cuál es la capital de Francia?"}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }
        }


class ChatResponse(BaseModel):
    """Schema para respuesta de chat"""
    message: str = Field(..., description="Respuesta generada")
    model: str = Field(..., description="Modelo usado")
    timestamp: str = Field(..., description="Timestamp de la respuesta")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "La capital de Francia es París.",
                "model": "gpt-4o-mini",
                "timestamp": "2024-01-01T10:00:00Z"
            }
        }
{% endif %}
