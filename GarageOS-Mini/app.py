import os

from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chiave-solo-per-sviluppo")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/info")
def info():
    return render_template("info.html")


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
