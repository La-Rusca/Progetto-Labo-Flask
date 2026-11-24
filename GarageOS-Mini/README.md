# GarageOS Mini

Sito fatto con Flask per salvare auto e spese. Ogni utente ha il proprio account e vede solo i propri dati.

## Avvio (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Nel file `.env` cambia `SECRET_KEY` con una chiave casuale. Per crearla:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Se `migrations/` esiste già, aggiorna il database:

```powershell
.\.venv\Scripts\python.exe -m flask --app app db migrate -m "aggiunta utenti"
.\.venv\Scripts\python.exe -m flask --app app db upgrade
```

Se non hai ancora la cartella `migrations/`, prima esegui:

```powershell
.\.venv\Scripts\python.exe -m flask --app app db init
```

Poi esegui `db migrate` e `db upgrade` come sopra.

Per avviare il sito:

```powershell
.\.venv\Scripts\python.exe app.py
```

Apri http://127.0.0.1:5000. Da lì puoi registrarti, accedere e aggiungere veicoli e spese.

## Nota sui dati vecchi

Se avevi già delle auto prima del login, quelle righe restano nel database ma non sono collegate a un utente e quindi non si vedono nei nuovi account. Puoi aggiungerle di nuovo. Non cancellare il database senza aver salvato i dati che ti servono.

## Test

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

Il file `.env` e il database locale non vanno caricati su GitHub; la cartella `migrations/` invece sì.
