#!/usr/bin/env python3
"""
Genera la página About (/about/) con el equipo.

Uso:
    python3 tools/build_about.py

Salida:
    about/index.html
    i18n/about.es.js

SOBRE EL NOMBRE DE LOS EMPLEADORES
----------------------------------
Ninguna de las dos biografías nombra a las empresas donde trabajaron. Es una
decisión conservadora, no un descuido:

- El empleador ACTUAL de Antonio es un tema abierto hasta que revise su contrato
  (exclusividad, no competencia, uso de marca). Nombrarlo en una página comercial
  se lee como cliente o como aval, que es distinto a listarlo en un CV.
- Nombrar solo a los empleadores pasados de Samuel dejaría una asimetría rara:
  cualquiera que ate cabos llega al mismo lugar.

Cuando el contrato esté revisado, cambiar esto es una línea por persona: busca
"NYSE-listed" y "two recognised adtech companies" abajo y sustituye por los
nombres. La estructura no cambia.

CONSENTIMIENTO
--------------
La foto y la biografía de Samuel son datos de un tercero. Antes de publicar,
consigue su visto bueno POR ESCRITO sobre el texto exacto y la imagen exacta.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://tu-dominio.com"
E = html.escape

PEOPLE = [
    {
        "slug": "antonio-garduno",
        "name": "Antonio Garduño",
        "role_en": "Founder · Technical Director",
        "role_es": "Fundador · Director técnico",
        "alt_en": "Portrait of Antonio Garduño",
        "alt_es": "Retrato de Antonio Garduño",
        "bio_en": [
            "Mechatronics engineer with roughly a decade of professional experience, nine years of it in project and program management. For the last three and a half years he has owned technical delivery for Fortune 500 accounts at a NYSE-listed ad-verification platform — coordinating engineering, product and client teams across the United States and international markets, and running root-cause analysis on live incidents with revenue attached to them.",
            "Before that: Scrum Master on four parallel software workstreams, project manager in consulting, and a first career running safety, quality and environmental programmes on industrial plant floors. That last one matters more than it sounds. Risk management stops being a spreadsheet exercise when a mistake has physical consequences, and a plant is where you learn to talk to the shop floor and to the board in the same week.",
            "He is a certified Gray Hat Web Penetration Tester and currently runs two live security engagements alongside the studio's build work. The through-line is the same across all of it: turn a business problem into a system that works, then hand it over.",
        ],
        "bio_es": [
            "Ingeniero mecatrónico con alrededor de una década de experiencia profesional, nueve años de ella en gestión de proyectos y programas. Los últimos tres años y medio ha sido dueño de la entrega técnica de cuentas Fortune 500 en una plataforma global de verificación publicitaria cotizada en NYSE — coordinando equipos de ingeniería, producto y cliente en Estados Unidos y mercados internacionales, y dirigiendo el análisis de causa raíz de incidentes en vivo con ingresos de por medio.",
            "Antes de eso: Scrum Master de cuatro flujos de software en paralelo, project manager en consultoría, y una primera carrera dirigiendo programas de seguridad, calidad y medio ambiente en piso de planta industrial. Esto último pesa más de lo que parece. La gestión de riesgos deja de ser un ejercicio de hoja de cálculo cuando un error tiene consecuencias físicas, y una planta es donde se aprende a hablar con el piso y con el consejo en la misma semana.",
            "Es Web Penetration Tester Gray Hat certificado y hoy lleva dos proyectos de seguridad vivos en paralelo al trabajo de construcción del estudio. El hilo conductor es el mismo en todo: convertir un problema de negocio en un sistema que funciona, y luego entregarlo.",
        ],
        "focus_en": ["Technical delivery", "Cybersecurity", "Program management", "Client leadership"],
        "focus_es": ["Entrega técnica", "Ciberseguridad", "Gestión de programas", "Liderazgo de cuentas"],
        "creds": [
            ("BEng Mechatronics", "Ingeniería Mecatrónica"),
            ("Certified Scrum Master — LearnQuest", "Scrum Master certificado — LearnQuest"),
            ("Google Project Management", "Gestión de Proyectos — Google"),
            ("Gray Hat Web Penetration Tester — American Council for Cybersecurity and Computer Forensics",
             "Web Penetration Tester Gray Hat — American Council for Cybersecurity and Computer Forensics"),
            ("Full-stack JavaScript &amp; Python", "Full-stack JavaScript y Python"),
            ("AI Agents: RAG &amp; LangChain", "Agentes de IA: RAG y LangChain"),
            ("Python — Pontificia Universidad Católica de Chile",
             "Python — Pontificia Universidad Católica de Chile"),
            ("Databases for Data Scientists — University of Colorado Boulder",
             "Bases de Datos para Científicos de Datos — Universidad de Colorado Boulder"),
            ("Disaster Risk Management — UNAM", "Gestión de Riesgo de Desastres — UNAM"),
            ("English C1 · Spanish native", "Inglés C1 · Español nativo"),
        ],
    },
    {
        "slug": "samuel-gonzalez",
        "name": "Samuel González",
        "role_en": "Software &amp; Automation Engineer",
        "role_es": "Ingeniero de software y automatización",
        "alt_en": "Portrait of Samuel González",
        "alt_es": "Retrato de Samuel González",
        "bio_en": [
            "Multiplatform software development engineer. He built at scale inside two recognised adtech companies — an industry measured in billions of events per day, where a competitor is always one release ahead. That environment teaches something specific: clever code nobody can operate is not an asset, it is a liability with good intentions.",
            "His work today is process automation with AI: bots, autonomous agents and n8n workflows, backed by the data engineering that makes them trustworthy. The emphasis is deliberately practical. Plenty of people can demonstrate what a model is capable of; the harder and more useful problem is making it change what a team actually does on Monday morning.",
        ],
        "bio_es": [
            "Ingeniero en Desarrollo de Software Multiplataforma. Construyó a escala dentro de dos empresas reconocidas de adtech — una industria que se mide en miles de millones de eventos al día, donde el competidor siempre va un release adelante. Ese entorno enseña algo concreto: el código ingenioso que nadie puede operar no es un activo, es un pasivo con buenas intenciones.",
            "Su trabajo hoy es la automatización de procesos con IA: bots, agentes autónomos y flujos de trabajo en n8n, respaldados por la ingeniería de datos que los hace confiables. El énfasis es deliberadamente práctico. Mucha gente puede demostrar de qué es capaz un modelo; el problema más difícil y más útil es lograr que cambie lo que un equipo realmente hace el lunes por la mañana.",
        ],
        "focus_en": ["AI agents", "Workflow automation (n8n)", "Data engineering", "Backend systems"],
        "focus_es": ["Agentes de IA", "Automatización de flujos (n8n)", "Ingeniería de datos", "Sistemas backend"],
        "creds": [
            ("BEng Multiplatform Software Development", "Ingeniería en Desarrollo de Software Multiplataforma"),
            ("Adtech engineering at scale", "Ingeniería adtech a escala"),
            ("n8n workflow automation", "Automatización de flujos con n8n"),
            ("Autonomous agents and bots", "Agentes autónomos y bots"),
            ("Data engineering for operations", "Ingeniería de datos para operaciones"),
        ],
    },
]

PRINCIPLES = [
    ("Scope in writing, before the work", "Alcance por escrito, antes del trabajo",
     "Every engagement states what is included, what is excluded and what you receive at the end. The exclusions are on the site precisely so the first call is about your problem instead of about ours.",
     "Cada proyecto declara qué incluye, qué excluye y qué recibes al final. Las exclusiones están publicadas justamente para que la primera llamada sea sobre tu problema y no sobre el nuestro."),
    ("Built to be handed over", "Hecho para entregarse",
     "Source code, documentation and credentials are yours from the first commit, and our access is revoked at closure. A supplier who makes you dependent has solved their problem, not yours.",
     "El código, la documentación y las credenciales son tuyos desde el primer commit, y nuestros accesos se revocan al cierre. Un proveedor que te vuelve dependiente resolvió su problema, no el tuyo."),
    ("Two seniors, not a pyramid", "Dos seniors, no una pirámide",
     "You get the people on this page. There is no layer of junior staff learning on your budget, and when a project needs more hands we tell you who is joining before they start.",
     "Trabajas con las personas de esta página. No hay una capa de gente junior aprendiendo con tu presupuesto, y cuando un proyecto necesita más manos te decimos quién entra antes de que empiece."),
]


def nav_html(cta="#contact"):
    return f"""  <div class="wrap">
    <a class="brand" href="/"><span class="monogram">TS</span><span>Technical Transformation Studio</span></a>
    <button class="burger" id="burger" aria-expanded="false" aria-controls="mainnav" aria-label="Open menu">☰</button>
    <nav class="mainnav" id="mainnav">
      <a href="/#practices" data-i18n="nav.practices">Practices</a>
      <a href="/work/" data-i18n="nav.work">Case studies</a>
      <a href="/about/" data-i18n="nav.about">About</a>
      <a href="/#cost" data-i18n="nav.cost">Cost</a>
      <a href="/#faq" data-i18n="nav.faq">FAQ</a>
      <label class="skip" for="langSelect" data-i18n="lang.label">Language</label>
      <select class="langpick" id="langSelect" hidden></select>
      <a class="cta-sm" href="{cta}" data-i18n="nav.cta">Book an assessment</a>
    </nav>
  </div>"""


def form_html():
    options = [
        ("Software Engineering", "form.o1", "Software Engineering"),
        ("AI &amp; Automation", "form.o2", "AI &amp; Automation"),
        ("Cybersecurity", "form.o3", "Cybersecurity"),
        ("Data &amp; Analytics", "form.o4", "Data &amp; Analytics"),
        ("Technical Delivery", "form.o5", "Technical Delivery &amp; Account Leadership"),
        ("Not sure yet", "form.o6", "Not sure yet"),
    ]
    opts = "\n".join(
        f'          <option value="{v}" data-i18n="{k}"{" selected" if v == "Not sure yet" else ""}>{l}</option>'
        for v, k, l in options
    )
    return """    <form class="form" id="contactForm" method="post" action="/api/contact" novalidate>
      <label><span data-i18n="form.company">Company</span><input name="company" required maxlength="120" autocomplete="organization" data-i18n-ph="form.ph.company" placeholder="Your company"></label>
      <label><span data-i18n="form.email">Work email</span><input type="email" name="email" required maxlength="254" autocomplete="email" data-i18n-ph="form.ph.email" placeholder="you@company.com"></label>
      <label><span data-i18n="form.practice">Practice</span><select name="practice">
