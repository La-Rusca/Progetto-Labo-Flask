# GarageOS Mini

Un piccolo sito fatto con Python e Flask per gestire auto e spese.

## Cosa c'è adesso

- home
- pagina info
- stile css

## Come avviarlo (Windows)

Serve Python 3.11 o più recente.

Aprire il terminale nella cartella del progetto e scrivere:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Nel file `.env` bisogna sostituire `SECRET_KEY` con una chiave casuale. Si può creare così:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Per avviare:

```powershell
.\.venv\Scripts\python.exe app.py
```

Aprire `http://127.0.0.1:5000` nel browser.

## File

- `app.py`: le pagine gestite da Flask
- `templates/`: file html
- `static/`: file css
- `requirements.txt`: librerie da installare
- `.env.example`: esempio delle impostazioni

## Da aggiungere

Database, gestione delle auto, spese e utenti.
