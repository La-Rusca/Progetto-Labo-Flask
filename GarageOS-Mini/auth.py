from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Utente

auth = Blueprint("auth", __name__)


@auth.route("/registrazione", methods=["GET", "POST"])
def registrazione():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if len(username) < 3 or len(password) < 8:
            flash("nome di almeno 3 caratteri e password di almeno 8")
        elif Utente.query.filter_by(username=username).first():
            flash("questo nome utente esiste già")
        else:
            utente = Utente(username=username, password=generate_password_hash(password))
            db.session.add(utente)
            db.session.commit()
            login_user(utente)
            return redirect(url_for("home"))
    return render_template("registrazione.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        utente = Utente.query.filter_by(username=request.form.get("username", "").strip()).first()
        if utente and check_password_hash(utente.password, request.form.get("password", "")):
            login_user(utente)
            return redirect(url_for("home"))
        flash("nome utente o password sbagliati")
    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
