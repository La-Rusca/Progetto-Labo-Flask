import pytest
from app import app
from models import db, Utente, Veicolo


@pytest.fixture
def client(tmp_path):
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False,
                      SQLALCHEMY_DATABASE_URI=f"sqlite:///{tmp_path / 'test.db'}")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_registrazione_e_login(client):
    risposta = client.post("/registrazione", data={"username": "mario", "password": "password123"}, follow_redirects=True)
    assert risposta.status_code == 200
    assert b"mario" in risposta.data
    with app.app_context():
        assert Utente.query.count() == 1
        assert Utente.query.first().password != "password123"


def test_veicoli_privati(client):
    client.post("/registrazione", data={"username": "mario", "password": "password123"})
    client.post("/veicoli", data={"marca": "VW", "modello": "Golf", "anno": "2020"})
    client.post("/logout")
    client.post("/registrazione", data={"username": "luca", "password": "password123"})
    assert b"Golf" not in client.get("/veicoli").data
    with app.app_context():
        veicolo = Veicolo.query.first()
        assert veicolo is not None
        id = veicolo.id
    assert client.post(f"/veicoli/{id}/elimina").status_code == 404


def test_login_richiesto(client):
    assert client.get("/veicoli").status_code == 302
    assert "/login" in client.get("/veicoli").location