""" + opts + """
      </select></label>
      <label><span data-i18n="form.problem">The problem</span><textarea name="message" rows="5" required maxlength="4000" data-i18n-ph="form.ph.message" placeholder="What are you trying to fix, build or protect?"></textarea></label>

      <div class="hp" aria-hidden="true"><label>Leave this field empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="rendered_at" id="renderedAt">

      <button type="submit" id="submitBtn" data-i18n="form.send">Send the brief</button>
      <p class="formstatus" id="formStatus" role="status" aria-live="polite"></p>
      <p class="formnote" data-i18n="form.note">We use your message to reply to you. Nothing else — no list, no third parties.</p>
    </form>"""


def person_html(i: int, p: dict) -> str:
    n = i + 1
    bio = "\n".join(
        f'        <p data-i18n="ab.p{n}b{j+1}">{E(t)}</p>' for j, t in enumerate(p["bio_en"])
    )
    focus = "".join(
        f'<span data-i18n="ab.p{n}f{j+1}">{f}</span>' for j, f in enumerate(p["focus_en"])
    )
    creds = "\n".join(
        f'          <li data-i18n="ab.p{n}c{j+1}">{c_en}</li>' for j, (c_en, c_es) in enumerate(p["creds"])
    )
    return f"""    <article class="person">
      <div class="person-photo">
        <picture>
          <source type="image/webp" srcset="/img/{p['slug']}-320.webp 320w, /img/{p['slug']}-640.webp 640w" sizes="(max-width:620px) 100vw, 320px">
          <img src="/img/{p['slug']}-320.jpg"
               srcset="/img/{p['slug']}-320.jpg 320w, /img/{p['slug']}-640.jpg 640w"
               sizes="(max-width:620px) 100vw, 320px"
               width="320" height="320" loading="lazy" decoding="async"
               alt="{p['alt_en']}" data-i18n-alt="ab.p{n}alt">
        </picture>
      </div>
      <div class="person-body">
        <h2 class="person-name">{p['name']}</h2>
        <p class="person-role" data-i18n="ab.p{n}role">{p['role_en']}</p>
{bio}
        <div class="pill-row">{focus}</div>
        <h3 class="creds-head" data-i18n="ab.p{n}ch">Credentials</h3>
        <ul class="creds">
{creds}
        </ul>
      </div>
    </article>"""


def build() -> str:
    people = "\n".join(person_html(i, p) for i, p in enumerate(PEOPLE))
    principles = "\n".join(
        f'      <div class="step"><b>{i+1:02d}</b>'
        f'<h3 data-i18n="ab.pr{i+1}t">{E(t_en)}</h3>'
        f'<p data-i18n="ab.pr{i+1}d">{E(d_en)}</p></div>'
        for i, (t_en, t_es, d_en, d_es) in enumerate(PRINCIPLES)
    )

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "AboutPage", "@id": DOMAIN + "/about/", "url": DOMAIN + "/about/",
             "name": "About — the people behind the studio"},
            {"@type": "Person", "@id": DOMAIN + "/about/#antonio", "name": "Antonio Garduño",
             "jobTitle": "Founder and Technical Director",
             "worksFor": {"@id": DOMAIN + "/#studio"},
             "image": DOMAIN + "/img/antonio-garduno-640.jpg",
             "knowsAbout": ["Technical program management", "Cybersecurity",
                            "Software engineering", "AI automation"],
             "address": {"@type": "PostalAddress", "addressLocality": "Santiago de Querétaro",
                         "addressCountry": "MX"}},
            {"@type": "Person", "@id": DOMAIN + "/about/#samuel", "name": "Samuel González",
             "jobTitle": "Software and Automation Engineer",
             "worksFor": {"@id": DOMAIN + "/#studio"},
             "image": DOMAIN + "/img/samuel-gonzalez-640.jpg",
             "knowsAbout": ["AI agents", "Workflow automation", "Data engineering",
                            "Software development"]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                {"@type": "ListItem", "position": 2, "name": "About", "item": DOMAIN + "/about/"}]},
        ],
    }

    return f"""<!doctype html>
