from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Utente(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Veicolo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modello = db.Column(db.String(50), nullable=False)
    anno = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("utente.id"))
    spese = db.relationship("Spesa", backref="veicolo", cascade="all, delete-orphan")


class Spesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descrizione = db.Column(db.String(100), nullable=False)
    importo = db.Column(db.Float, nullable=False)
    veicolo_id = db.Column(db.Integer, db.ForeignKey("veicolo.id"), nullable=False)
