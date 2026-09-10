"""
Pruebas del servidor. Cubren la API, el antispam y —importante— que el servidor de
estáticos NO sirva el código fuente ni la base de datos.

Correr desde la raíz del proyecto:
    source .venv/bin/activate
    pip install pytest
    pytest api/test_api.py -v

O sin pytest:
    python api/test_api.py
"""

import os
import sys
import time
from pathlib import Path

API_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(API_DIR))

os.environ.setdefault("DB_PATH", str(API_DIR / "test_leads.db"))
os.environ.setdefault("ADMIN_TOKEN", "")

from fastapi.testclient import TestClient  # noqa: E402
import main                                # noqa: E402

client = TestClient(main.app)


def brief(**overrides):
    payload = {
        "company": "ACME",
        "email": "hola@acme.com",
        "practice": "Cybersecurity",
        "message": "Necesitamos visibilidad de lo que exponemos a internet y un plan.",
        "website": "",
        "rendered_at": int((time.time() - 10) * 1000),
        "locale": "es",
    }
    payload.update(overrides)
    return payload


def reset_rate_limit():
    main._hits.clear()


# --------------------------------------------------------------------------
# Sitio estático
# --------------------------------------------------------------------------
def test_serves_index():
    r = client.get("/")
    assert r.status_code == 200
    assert "Technical Transformation Studio" in r.text


def test_serves_assets():
    for path in ("/styles.css", "/app.js", "/i18n.js", "/i18n/es.js"):
        assert client.get(path).status_code == 200, path


def test_spanish_dictionary_is_valid_js():
    body = client.get("/i18n/es.js").text
    assert body.startswith("/*") or "ttsRegisterDictionary" in body
    assert body.count("{") >= 1


def test_security_headers_present():
    headers = client.get("/").headers
    assert "Content-Security-Policy" in headers
    assert headers["X-Content-Type-Options"] == "nosniff"
    assert headers["X-Frame-Options"] == "DENY"


def test_source_code_is_not_downloadable():
    """El fallo clásico de servir la raíz del repo: código y secretos expuestos."""
    for path in (
        "/api/main.py",
        "/api/.env",
        "/api/.env.example",
        "/api/leads.db",
        "/api/requirements.txt",
        "/run.sh",
        "/.gitignore",
        "/assets/portraits/1-antonio.jpeg",
        "/tools/build_about.py",
        "/tests/frontend.check.js",
    ):
        assert client.get(path).status_code == 404, f"{path} NO debería servirse"


# --------------------------------------------------------------------------
# API de contacto
# --------------------------------------------------------------------------
def test_valid_submission():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief()).status_code == 201


def test_honeypot_is_silently_accepted():
    reset_rate_limit()
    r = client.post("/api/contact", json=brief(website="http://spam.example"))
    assert r.status_code == 201            # el bot no debe saber que fue detectado


def test_timetrap_rejects_instant_submission():
    reset_rate_limit()
    r = client.post("/api/contact", json=brief(rendered_at=int(time.time() * 1000)))
    assert r.status_code == 400


def test_unknown_practice_rejected():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief(practice="Hacking")).status_code == 422


def test_short_message_rejected():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief(message="hola")).status_code == 422


def test_bad_email_rejected():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief(email="no-es-correo")).status_code == 422


def test_oversized_message_rejected():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief(message="x" * 5000)).status_code == 422


def test_control_characters_rejected():
    reset_rate_limit()
    payload = brief(company="ACME\x00\x07 Corp")
    assert client.post("/api/contact", json=payload).status_code == 422


def test_unknown_locale_falls_back_to_english():
    reset_rate_limit()
    assert client.post("/api/contact", json=brief(locale="<script>")).status_code == 201


def test_rate_limit_kicks_in():
    reset_rate_limit()
    codes = [client.post("/api/contact", json=brief()).status_code for _ in range(7)]
    assert 429 in codes
    assert codes[: main.RATE_LIMIT_MAX] == [201] * main.RATE_LIMIT_MAX


