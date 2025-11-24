"""
Servicio para integración con APIs de IA
"""
from typing import List, Dict, Any, Optional
from app.core.config import settings

{% if cookiecutter.ai_provider == "openai" -%}
from openai import OpenAI


class AIService:
    """Servicio para interactuar con OpenAI API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Genera respuesta usando chat completion.

        Args:
            messages: Lista de mensajes en formato OpenAI
            model: Modelo a usar (default: settings.DEFAULT_MODEL_CHAT)
            temperature: Temperatura de generación
            max_tokens: Máximo de tokens

        Returns:
            Respuesta generada
        """
        model = model or settings.DEFAULT_MODEL_CHAT

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def generate_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Genera embedding para un texto.

        Args:
            text: Texto a convertir en embedding
            model: Modelo de embedding (default: settings.DEFAULT_MODEL_EMB)

        Returns:
            Vector de embedding
        """
        model = model or settings.DEFAULT_MODEL_EMB

        response = self.client.embeddings.create(
            model=model,
            input=text
        )

        return response.data[0].embedding


{% elif cookiecutter.ai_provider == "gemini" -%}
import google.generativeai as genai


class AIService:
    """Servicio para interactuar con Google Gemini API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Genera respuesta usando chat completion.

        Args:
            messages: Lista de mensajes
            model: Modelo a usar
            temperature: Temperatura de generación
            max_tokens: Máximo de tokens

        Returns:
            Respuesta generada
        """
        model_name = model or settings.DEFAULT_MODEL_CHAT
        model = genai.GenerativeModel(model_name)

        # Convertir mensajes a formato Gemini
        chat_history = []
        system_instruction = None

        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            elif msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "model", "parts": [msg["content"]]})

        # Crear chat con configuración
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        if system_instruction:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )

        chat = model.start_chat(history=chat_history[:-1] if chat_history else [])

        # Enviar el último mensaje del usuario
        last_message = chat_history[-1]["parts"][0] if chat_history else ""
        response = chat.send_message(last_message, generation_config=generation_config)

        return response.text

    def generate_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Genera embedding para un texto.

        Args:
            text: Texto a convertir en embedding
            model: Modelo de embedding (default: settings.DEFAULT_MODEL_EMB)

        Returns:
            Vector de embedding
        """
        model_name = model or settings.DEFAULT_MODEL_EMB

        result = genai.embed_content(
            model=f"models/{model_name}",
            content=text,
            task_type="retrieval_document"
        )

        return result['embedding']


{% elif cookiecutter.ai_provider == "huggingface" -%}
from huggingface_hub import InferenceClient


class AIService:
    """Servicio para interactuar con HuggingFace API"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.HUGGINGFACE_API_KEY
        self.client = InferenceClient(token=self.api_key)

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Genera respuesta usando chat completion.

        Args:
            messages: Lista de mensajes
            model: Modelo a usar
            temperature: Temperatura de generación
            max_tokens: Máximo de tokens

        Returns:
            Respuesta generada
        """
        model = model or settings.DEFAULT_MODEL

        response = self.client.chat_completion(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content


{% else -%}
class AIService:
    """Servicio placeholder - No AI provider configured"""

    def __init__(self, api_key: Optional[str] = None):
        raise NotImplementedError("No AI provider configured")
{% endif %}


def get_ai_service(api_key: Optional[str] = None) -> AIService:
    """Factory function para crear instancias del servicio"""
    return AIService(api_key)
