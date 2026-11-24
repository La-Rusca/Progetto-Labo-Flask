
from uuid import uuid4
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:5000"


def registra_utente(pagina):
    nome = "test_" + uuid4().hex[:8]

    pagina.goto(URL + "/registrazione")
    pagina.locator('input[name="username"]').fill(nome)
    pagina.locator('input[name="password"]').fill("password123")
    pagina.get_by_role("button", name="Registrati").click()


    print("url:", pagina.url)
    print("messaggi:", pagina.locator("body").inner_text()[:800])


    assert pagina.url.rstrip("/") == URL
    return nome


def test_aggiunta_veicolo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        pagina = browser.new_page()

        registra_utente(pagina)

        # aggiungo un veicolo
        pagina.goto(URL + "/veicoli")
        pagina.locator('input[name="marca"]').fill("BMW")
        pagina.locator('input[name="modello"]').fill("Serie 1")
        pagina.locator('input[name="anno"]').fill("2020")
        pagina.get_by_role("button", name="Aggiungi veicolo").click()

        assert pagina.get_by_text("BMW Serie 1").is_visible()
        browser.close()


def test_login_logout():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        pagina = browser.new_page()

        nome = registra_utente(pagina)

        # esco e provo a rientrare
        pagina.get_by_role("button", name="Esci").click()
        assert "/login" in pagina.url

        pagina.locator('input[name="username"]').fill(nome)
        pagina.locator('input[name="password"]').fill("password123")
        pagina.get_by_role("button", name="Accedi").click()

        assert pagina.url.rstrip("/") == URL
        browser.close()


def test_aggiunta_spesa():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        pagina = browser.new_page()

        registra_utente(pagina)

        # prima creo un veicolo
        pagina.goto(URL + "/veicoli")
        pagina.locator('input[name="marca"]').fill("Fiat")
        pagina.locator('input[name="modello"]').fill("500")
        pagina.locator('input[name="anno"]').fill("2021")
        pagina.get_by_role("button", name="Aggiungi veicolo").click()

        # poi registro una spesa
        pagina.goto(URL + "/spese")
        pagina.locator('input[name="descrizione"]').fill("Benzina")
        pagina.locator('input[name="importo"]').fill("65.50")
        pagina.get_by_role("button", name="Aggiungi spesa").click()

        assert pagina.get_by_text("Benzina").is_visible()
        assert pagina.get_by_text("CHF 65.50").is_visible()

        browser.close()
