"""
Servicio para manejar inferencias del modelo ML
"""
from typing import Any, Dict, Optional
import joblib
from app.core.config import settings


class MLService:
    """Servicio para carga y predicción con modelos de ML"""

    def __init__(self):
        self.model = None
        self.model_path = settings.MODEL_PATH
        self.model_name = settings.MODEL_NAME

    def load_model(self):
        """Carga el modelo ML desde disco"""
        if not self.model:
            full_path = f"{self.model_path}{self.model_name}"
            self.model = joblib.load(full_path)
            print(f"✓ Modelo cargado: {full_path}")
        return self.model

    def predict(self, data: Dict[str, Any]) -> Any:
        """
        Realiza predicción con el modelo cargado.

        Args:
            data: Diccionario con los datos de entrada

        Returns:
            Resultado de la predicción
        """
        model = self.load_model()

        # Aquí personaliza según tu modelo
        # Ejemplo para sklearn:
        # features = [data['feature1'], data['feature2'], ...]
        # prediction = model.predict([features])

        prediction = model.predict(data)
        return prediction

    def predict_proba(self, data: Dict[str, Any]) -> Optional[Any]:
        """
        Retorna probabilidades de predicción (si el modelo lo soporta).

        Args:
            data: Diccionario con los datos de entrada

        Returns:
            Probabilidades de cada clase
        """
        model = self.load_model()

        if hasattr(model, 'predict_proba'):
            return model.predict_proba(data)

        return None


def get_ml_service() -> MLService:
    """Factory function para crear instancias del servicio"""
    return MLService()
