from fastapi import FastAPI
from sqlalchemy.exc import OperationalError

from core import events
from main import get_application
import services.predict as predict


def test_preload_model(monkeypatch):
    called = {}

    def fake_get_model(cls, loader):
        called["called"] = True

    monkeypatch.setattr(
        predict.MachineLearningModelHandlerScore,
        "get_model",
        classmethod(fake_get_model),
    )
    events.preload_model()
    assert called.get("called") is True


def test_create_start_app_handler(monkeypatch):
    called = {}

    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    def fake_preload():
        called["called"] = True

    monkeypatch.setattr(events, "preload_model", fake_preload)
    {% endif -%}

    {% if cookiecutter.use_database == "yes" -%}
    def fake_create_all(*args, **kwargs):
        raise OperationalError("stmt", {}, Exception("db down"))

    monkeypatch.setattr(events.Base.metadata, "create_all", fake_create_all)
    {% endif %}
    app = FastAPI()
    handler = events.create_start_app_handler(app)
    handler()
    {% if cookiecutter.project_type in ["ml_api", "ai_rag_api"] -%}
    assert called.get("called") is True
    {% endif %}


def test_get_application():
    app = get_application()
    assert isinstance(app, FastAPI)
