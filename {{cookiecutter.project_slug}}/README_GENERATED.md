# {{cookiecutter.project_name}}

{{cookiecutter.project_short_description}}

**Tipo de proyecto:** `{{cookiecutter.project_type}}`

---

## 🚀 Características

{% if cookiecutter.project_type == "basic_api" -%}
- ✅ API REST básica con FastAPI
- ✅ CRUD completo de tareas
{% elif cookiecutter.project_type == "ml_api" -%}
- 🤖 API para servir modelos de Machine Learning
- ✅ Predicciones con modelos entrenados
- ✅ Soporte para carga lazy de modelos
{% elif cookiecutter.project_type == "ai_rag_api" -%}
- 🧠 API para sistemas RAG (Retrieval-Augmented Generation)
- ✅ Integración con servicios de IA
- ✅ Embeddings y búsqueda semántica
{% endif %}
- ✅ Validación con Pydantic
- ✅ Configuración con variables de entorno
- ✅ Healthcheck robusto
{% if cookiecutter.use_database == "yes" -%}
- 🗄️ Base de datos: {{cookiecutter.database_type}}
{% endif %}
{% if cookiecutter.use_redis == "yes" -%}
- 📦 Redis para caché
{% endif %}
{% if cookiecutter.use_workers == "yes" -%}
- ⚙️ Workers asíncronos: {{cookiecutter.worker_type}}
{% endif %}
{% if cookiecutter.use_storage == "yes" -%}
- 💾 Almacenamiento: {{cookiecutter.storage_type}}
{% endif %}
{% if cookiecutter.use_ai_services == "yes" -%}
- 🤖 Proveedor de IA: {{cookiecutter.ai_provider}}
{% endif %}

---

## 📋 Requisitos

- Python 3.10+
- Docker y Docker Compose (opcional pero recomendado)
{% if cookiecutter.use_database == "yes" and cookiecutter.database_type == "postgresql" -%}
- PostgreSQL 15+ (si no usas Docker)
{% elif cookiecutter.use_database == "yes" and cookiecutter.database_type == "mysql" -%}
- MySQL 8.0+ (si no usas Docker)
{% endif %}
{% if cookiecutter.use_redis == "yes" -%}
- Redis 7+ (si no usas Docker)
{% endif %}

---

## 🛠️ Instalación

### Opción 1: Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd {{cookiecutter.project_slug}}

# 2. Copiar variables de entorno
cp env.example .env

# 3. Editar .env con tus credenciales
nano .env

# 4. Levantar servicios en modo desarrollo (con hot-reload)
docker-compose -f docker-compose.dev.yml up

# La API estará disponible en http://localhost:8000
# Documentación: http://localhost:8000/docs
```

### Opción 2: Instalación Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp env.example .env
nano .env

{% if cookiecutter.use_database == "yes" -%}
# 4. Inicializar base de datos
alembic upgrade head
{% endif %}

# 5. Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📚 Uso

### Endpoints Principales

{% if cookiecutter.project_type == "basic_api" -%}
#### Tareas (CRUD)

```bash
# Crear tarea
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi primera tarea",
    "description": "Descripción de la tarea",
    "priority": 3
  }'

# Listar tareas
curl http://localhost:8000/api/tasks/

# Obtener tarea por ID
curl http://localhost:8000/api/tasks/1

# Actualizar tarea
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Eliminar tarea
curl -X DELETE http://localhost:8000/api/tasks/1
```

{% elif cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
#### Predicciones

```bash
# Hacer predicción
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "feature1": 1.0,
      "feature2": 2.5
    }
  }'
```

{% if cookiecutter.use_ai_services == "yes" -%}
#### Chat con IA

```bash
# Enviar mensaje
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "¿Cuál es la capital de Francia?"}
    ]
  }'
```
{% endif %}
{% endif %}

#### Healthcheck

```bash
# Healthcheck completo
curl http://localhost:8000/api/healthcheck

# Liveness probe
curl http://localhost:8000/api/liveness

# Readiness probe
curl http://localhost:8000/api/readiness
```

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_api.py -v
```

---

## 📦 Estructura del Proyecto

```
{{cookiecutter.project_slug}}/
├── app/
│   ├── api/
│   │   └── routes/           # Routers de la API
│   ├── core/                 # Configuración y logging
│   ├── models/               # Modelos de BD (SQLAlchemy)
│   ├── schemas/              # Schemas Pydantic
│   ├── services/             # Lógica de negocio
{% if cookiecutter.use_workers == "yes" -%}
│   ├── workers/              # Tareas asíncronas
{% endif %}
│   ├── deps.py               # Dependencias compartidas
│   └── main.py               # Aplicación principal
├── tests/                    # Tests
{% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
├── ml/                       # Modelos y notebooks
{% endif %}
├── docker-compose.yml        # Docker Compose producción
├── docker-compose.dev.yml    # Docker Compose desarrollo
├── Dockerfile                # Imagen Docker
├── pyproject.toml            # Configuración del proyecto
└── README.md                 # Este archivo
```

---

## 🔧 Configuración

Todas las configuraciones se manejan vía variables de entorno en `.env`:

{% if cookiecutter.use_ai_services == "yes" -%}
### API Keys de IA

```bash
{% if cookiecutter.ai_provider == "openai" -%}
OPENAI_API_KEY=sk-...
{% elif cookiecutter.ai_provider == "anthropic" -%}
ANTHROPIC_API_KEY=sk-ant-...
{% elif cookiecutter.ai_provider == "huggingface" -%}
HUGGINGFACE_API_KEY=hf_...
{% endif %}
```
{% endif %}

{% if cookiecutter.use_database == "yes" -%}
### Base de Datos

```bash
DATABASE_URL={{cookiecutter.database_type}}://user:password@host:port/dbname
```
{% endif %}

---

## 🚢 Despliegue

### Docker (Producción)

```bash
# Build de la imagen
docker build -t {{cookiecutter.project_slug}}:latest .

# Run del contenedor
docker run -d \
  -p 8000:8000 \
  --env-file .env \
  --name {{cookiecutter.project_slug}} \
  {{cookiecutter.project_slug}}:latest
```

### Con Docker Compose

```bash
docker-compose up -d
```

---

## 📝 Licencia

[Especificar licencia]

---

## 👥 Autor

**{{cookiecutter.full_name}}** - {{cookiecutter.email}}

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**Generado con ❤️ usando cookiecutter-fastapi**
