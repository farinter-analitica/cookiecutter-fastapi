# cookiecutter-fastapi

Plantilla para crear proyectos FastAPI para el equipo de IA de Grupo Farinter. :rocket:

## Importante

Para usar este proyecto no necesitas hacer fork. ¡Solo ejecuta el CLI de cookiecutter y listo!

## Cookiecutter

Cookiecutter es una herramienta CLI (Interfaz de Línea de Comandos) para crear una estructura base de aplicación desde una plantilla. Utiliza un sistema de plantillas — Jinja2 — para reemplazar o personalizar nombres de carpetas y archivos, así como el contenido de los archivos.

### ¿Cómo instalo cookiecutter?

```bash
pip install cookiecutter
```

### ¿Cómo genero un proyecto FastAPI?

**Desde GitHub (recomendado para producción):**
```bash
cookiecutter https://github.com/farinter-analitica/cookiecutter-fastapi
```

**Desde repositorio local (para desarrollo):**
```bash
cd /ruta/al/repositorio
cookiecutter cookiecutter-fastapi
```

> **Nota:** Si has descargado el template antes, cookiecutter preguntará si deseas eliminarlo y re-descargarlo. Responde `y` para obtener la versión más reciente.

### Guía de respuestas para las preguntas

Durante la generación del proyecto, cookiecutter te hará varias preguntas. Aquí una guía:

#### Preguntas básicas
1. **project_name**: Nombre del proyecto (ej: "Mi API")
2. **project_slug**: Nombre técnico sin espacios (ej: "mi-api")
3. **project_short_description**: Descripción breve
4. **full_name**: Tu nombre completo
5. **email**: Tu correo electrónico
6. **version**: Versión inicial (default: "0.1.0")

#### Tipo de proyecto
7. **project_type**:
   - `basic_api`: API REST básica con endpoints CRUD
   - `ml_api`: API para modelos de Machine Learning
   - `ai_rag_api`: API para RAG (Retrieval Augmented Generation)

#### Base de datos
8. **use_database**: ¿Usar base de datos?
   - `yes`: Incluye SQLAlchemy y modelos
   - `no`: Sin base de datos
9. **database_type**: Tipo de base de datos (si elegiste `yes` arriba)
   - `postgresql`: PostgreSQL (recomendado)
   - `sqlserver`: SQL Server
   - `sqlite`: SQLite (solo para desarrollo)
   - `none`: Selecciona esto si pusiste `no` en use_database

#### Servicios de IA
10. **use_ai_services**: ¿Usar servicios de IA?
11. **ai_provider**: Proveedor de IA
    - `none`: Selecciona esto si pusiste `no` en use_ai_services
    - `openai`: OpenAI (GPT-4, GPT-3.5)
    - `gemini`: Google Gemini
    - `huggingface`: Hugging Face

#### Workers
12. **use_workers**: ¿Usar workers para tareas asíncronas?
13. **worker_type**: Tipo de worker
    - `none`: Selecciona esto si pusiste `no` en use_workers
    - `celery`: Celery (recomendado)
    - `rq`: Redis Queue

#### Almacenamiento
14. **use_storage**: ¿Usar almacenamiento de archivos?
15. **storage_type**: Tipo de almacenamiento
    - `none`: Selecciona esto si pusiste `no` en use_storage
    - `minio`: MinIO (S3-compatible)
    - `s3`: AWS S3
    - `local`: Almacenamiento local

#### Redis
16. **use_redis**: ¿Usar Redis para caché?

#### Configuración ML (solo si elegiste ml_api o ai_rag_api)
17. **machine_learn_model_path**: Ruta donde se guardará el modelo
18. **machine_learn_model_name**: Nombre del archivo del modelo
19. **input_example_path**: Ruta al archivo de ejemplo de entrada

### Ejemplos de configuración

#### API básica sin base de datos
```
project_type: basic_api
use_database: no
database_type: none
use_ai_services: no
ai_provider: none
use_workers: no
worker_type: none
use_storage: no
storage_type: none
use_redis: no
```

#### API de Machine Learning con PostgreSQL
```
project_type: ml_api
use_database: yes
database_type: postgresql
use_ai_services: no
ai_provider: none
use_workers: no
worker_type: none
use_storage: yes
storage_type: minio
use_redis: yes
```

#### API RAG con todos los servicios
```
project_type: ai_rag_api
use_database: yes
database_type: postgresql
use_ai_services: yes
ai_provider: openai
use_workers: yes
worker_type: celery
use_storage: yes
storage_type: s3
use_redis: yes
```