def test_leads_endpoint_closed_without_token():
    assert client.get("/api/leads").status_code == 404


def test_openapi_docs_disabled():
    for path in ("/openapi.json", "/docs", "/redoc"):
        assert client.get(path).status_code == 404, path


def test_health():
    assert client.get("/api/health").json()["status"] == "ok"



# --------------------------------------------------------------------------
# Páginas de servicio
# --------------------------------------------------------------------------
SERVICE_SLUGS = [
    "software-engineering",
    "ai-automation",
    "cybersecurity",
    "data-analytics",
    "technical-delivery",
    "web-growth",
]


def test_service_pages_are_served():
    for slug in SERVICE_SLUGS:
        r = client.get(f"/services/{slug}/")
        assert r.status_code == 200, slug
        assert "<h1" in r.text, slug


def test_service_pages_have_unique_title_and_description():
    titles, descriptions = set(), set()
    for slug in SERVICE_SLUGS:
        body = client.get(f"/services/{slug}/").text
        title = body.split("<title>")[1].split("</title>")[0]
        desc = body.split('name="description" content="')[1].split('"')[0]
        assert title not in titles, f"título duplicado en {slug}"
        assert desc not in descriptions, f"description duplicada en {slug}"
        titles.add(title)
        descriptions.add(desc)


def test_service_pages_have_canonical_and_structured_data():
    for slug in SERVICE_SLUGS:
        body = client.get(f"/services/{slug}/").text
        assert f"/services/{slug}/" in body, slug
        assert 'rel="canonical"' in body, slug
        assert "BreadcrumbList" in body, slug
        assert '"@type":"Service"' in body, slug


def test_service_dictionaries_are_served():
    for slug in SERVICE_SLUGS:
        r = client.get(f"/i18n/{slug}.es.js")
        assert r.status_code == 200, slug
        assert "ttsRegisterDictionary" in r.text, slug


def test_home_links_to_every_service_page():
    home = client.get("/").text
    for slug in SERVICE_SLUGS:
        assert f'href="/services/{slug}/"' in home, slug


def test_sitemap_lists_every_page():
    body = client.get("/sitemap.xml").text
    # portada + 6 prácticas + índice de casos + 5 casos
    assert body.count("<url>") == 13
    for slug in SERVICE_SLUGS:
        assert f"/services/{slug}/" in body, slug


def test_build_script_is_not_downloadable():
    assert client.get("/tools/build_pages.py").status_code == 404



def test_pentest_scope_is_stated_consistently():
    """El pentesting se ofrece, pero SIEMPRE junto a su condición legal.
    Si alguien edita el copy y borra la autorización escrita, esto truena."""
    page = client.get("/services/cybersecurity/").text
    home = client.get("/").text
    for body, where in ((page, "página de ciberseguridad"), (home, "portada")):
        assert "penetration testing" in body.lower(), where
        assert "written authorisation" in body.lower(), where
    # Lo que queda fuera tiene que seguir declarado
    assert "red-team" in page.lower()
    assert "social engineering" in page.lower()



# --------------------------------------------------------------------------
# Casos de estudio
# --------------------------------------------------------------------------
CASE_SLUGS = [
    "cg-legal-phishing",
    "attack-surface-automation",
    "reporting-engine",
    "granelco",
    "aaif",
]


def test_case_index_and_pages_are_served():
    assert client.get("/work/").status_code == 200
    for slug in CASE_SLUGS:
        r = client.get(f"/work/{slug}/")
        assert r.status_code == 200, slug
        assert "<h1" in r.text, slug


def test_case_pages_have_unique_titles():
    titles = set()
    for slug in CASE_SLUGS:
        body = client.get(f"/work/{slug}/").text
        title = body.split("<title>")[1].split("</title>")[0]
        assert title not in titles, slug
        titles.add(title)