<html lang="en" dir="ltr" data-i18n-page="about">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>About: The Two People Who Do the Work | Technical Transformation Studio</title>
<meta name="description" content="Antonio Garduño and Samuel González — a technical director with a decade in delivery, cybersecurity and program management, and a software engineer specialised in AI agents and workflow automation. Based in Querétaro, México.">

<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0E2439">

<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="canonical" href="{DOMAIN}/about/">
<link rel="alternate" hreflang="en" href="{DOMAIN}/about/">
<link rel="alternate" hreflang="es" href="{DOMAIN}/es/nosotros/">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/about/">
<meta property="og:type" content="website">
<meta property="og:title" content="The two people who do the work">
<meta property="og:description" content="A technical director and a software engineer. No pyramid, no junior layer learning on your budget.">
<meta property="og:url" content="{DOMAIN}/about/">
<meta property="og:image" content="{DOMAIN}/og/about.png">
<meta name="twitter:card" content="summary_large_image">

<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main" data-i18n="skip">Skip to content</a>

<header class="masthead">
{nav_html()}
</header>

<main id="main">
<section class="hero" id="top">
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="/" data-i18n="ab.crumbHome">Home</a>
        <span aria-hidden="true">/</span>
        <span data-i18n="ab.crumbSelf">About</span>
      </nav>
      <p class="kicker" data-i18n="ab.kicker">Who does the work</p>
      <h1><span data-i18n="ab.h1a">Two people, and</span> <em data-i18n="ab.h1b">both of them senior.</em></h1>
      <p class="deck" data-i18n="ab.deck">Most consultancies sell you a partner and staff the project with someone else. This page exists so you know exactly who shows up: two engineers, named, with the certifications and the scars to match.</p>
      <div class="btnrow">
        <a class="btn btn-fill" href="#contact" data-i18n="ab.cta1">Book a technical assessment</a>
        <a class="btn btn-line" href="/work/" data-i18n="ab.cta2">See what we have built</a>
      </div>
    </div>
    <div class="filecard">
      <h2 data-i18n="ab.cardHead">The studio</h2>
      <dl>
        <div class="filerow"><dt data-i18n="ab.k1">Based in</dt><dd data-i18n="ab.v1">Querétaro, México</dd></div>
        <div class="filerow"><dt data-i18n="ab.k2">Working languages</dt><dd>EN / ES</dd></div>
        <div class="filerow"><dt data-i18n="ab.k3">Team size</dt><dd data-i18n="ab.v3">Two, both senior</dd></div>
        <div class="filerow"><dt data-i18n="ab.k4">Delivery</dt><dd data-i18n="ab.v4">Remote, overlap hours agreed</dd></div>
        <div class="filerow"><dt data-i18n="ab.k5">Entry point</dt><dd data-i18n="ab.v5">Two-week assessment</dd></div>
      </dl>
      <p class="stamp" data-i18n="ab.stamp">You work with the people on this page.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
{people}
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="ab.prKicker">How we work</p>
      <h2 class="sect" data-i18n="ab.prH">Three commitments, and they are checkable.</h2>
    </div>
    <div class="ladder">
{principles}
    </div>
  </div>
