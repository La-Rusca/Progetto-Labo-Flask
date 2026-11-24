
import pytest
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from app import app as app_principale
from auth import auth
from models import db, Utente


@pytest.fixture
def client(tmp_path):
    app = Flask(
    __name__,
    template_folder=str(__import__("pathlib").Path(__file__).resolve().parent.parent / "templates")
)
    app.config.update(
        TESTING=True,
        SECRET_KEY="chiave-test",
        WTF_CSRF_ENABLED=False,
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}"
    )

    db.init_app(app)
    CSRFProtect(app)
    app.register_blueprint(auth)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def carica_utente(id):
        return db.session.get(Utente, int(id))

    # uso le route del progetto anche nei test
    for regola in app_principale.url_map.iter_rules():
        if regola.endpoint in ("static",) or regola.endpoint.startswith("auth."):
            continue
        funzione = app_principale.view_functions[regola.endpoint]
        app.add_url_rule(
            regola.rule,
            endpoint=regola.endpoint,
            view_func=funzione,
            methods=list(regola.methods)
        )

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()


def test_login_richiesto(client):
    risposta = client.get("/veicoli")

    assert risposta.status_code == 302
    assert "/login" in risposta.location


def test_registrazione(client):
    risposta = client.post("/registrazione", data={
        "username": "mario",
        "password": "password123"
    })

    assert risposta.status_code == 302

    with client.application.app_context():
        assert Utente.query.count() == 1
        assert Utente.query.first().password != "password123"


def test_aggiunta_veicolo(client):
    client.post("/registrazione", data={
        "username": "mario",
        "password": "password123"
    })

    client.post("/veicoli", data={
        "marca": "BMW",
        "modello": "Serie 1",
        "anno": "2020"
    })

    risposta = client.get("/veicoli")

    assert b"BMW" in risposta.data
    assert b"Serie 1" in risposta.data
