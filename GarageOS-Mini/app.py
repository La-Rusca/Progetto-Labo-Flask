import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db, Utente, Veicolo, Spesa
from auth import auth

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "sviluppo")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///garageos.db")
db.init_app(app)
Migrate(app, db)
CSRFProtect(app)
app.register_blueprint(auth)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def carica_utente(id):
    return db.session.get(Utente, int(id))


@app.route("/")
@login_required
def home():
    auto = Veicolo.query.filter_by(user_id=current_user.id).all()
    spese = [spesa for veicolo in auto for spesa in veicolo.spese]
    return render_template("index.html", veicoli=len(auto),
                           numero_spese=len(spese), totale=sum(s.importo for s in spese))


@app.route("/veicoli", methods=["GET", "POST"])
@login_required
def veicoli():
    if request.method == "POST":
        marca = request.form.get("marca", "").strip()
        modello = request.form.get("modello", "").strip()
        anno = request.form.get("anno", "")
        if marca and modello and anno.isdigit() and 1900 <= int(anno) <= 2100:
            db.session.add(Veicolo(marca=marca, modello=modello, anno=int(anno), user_id=current_user.id))
            db.session.commit()
            return redirect(url_for("veicoli"))
    return render_template("veicoli.html", veicoli=Veicolo.query.filter_by(user_id=current_user.id).all())


@app.route("/veicoli/<int:id>/elimina", methods=["POST"])
@login_required
def elimina_veicolo(id):
    veicolo = Veicolo.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(veicolo)
    db.session.commit()
    return redirect(url_for("veicoli"))


@app.route("/spese", methods=["GET", "POST"])
@login_required
def spese():
    auto = Veicolo.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        descrizione = request.form.get("descrizione", "").strip()
        try:
            importo = float(request.form.get("importo", "0"))
            veicolo_id = int(request.form.get("veicolo_id", "0"))
        except ValueError:
            importo, veicolo_id = 0, 0
        if descrizione and 0 < importo < float("inf") and any(v.id == veicolo_id for v in auto):
            db.session.add(Spesa(descrizione=descrizione, importo=importo, veicolo_id=veicolo_id))
            db.session.commit()
            return redirect(url_for("spese"))
    spese_utente = [spesa for veicolo in auto for spesa in veicolo.spese]
    return render_template("spese.html", spese=spese_utente, veicoli=auto)


@app.route("/spese/<int:id>/elimina", methods=["POST"])
@login_required
def elimina_spesa(id):
    spesa = Spesa.query.join(Veicolo).filter(Spesa.id == id, Veicolo.user_id == current_user.id).first_or_404()
    db.session.delete(spesa)
    db.session.commit()
    return redirect(url_for("spese"))


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
