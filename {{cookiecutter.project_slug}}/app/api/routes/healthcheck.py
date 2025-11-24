"""
Router de healthcheck y monitoreo del sistema
"""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.config import settings
import os

router = APIRouter()


@router.get("/healthcheck", summary="Healthcheck completo del sistema")
async def healthcheck():
    """
    Endpoint de healthcheck que valida componentes críticos del sistema
    """
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': settings.PROJECT_NAME,
        'version': settings.VERSION,
        'environment': settings.APP_ENV,
        'components': {}
    }

    all_healthy = True

    {% if cookiecutter.use_database == "yes" -%}
    # 1. Verificar base de datos
    try:
        from app.db import engine
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1")).scalar()

        health_status['components']['database'] = {
            'status': 'healthy',
            'type': '{{ cookiecutter.database_type }}',
            'message': 'Conexión exitosa'
        }
    except Exception as e:
        all_healthy = False
        health_status['components']['database'] = {
            'status': 'unhealthy',
            'type': '{{ cookiecutter.database_type }}',
            'error': str(e),
            'message': 'Error de conexión a la base de datos'
        }
    {% endif %}

    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    # 2. Verificar modelo ML
    try:
        model_exists = os.path.exists(settings.MODEL_PATH + settings.MODEL_NAME)
        health_status['components']['ml_model'] = {
            'status': 'healthy' if model_exists else 'unhealthy',
            'path': settings.MODEL_PATH + settings.MODEL_NAME,
            'exists': model_exists,
            'message': 'Modelo disponible' if model_exists else 'Modelo no encontrado'
        }
        if not model_exists:
            all_healthy = False
    except Exception as e:
        all_healthy = False
        health_status['components']['ml_model'] = {
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Error al verificar modelo'
        }
    {% endif %}

    {% if cookiecutter.use_ai_services == "yes" -%}
    # 3. Verificar API de IA
    try:
        {% if cookiecutter.ai_provider == "openai" -%}
        if settings.OPENAI_API_KEY:
            health_status['components']['ai_api'] = {
                'status': 'healthy',
                'provider': 'OpenAI',
                'message': 'API key configurada',
                'model_chat': settings.DEFAULT_MODEL_CHAT,
                'model_emb': settings.DEFAULT_MODEL_EMB
            }
        else:
            health_status['components']['ai_api'] = {
                'status': 'warning',
                'provider': 'OpenAI',
                'message': 'API key no configurada'
            }
        {% elif cookiecutter.ai_provider == "gemini" -%}
        if settings.GEMINI_API_KEY:
            health_status['components']['ai_api'] = {
                'status': 'healthy',
                'provider': 'Google Gemini',
                'message': 'API key configurada',
                'model_chat': settings.DEFAULT_MODEL_CHAT,
                'model_emb': settings.DEFAULT_MODEL_EMB
            }
        else:
            health_status['components']['ai_api'] = {
                'status': 'warning',
                'provider': 'Google Gemini',
                'message': 'API key no configurada'
            }
        {% endif %}
    except Exception as e:
        health_status['components']['ai_api'] = {
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Error al verificar servicio de IA'
        }
    {% endif %}

    {% if cookiecutter.use_redis == "yes" -%}
    # 4. Verificar Redis
    try:
        import redis
        redis_client = redis.from_url(settings.REDIS_URL, socket_connect_timeout=5)
        redis_client.ping()

        health_status['components']['redis'] = {
            'status': 'healthy',
            'message': 'Conexión exitosa',
            'url': settings.REDIS_URL
        }
    except Exception as e:
        all_healthy = False
        health_status['components']['redis'] = {
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Error de conexión a Redis'
        }
    {% endif %}

    {% if cookiecutter.use_storage == "yes" -%}
    # 5. Verificar almacenamiento
    try:
        {% if cookiecutter.storage_type == "minio" -%}
        import boto3
        s3_client = boto3.client(
            's3',
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY
        )
        s3_client.head_bucket(Bucket=settings.MINIO_BUCKET)

        health_status['components']['storage'] = {
            'status': 'healthy',
            'type': 'MinIO',
            'message': 'Bucket accesible',
            'bucket': settings.MINIO_BUCKET
        }
        {% elif cookiecutter.storage_type == "local" -%}
        storage_exists = os.path.exists(settings.UPLOAD_DIR)
        health_status['components']['storage'] = {
            'status': 'healthy' if storage_exists else 'warning',
            'type': 'Local',
            'path': settings.UPLOAD_DIR,
            'exists': storage_exists
        }
        {% endif %}
    except Exception as e:
        all_healthy = False
        health_status['components']['storage'] = {
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Error al verificar almacenamiento'
        }
    {% endif %}

    # Determinar estado general
    if not all_healthy:
        health_status['status'] = 'degraded'
        response_status = status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        response_status = status.HTTP_200_OK

    # Contar componentes por estado
    health_status['summary'] = {
        'healthy': sum(1 for c in health_status['components'].values() if c.get('status') == 'healthy'),
        'unhealthy': sum(1 for c in health_status['components'].values() if c.get('status') == 'unhealthy'),
        'warning': sum(1 for c in health_status['components'].values() if c.get('status') == 'warning'),
        'total': len(health_status['components'])
    }

    return JSONResponse(content=health_status, status_code=response_status)


@router.get("/liveness", summary="Liveness probe para Kubernetes/Docker")
async def liveness():
    """
    Endpoint de liveness que verifica que el servicio está vivo
    """
    return JSONResponse(
        content={
            'alive': True,
            'timestamp': datetime.now().isoformat(),
            'service': settings.PROJECT_NAME
        },
        status_code=status.HTTP_200_OK
    )


@router.get("/readiness", summary="Readiness probe para Kubernetes/Docker")
async def readiness():
    """
    Endpoint de readiness que verifica componentes críticos
    """
    is_ready = True
    checks = {}

    {% if cookiecutter.use_database == "yes" -%}
    # Verificar base de datos
    try:
        from app.db import engine
        from sqlalchemy import text

        with engine.connect() as connection:
            connection.execute(text("SELECT 1")).scalar()
        checks['database'] = True
    except Exception:
        checks['database'] = False
        is_ready = False
    {% endif %}

    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    # Verificar modelo
    try:
        model_exists = os.path.exists(settings.MODEL_PATH + settings.MODEL_NAME)
        checks['model'] = model_exists
        if not model_exists:
            is_ready = False
    except Exception:
        checks['model'] = False
        is_ready = False
    {% endif %}

    {% if cookiecutter.use_redis == "yes" -%}
    # Verificar Redis
    try:
        import redis
        redis_client = redis.from_url(settings.REDIS_URL, socket_connect_timeout=3)
        redis_client.ping()
        checks['redis'] = True
    except Exception:
        checks['redis'] = False
        is_ready = False
    {% endif %}

    return JSONResponse(
        content={'ready': is_ready, 'timestamp': datetime.now().isoformat(), 'checks': checks},
        status_code=status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE
    )