def test_case_dictionaries_are_served():
    assert client.get("/i18n/work-index.es.js").status_code == 200
    for slug in CASE_SLUGS:
        r = client.get(f"/i18n/case-{slug}.es.js")
        assert r.status_code == 200, slug
        assert "ttsRegisterDictionary" in r.text, slug


def test_every_case_states_its_consent_and_links_its_practice():
    """Ninguna cifra se publica sin decir bajo qué permiso, y cada caso
    devuelve tráfico a la práctica que lo vendió."""
    for slug in CASE_SLUGS:
        body = client.get(f"/work/{slug}/").text
        assert 'class="consent"' in body, slug
        assert 'href="/services/' in body, slug


def test_unnamed_client_stays_unnamed():
    """El cliente universitario pidió no ser nombrado. Si alguien lo agrega
    al copy por descuido, esto truena."""
    for path in ["/", "/work/", "/work/attack-surface-automation/",
                 "/services/cybersecurity/"]:
        body = client.get(path).text.lower()
        for forbidden in ("buap", "benemérita", "benemerita", "puebla"):
            assert forbidden not in body, f"{forbidden} aparece en {path}"


def test_case_index_links_every_case():
    body = client.get("/work/").text
    for slug in CASE_SLUGS:
        assert f'href="/work/{slug}/"' in body, slug


def test_sitemap_includes_cases():
    body = client.get("/sitemap.xml").text
    assert "/work/</loc>" in body
    for slug in CASE_SLUGS:
        assert f"/work/{slug}/" in body, slug



def test_no_inline_styles_anywhere():
    """Un atributo style= viola style-src 'self': el navegador lo bloquea, el
    estilo no se aplica y quedan errores en consola. Los estilos van en CSS."""
    paths = ["/", "/work/"]
    paths += [f"/services/{s}/" for s in SERVICE_SLUGS]
    paths += [f"/work/{s}/" for s in CASE_SLUGS]
    for path in paths:
        body = client.get(path).text
        assert 'style="' not in body, f"estilo inline en {path}"
        assert "onclick=" not in body, f"handler inline en {path}"



# --------------------------------------------------------------------------
# Iconos
# --------------------------------------------------------------------------
def test_favicon_files_are_served():
    """El navegador pide /favicon.ico aunque nadie lo enlace. Sin archivo,
    cada visita deja un 404 en la consola y en los logs del servidor."""
    for path, content_type in [
        ("/favicon.ico", "image"),
        ("/favicon.svg", "image/svg"),
        ("/apple-touch-icon.png", "image/png"),
        ("/icon-192.png", "image/png"),
        ("/icon-512.png", "image/png"),
        ("/site.webmanifest", None),
    ]:
        r = client.get(path)
        assert r.status_code == 200, path
        if content_type:
            assert content_type in r.headers.get("content-type", ""), path


def test_every_page_links_the_icons():
    paths = ["/", "/work/"]
    paths += [f"/services/{s}/" for s in SERVICE_SLUGS]
    paths += [f"/work/{s}/" for s in CASE_SLUGS]
    for path in paths:
        body = client.get(path).text
        assert 'href="/favicon.svg"' in body, path
        assert 'href="/favicon.ico"' in body, path
        assert 'rel="apple-touch-icon"' in body, path



# --------------------------------------------------------------------------
# About, legal, imágenes sociales y avisos
# --------------------------------------------------------------------------
def test_about_page_is_served_with_both_people():
    body = client.get("/about/").text
    assert "Antonio Garduño" in body
    assert "Samuel González" in body
    assert client.get("/i18n/about.es.js").status_code == 200


def test_portraits_are_served_in_both_formats():
    for slug in ("antonio-garduno", "samuel-gonzalez"):
        for width in (320, 640):
            for ext in ("jpg", "webp"):
                r = client.get(f"/img/{slug}-{width}.{ext}")
                assert r.status_code == 200, f"{slug}-{width}.{ext}"


