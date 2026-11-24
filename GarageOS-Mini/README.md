# GarageOS Mini

GarageOS Mini è un'applicazione web fatta con Python e Flask per gestire le auto e le relative spese.

## Funzionalità

- registrazione, login e logout
- aggiunta ed eliminazione dei veicoli
- registrazione ed eliminazione delle spese
- riepilogo delle spese nella home
- ogni utente vede solo i propri dati

## Installazione (Windows)

Aprire un terminale nella cartella `GarageOS-Mini`.

Creare l'ambiente virtuale e installare le librerie:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copiare `.env.example` in `.env`:

```powershell
Copy-Item .env.example .env
```

Generare una chiave segreta:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Inserire la chiave generata come valore di `SECRET_KEY` nel file `.env`.

## Database

Per creare le tabelle usando le migrazioni già presenti:

```powershell
.\.venv\Scripts\python.exe -m flask --app app db upgrade
```

Le migrazioni sono nella cartella `migrations/`.

## Avvio

```powershell
.\.venv\Scripts\python.exe app.py
```

Aprire `http://127.0.0.1:5000` nel browser.

## Test

### Pytest

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_app.py -v
```

### Playwright

Installare Chromium (solo la prima volta):

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

Per non usare i dati normali dell'app, i test Playwright si eseguono con un database separato. Prima fermare gli eventuali server Flask già avviati.

Nel **primo terminale PowerShell**:

```powershell
$env:DATABASE_URL = "sqlite:///garageos_playwright.db"
.\.venv\Scripts\python.exe -c "from app import app; from models import db; ctx = app.app_context(); ctx.push(); db.create_all(); ctx.pop()"
.\.venv\Scripts\python.exe app.py
```

Lasciare aperto il primo terminale. Nel **secondo terminale**:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_browser.py -v
```

Questi test simulano alcune operazioni nel browser, come registrarsi, accedere e aggiungere dati.