</section>

<section class="band contact" id="contact">
  <div class="wrap">
    <div>
      <p class="kicker gold" data-i18n="con.kicker">Start here</p>
      <h2 class="sect" data-i18n="ab.conH">Tell us what is broken, slow or expensive.</h2>
      <div class="band-head"><p data-i18n="con.lead">Describe the problem in a few lines. You get a written reply with a first read on it, whether or not there is an engagement in it. The message is sent from this page — no email client, no third-party form service, no trackers.</p></div>
    </div>
{form_html()}
  </div>
</section>
</main>

<footer>
  <div class="wrap">
    <div>Technical Transformation Studio · Querétaro, México</div>
    <div>
      <a href="/legal/privacy/" data-i18n="footer.privacy">Privacy</a> ·
      <a href="/legal/terms/" data-i18n="footer.terms">Terms</a> ·
      <span id="year"></span>
    </div>
  </div>
</footer>

<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}
</script>

<script src="/i18n.js" defer></script>
<script src="/app.js" defer></script>
</body>
</html>
"""


def build_dict() -> str:
    d = {
        "ab.crumbHome": "Inicio",
        "ab.crumbSelf": "Nosotros",
        "ab.kicker": "Quién hace el trabajo",
        "ab.h1a": "Dos personas, y",
        "ab.h1b": "las dos senior.",
        "ab.deck": "Casi toda consultoría te vende un socio y luego asigna el proyecto a alguien más. Esta página existe para que sepas exactamente quién se presenta: dos ingenieros, con nombre, con las certificaciones y las cicatrices que lo respaldan.",
        "ab.cta1": "Agenda un diagnóstico técnico",
        "ab.cta2": "Ver lo que hemos construido",
        "ab.cardHead": "El estudio",
        "ab.k1": "Con base en", "ab.v1": "Querétaro, México",
        "ab.k2": "Idiomas de trabajo",
        "ab.k3": "Tamaño del equipo", "ab.v3": "Dos, ambos senior",
        "ab.k4": "Entrega", "ab.v4": "Remoto, con horas de traslape acordadas",
        "ab.k5": "Punto de entrada", "ab.v5": "Diagnóstico de dos semanas",
        "ab.stamp": "Trabajas con las personas de esta página.",
        "ab.prKicker": "Cómo trabajamos",
        "ab.prH": "Tres compromisos, y se pueden verificar.",
        "ab.conH": "Cuéntanos qué está roto, lento o caro.",
        "ab.backHome": "Volver al inicio",
    }
    for i, p in enumerate(PEOPLE):
        n = i + 1
        d[f"ab.p{n}role"] = p["role_es"]
        d[f"ab.p{n}alt"] = p["alt_es"]
        d[f"ab.p{n}ch"] = "Credenciales"
        for j, t in enumerate(p["bio_es"]):
            d[f"ab.p{n}b{j+1}"] = t
        for j, f in enumerate(p["focus_es"]):
            d[f"ab.p{n}f{j+1}"] = f
        for j, (c_en, c_es) in enumerate(p["creds"]):
            d[f"ab.p{n}c{j+1}"] = c_es
    for i, (t_en, t_es, d_en, d_es) in enumerate(PRINCIPLES):
        d[f"ab.pr{i+1}t"] = t_es
        d[f"ab.pr{i+1}d"] = d_es

    body = ",\n".join(f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}'
                      for k, v in d.items())
    return ('/* Español — página About. Generado por tools/build_about.py. */\n'
            f'window.ttsRegisterDictionary("es", {{\n{body}\n}});\n')


def main() -> None:
    (ROOT / "about").mkdir(exist_ok=True)
    (ROOT / "about" / "index.html").write_text(build(), encoding="utf-8")
    (ROOT / "i18n" / "about.es.js").write_text(build_dict(), encoding="utf-8")
    print("  about/index.html  +  i18n/about.es.js")


if __name__ == "__main__":
    main()