def test_portraits_have_alt_and_dimensions():
    """Sin width/height la página salta al cargar la imagen (CLS), y sin alt
    no hay nada que leer para quien usa lector de pantalla."""
    body = client.get("/about/").text
    assert body.count("<img") == 3
    assert body.count('width="320" height="320"') == 3
    assert body.count("alt=\"Portrait of") == 3
    assert body.count('loading="lazy"') == 3


def test_legal_pages_are_served():
    for path in ("/legal/privacy/", "/legal/terms/"):
        r = client.get(path)
        assert r.status_code == 200, path
        assert "<h1" in r.text, path


def test_every_page_links_the_legal_pages():
    paths = ["/", "/work/", "/about/"]
    paths += [f"/services/{s}/" for s in SERVICE_SLUGS]
    paths += [f"/work/{s}/" for s in CASE_SLUGS]
    for path in paths:
        body = client.get(path).text
        assert 'href="/legal/privacy/"' in body, path
        assert 'href="/legal/terms/"' in body, path


def test_privacy_notice_matches_what_the_site_actually_does():
    """Si algún día se agrega analítica o cookies, esta prueba debe fallar
    antes de que el aviso de privacidad se vuelva mentira."""
    privacy = client.get("/legal/privacy/").text.lower()
    assert "no cookies" in privacy
    for path in ["/", "/about/", "/work/"]:
        body = client.get(path).text.lower()
        assert "document.cookie" not in body
        assert "localstorage" not in body
        assert "googletagmanager" not in body
        assert "google-analytics" not in body


def test_every_page_has_an_og_image():
    paths = ["/", "/work/", "/about/", "/legal/privacy/", "/legal/terms/"]
    paths += [f"/services/{s}/" for s in SERVICE_SLUGS]
    paths += [f"/work/{s}/" for s in CASE_SLUGS]
    for path in paths:
        body = client.get(path).text
        assert 'property="og:image"' in body, path
        og = body.split('property="og:image" content="')[1].split('"')[0]
        local = og.replace("https://tu-dominio.com", "")
        assert client.get(local).status_code == 200, f"{path} apunta a {local}"


def test_notifications_are_off_by_default_and_never_block():
    """Sin configurar, no se intenta nada. Y el envío va en BackgroundTasks:
    el visitante no espera a Telegram ni al SMTP."""
    assert main.NOTIFY_CHANNEL in ("none", "")
    assert main.send_webhook(brief_model()) is False
    import inspect
    source = inspect.getsource(main.contact)
    assert "background.add_task" in source


def brief_model():
    return main.ContactRequest(**brief())



def test_gold_on_paper_meets_wcag_aa():
    """El dorado se usa en textos de 10–12 px sobre papel. Si alguien lo aclara
    para que "se vea más bonito", el sitio deja de cumplir AA en contraste y
    Lighthouse lo marca. Esta prueba fija el piso."""
    css = client.get("/styles.css").text
    gold = css.split("--gold:")[1].split(";")[0].strip()
    paper = css.split("--paper:")[1].split(";")[0].strip()

    def luminance(hex_colour):
        hex_colour = hex_colour.lstrip("#")
        channels = [int(hex_colour[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        adjusted = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
                    for c in channels]
        return 0.2126 * adjusted[0] + 0.7152 * adjusted[1] + 0.0722 * adjusted[2]

    a, b = luminance(gold), luminance(paper)
    contrast = (max(a, b) + 0.05) / (min(a, b) + 0.05)
    assert contrast >= 4.5, f"--gold {gold} sobre --paper {paper} da {contrast:.2f}:1"


if __name__ == "__main__":
    passed = failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"  ok    {name}")
                passed += 1
            except AssertionError as exc:
                print(f"  FALLA {name}: {exc}")
                failed += 1
    Path(os.environ["DB_PATH"]).unlink(missing_ok=True)
    print(f"\n{passed} pasaron, {failed} fallaron")
    sys.exit(1 if failed else 0)
