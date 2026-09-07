#!/usr/bin/env python3
"""
Genera las páginas de caso a partir del contenido definido aquí abajo.

Misma lógica que tools/build_pages.py: el contenido vive en un solo lugar, con el
inglés y el español juntos, y el HTML se regenera.

Uso:
    python3 tools/build_cases.py

Salida:
    work/index.html                 índice de casos
    work/<slug>/index.html          una página por caso
    i18n/case-<slug>.es.js          diccionario español de cada caso
    i18n/work-index.es.js

REGLA DE HONESTIDAD DE ESTE ARCHIVO
-----------------------------------
Cada cifra publicada aquí viene del cliente. Ninguna se redondea hacia arriba,
ninguna se anualiza sin decir que está anualizada, y donde no hubo medición se
dice "no se midió" en vez de inventar un porcentaje. Si mañana un prospecto
pregunta de dónde salió un número, la respuesta tiene que existir.

Consentimiento: CG Legal & Real Estate Consulting aparece con nombre. La
universidad NO se nombra por decisión del cliente. El cliente final afectado por
la campaña de phishing nunca se nombra, ni se describen los detalles técnicos que
permitirían repetir el ataque.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://tu-dominio.com"

E = html.escape

CASES = [
    {
        "slug": "cg-legal-phishing",
        "practice": "cybersecurity",
        "kicker_en": "Cybersecurity · Named client",
        "kicker_es": "Ciberseguridad · Cliente con nombre",
        "client_en": "CG Legal &amp; Real Estate Consulting",
        "client_es": "CG Legal &amp; Real Estate Consulting",
        "title_en": "Phishing and Impersonation Takedown: Two Live Campaigns Stopped in Three Days",
        "title_es": "Desactivación de phishing y suplantación: dos campañas activas detenidas en tres días",
        "desc_en": "A law firm was being impersonated for over a month. One day of analysis found seven hidden assets behind a single domain; three days later the infrastructure was down.",
        "desc_es": "Un despacho legal llevaba más de un mes siendo suplantado. Un día de análisis encontró siete activos ocultos detrás de un solo dominio; tres días después la infraestructura estaba dada de baja.",
        "h1_en": "A month of impersonation, ended in three days",
        "h1_es": "Un mes de suplantación, terminado en tres días",
        "deck_en": "Two active phishing campaigns were running against a law firm's client from a single impersonation domain. Nobody had found the infrastructure behind it. Analysis took one day; takedown took three.",
        "deck_es": "Dos campañas activas de phishing corrían contra el cliente de un despacho legal desde un solo dominio de suplantación. Nadie había encontrado la infraestructura detrás. El análisis tomó un día; la baja, tres.",
        "meta": [
            ("Client", "Cliente", "CG Legal &amp; Real Estate", "CG Legal &amp; Real Estate"),
            ("Practice", "Práctica", "Cybersecurity", "Ciberseguridad"),
            ("Analysis", "Análisis", "1 day", "1 día"),
            ("Takedown", "Baja", "3 days", "3 días"),
            ("Exposure before", "Exposición previa", "Over 1 month", "Más de 1 mes"),
        ],
        "situation_h_en": "The attack had been running for over a month",
        "situation_h_es": "El ataque llevaba más de un mes corriendo",
        "situation_p1_en": "A legal and real-estate consultancy discovered that someone was impersonating the firm to target one of its clients. Two separate phishing campaigns were live, and they had been running for more than a month before anyone connected them to a single source.",
        "situation_p1_es": "Una consultoría legal e inmobiliaria descubrió que alguien estaba suplantando al despacho para atacar a uno de sus clientes. Dos campañas de phishing distintas estaban activas, y llevaban más de un mes corriendo antes de que alguien las conectara con una sola fuente.",
        "situation_p2_en": "The firm's real exposure was wider than the incident in front of them. The same infrastructure could be pointed at any client on their book, and a duplicated campaign against a second client would have looked identical from the outside — which is the difference between an incident and a pattern.",
        "situation_p2_es": "La exposición real del despacho era más amplia que el incidente que tenían enfrente. La misma infraestructura podía apuntarse a cualquier cliente de su cartera, y una campaña duplicada contra un segundo cliente se habría visto idéntica desde fuera — que es la diferencia entre un incidente y un patrón.",
        "did": [
            ("Traced both campaigns to one origin", "Rastrear ambas campañas a un solo origen",
             "The two campaigns looked separate. One day of analysis established that both came from the same impersonation domain, which changed the problem from two incidents into one piece of infrastructure.",
             "Las dos campañas parecían separadas. Un día de análisis estableció que ambas venían del mismo dominio de suplantación, lo que convirtió el problema de dos incidentes en una sola pieza de infraestructura."),
            ("Mapped the hidden assets", "Mapear los activos ocultos",
             "Behind the visible domain sat seven further assets holding the campaign up. None of them were known to the client. Taking down only what was visible would have left the operation intact.",
             "Detrás del dominio visible había siete activos más sosteniendo la campaña. Ninguno era conocido por el cliente. Dar de baja solo lo visible habría dejado la operación intacta."),
            ("Escalated to the authorities", "Escalar con las autoridades",
             "Once the origin was documented, the case was escalated to the relevant authorities with the evidence organised for them rather than handed over raw.",
             "Una vez documentado el origen, el caso se escaló con las autoridades correspondientes, con la evidencia organizada para ellas y no entregada en crudo."),
            ("Left monitoring behind", "Dejar el monitoreo instalado",
             "A monitoring platform now watches for domain changes and new registrations, polling every ten seconds, so a duplicated campaign surfaces in seconds rather than after a month.",
             "Una plataforma de monitoreo vigila ahora los cambios de dominio y los registros nuevos, consultando cada diez segundos, para que una campaña duplicada aparezca en segundos y no después de un mes."),
        ],
        "metrics": [
            ("7", "hidden assets found behind one domain", "activos ocultos detrás de un dominio"),
            ("0", "of them known to the client beforehand", "de ellos conocidos antes por el cliente"),
            ("1 day", "from engagement to identified origin", "de arranque a origen identificado"),
            ("3 days", "from identification to takedown", "de identificación a baja del objetivo"),
        ],
        "lesson_h_en": "What this case actually shows",
        "lesson_h_es": "Qué demuestra realmente este caso",
        "lesson_en": "The month of exposure was not a detection failure by the firm — it was the absence of anyone looking. The seven unknown assets are the point: an organisation cannot defend a surface it has never been shown, and the visible domain was the smallest part of the problem. That is why the cybersecurity practice starts with discovery before it starts with fixing.",
        "lesson_es": "El mes de exposición no fue una falla de detección del despacho: fue la ausencia de alguien mirando. Los siete activos desconocidos son el punto: una organización no puede defender una superficie que nunca le han mostrado, y el dominio visible era la parte más pequeña del problema. Por eso la práctica de ciberseguridad empieza por descubrir antes que por arreglar.",
        "consent_en": "Published with the client's authorisation. The end client targeted by the campaign is not named, and no technical detail that would help reproduce the attack is included.",
        "consent_es": "Publicado con autorización del cliente. El cliente final atacado por la campaña no se nombra, y no se incluye ningún detalle técnico que ayude a reproducir el ataque.",
        "stack": "DNS · Certificate transparency · OSINT · Monitoring · Alerting",
    },
    {
        "slug": "attack-surface-automation",
        "practice": "cybersecurity",
        "kicker_en": "Cybersecurity · Public university",
        "kicker_es": "Ciberseguridad · Universidad pública",
        "client_en": "One of Mexico's largest public universities",
        "client_es": "Una de las universidades públicas más grandes de México",
        "title_en": "Attack Surface Assessment Automated: From Twelve Hours of Manual Analysis to Eight Minutes per Subdomain",
        "title_es": "Evaluación de superficie de ataque automatizada: de doce horas de análisis manual a ocho minutos por subdominio",
        "desc_en": "A full infrastructure assessment took twelve hours of continuous manual analysis. Automating it brought each subdomain down to about eight minutes and the full sweep from days to hours.",
        "desc_es": "Una evaluación completa de infraestructura tomaba doce horas de análisis manual continuo. Automatizarla bajó cada subdominio a unos ocho minutos y el barrido completo de días a horas.",
        "h1_en": "The assessment that used to take days now runs in hours",
        "h1_es": "La evaluación que tomaba días ahora corre en horas",
        "deck_en": "A public university with a large, sprawling estate needed its external infrastructure assessed — and then reassessed, repeatedly. Doing that by hand does not scale. Automating it changed the unit of work from the whole estate to a single subdomain.",
        "deck_es": "Una universidad pública con una infraestructura grande y dispersa necesitaba evaluar su superficie externa — y volver a evaluarla, una y otra vez. Hacerlo a mano no escala. Automatizarlo cambió la unidad de trabajo de toda la infraestructura a un solo subdominio.",
        "meta": [
            ("Client", "Cliente", "Public university (unnamed)", "Universidad pública (sin nombrar)"),
            ("Practice", "Práctica", "Cybersecurity", "Ciberseguridad"),
            ("Scope", "Alcance", "Full external infrastructure", "Infraestructura externa completa"),
            ("Before", "Antes", "12 h continuous manual analysis", "12 h de análisis manual continuo"),
            ("After", "Después", "~8 min per subdomain", "~8 min por subdominio"),
        ],
        "situation_h_en": "A security assessment you can only afford to run once is not a security programme",
        "situation_h_es": "Una evaluación de seguridad que solo puedes correr una vez no es un programa de seguridad",
        "situation_p1_en": "The first full assessment of the university's external infrastructure took twelve hours of continuous manual analysis. It produced a real picture — and it was obsolete the moment a department spun up a new subdomain, which in a university happens constantly.",
        "situation_p1_es": "La primera evaluación completa de la infraestructura externa de la universidad tomó doce horas de análisis manual continuo. Produjo un panorama real — y quedó obsoleto en cuanto un departamento levantó un subdominio nuevo, lo que en una universidad pasa constantemente.",
        "situation_p2_en": "That is the trap most organisations fall into: the assessment becomes an annual event because nobody can justify twelve hours a month. The fix is not working faster by hand. It is making the assessment repeatable enough that running it stops being a decision.",
        "situation_p2_es": "Esa es la trampa en la que cae casi toda organización: la evaluación se vuelve un evento anual porque nadie puede justificar doce horas al mes. La solución no es trabajar más rápido a mano. Es hacer la evaluación lo bastante repetible como para que correrla deje de ser una decisión.",
        "did": [
            ("Ran the manual baseline first", "Correr primero la línea base manual",
             "Twelve hours of continuous analysis across the full external estate, to establish what the assessment should find before automating the search for it.",
             "Doce horas de análisis continuo sobre toda la superficie externa, para establecer qué debía encontrar la evaluación antes de automatizar la búsqueda."),
            ("Encoded the analysis, not just the scanning", "Codificar el análisis, no solo el escaneo",
             "The automation reproduces the reasoning steps of the manual pass, so the output is a triaged finding rather than a raw scanner dump somebody still has to read.",
             "La automatización reproduce los pasos de razonamiento del pase manual, de modo que la salida es un hallazgo triado y no un volcado de escáner que alguien todavía tiene que leer."),
            ("Made the subdomain the unit of work", "Hacer del subdominio la unidad de trabajo",
             "Each subdomain is assessed independently in around eight minutes, which means new ones get covered as they appear instead of waiting for the next full sweep.",
             "Cada subdominio se evalúa de forma independiente en unos ocho minutos, lo que significa que los nuevos quedan cubiertos conforme aparecen en vez de esperar al siguiente barrido completo."),
            ("Handed over the tooling", "Entregar la herramienta",
             "The automation belongs to the client and runs without us, which is the difference between a report and a capability.",
             "La automatización es del cliente y corre sin nosotros, que es la diferencia entre un reporte y una capacidad."),
        ],
        "metrics": [
            ("12 h", "of continuous manual analysis, before", "de análisis manual continuo, antes"),
            ("~8 min", "per subdomain, automated", "por subdominio, automatizado"),
            ("Days → hours", "for a full sweep of the estate", "para un barrido completo"),
            ("Repeatable", "the assessment is now a routine, not an event",
             "la evaluación ahora es rutina, no evento"),
        ],
        "lesson_h_en": "What this case actually shows",
        "lesson_h_es": "Qué demuestra realmente este caso",
        "lesson_en": "The headline number is the eight minutes, but the result that matters is the change in frequency. An assessment that costs twelve hours gets run once a year and argued about; one that costs eight minutes per subdomain gets run whenever something changes. Security posture is not decided by how good a single assessment is — it is decided by how often you can afford to look.",
        "lesson_es": "El número llamativo son los ocho minutos, pero el resultado que importa es el cambio de frecuencia. Una evaluación que cuesta doce horas se corre una vez al año y se discute; una que cuesta ocho minutos por subdominio se corre cada vez que algo cambia. La postura de seguridad no la decide qué tan buena es una evaluación aislada: la decide con qué frecuencia puedes darte el lujo de mirar.",
        "consent_en": "The client asked not to be named. Scope, method and figures are published with their authorisation; no finding, host or vulnerability detail is included.",
        "consent_es": "El cliente pidió no ser nombrado. El alcance, el método y las cifras se publican con su autorización; no se incluye ningún hallazgo, host ni detalle de vulnerabilidad.",
        "stack": "Python · DNS · Subdomain enumeration · Automated triage · Reporting",
    },
    {
        "slug": "reporting-engine",
        "practice": "ai-automation",
        "kicker_en": "AI &amp; Automation · Enterprise reporting",
        "kicker_es": "IA y automatización · Reporteo enterprise",
        "client_en": "Enterprise reporting workflow",
        "client_es": "Flujo de reporteo enterprise",
        "title_en": "Weekly Reporting Automation: Three Person-Hours a Week Became Twenty Minutes of Review",
        "title_es": "Automatización de reportes semanales: tres horas-persona a la semana se volvieron veinte minutos de revisión",
        "desc_en": "Two analysts spent 1.5 hours each preparing a weekly report. An AI-assisted pipeline now does the analysis in ten minutes, leaving twenty minutes of human curation — roughly 128 person-hours a year returned.",
        "desc_es": "Dos analistas dedicaban 1.5 horas cada uno a preparar un reporte semanal. Un pipeline asistido por IA hace ahora el análisis en diez minutos, dejando veinte de curación humana — cerca de 128 horas-persona al año recuperadas.",
        "h1_en": "Three person-hours a week, returned",
        "h1_es": "Tres horas-persona a la semana, recuperadas",
        "deck_en": "The weekly report had the same shape every week: export, clean, analyse, write, format, send. Two people, an hour and a half each. The pipeline now does the mechanical part in ten minutes and the humans do what humans are for — checking that the numbers deserve to be trusted.",
        "deck_es": "El reporte semanal tenía la misma forma cada semana: exportar, limpiar, analizar, redactar, formatear, enviar. Dos personas, hora y media cada una. El pipeline hace ahora la parte mecánica en diez minutos y los humanos hacen lo que sí les toca: verificar que los números merezcan confianza.",
        "meta": [
            ("Practice", "Práctica", "AI &amp; Automation", "IA y automatización"),
            ("Cadence", "Frecuencia", "Weekly", "Semanal"),
            ("Volume", "Volumen", "~50 MB per file", "~50 MB por archivo"),
            ("Before", "Antes", "2 people × 1.5 h", "2 personas × 1.5 h"),
            ("After", "Después", "10 min tooling + 20 min review", "10 min de herramienta + 20 min de revisión"),
        ],
        "situation_h_en": "The report was not hard. It was just relentless",
        "situation_h_es": "El reporte no era difícil. Solo era implacable",
        "situation_p1_en": "Two analysts each spent about an hour and a half a week producing the same weekly report: pulling the export, cleaning it, running the analysis, writing the observations and formatting the output. Nothing about it was intellectually difficult. It simply arrived every week, forever.",
        "situation_p1_es": "Dos analistas dedicaban cada uno alrededor de hora y media a la semana a producir el mismo reporte: bajar la exportación, limpiarla, correr el análisis, redactar las observaciones y formatear la salida. Nada de eso era intelectualmente difícil. Simplemente llegaba cada semana, para siempre.",
        "situation_p2_en": "The obvious automation would have been the wrong one: an AI that writes a confident summary nobody can verify. At around fifty megabytes per file, a wrong figure is easy to produce and nearly impossible to spot downstream — so data integrity had to be part of the design, not a hope.",
        "situation_p2_es": "La automatización obvia habría sido la equivocada: una IA que escribe un resumen seguro de sí mismo que nadie puede verificar. Con unos cincuenta megabytes por archivo, una cifra equivocada es fácil de producir y casi imposible de detectar aguas abajo — así que la integridad de los datos tenía que ser parte del diseño, no una esperanza.",
        "did": [
            ("Measured the manual baseline", "Medir la línea base manual",
             "Two people, an hour and a half each, every week. That figure became both the budget for the work and the criterion for calling it successful.",
             "Dos personas, hora y media cada una, cada semana. Esa cifra se volvió a la vez el presupuesto del trabajo y el criterio para llamarlo exitoso."),
            ("Automated the mechanical half", "Automatizar la mitad mecánica",
             "Ingestion, cleaning, calculation and draft narrative run in about ten minutes across roughly fifty megabytes per file.",
             "Ingesta, limpieza, cálculo y narrativa borrador corren en unos diez minutos sobre cerca de cincuenta megabytes por archivo."),
            ("Kept a human on integrity", "Dejar un humano en la integridad",
             "Twenty minutes of curation and refinement remain deliberately in the loop. Figures are computed in code and traceable to source; the reviewer confirms the reading, not the arithmetic.",
             "Veinte minutos de curación y refinamiento se quedan deliberadamente en el circuito. Las cifras se calculan por código y son rastreables a la fuente; quien revisa confirma la lectura, no la aritmética."),
            ("Left the schedule alone", "No tocar el calendario",
             "The report still lands weekly, in the same format, for the same audience. Nobody downstream had to change how they work.",
             "El reporte sigue llegando cada semana, en el mismo formato, para la misma audiencia. Nadie aguas abajo tuvo que cambiar su forma de trabajar."),
        ],
        "metrics": [
            ("3 h", "of human work per week, before", "de trabajo humano por semana, antes"),
            ("20 min", "of human work per week, after", "de trabajo humano por semana, después"),
            ("~89%", "less human time on the same report", "menos tiempo humano en el mismo reporte"),
            ("~128 h", "returned per year, at 48 working weeks", "recuperadas al año, a 48 semanas laborales"),
        ],
        "lesson_h_en": "What this case actually shows",
        "lesson_h_es": "Qué demuestra realmente este caso",
        "lesson_en": "The twenty minutes that stayed are the interesting part. It would have been easy to claim the whole ninety, and the demo would have looked better — but a reporting pipeline nobody checks is a liability dressed as a saving. The human step is what makes the other eighty-nine percent safe to bank.",
        "lesson_es": "Los veinte minutos que se quedaron son la parte interesante. Habría sido fácil reclamar los noventa completos, y el demo se habría visto mejor — pero un pipeline de reportes que nadie revisa es un pasivo disfrazado de ahorro. El paso humano es lo que hace que el otro ochenta y nueve por ciento se pueda dar por bueno.",
        "consent_en": "Published without naming the organisation. Figures are the measured before-and-after of the workflow; no data, client or commercial detail is included.",
        "consent_es": "Publicado sin nombrar a la organización. Las cifras son el antes y después medido del flujo; no se incluye ningún dato, cliente ni detalle comercial.",
        "stack": "Python · Pandas · LLM analysis · Word/PDF generation · Scheduled delivery",
    },
    {
        "slug": "granelco",
        "practice": "software-engineering",
        "kicker_en": "Software engineering · Built in-house",
        "kicker_es": "Ingeniería de software · Construido en casa",
        "client_en": "In-house — our own retail operation",
        "client_es": "En casa — nuestra propia operación de retail",
        "title_en": "GranelCo: A Retail Application Built In-House and Still Running Daily",
        "title_es": "GranelCo: una aplicación de retail construida en casa y todavía en uso diario",
        "desc_en": "A packaged desktop application for goods sold by weight, used daily by three people. Built for our own store, which means we live with every design decision we made.",
        "desc_es": "Una aplicación de escritorio empaquetada para productos vendidos a granel, usada a diario por tres personas. Construida para nuestra propia tienda, lo que significa que vivimos con cada decisión de diseño que tomamos.",
        "h1_en": "The application we had to live with",
        "h1_es": "La aplicación con la que tuvimos que vivir",
        "deck_en": "GranelCo runs a real retail operation selling goods by weight: collections, inventory and cost updates. Three people use it every day. It was built for our own store, so every shortcut would have been our problem — which is a useful way to build software.",
        "deck_es": "GranelCo opera un negocio real de venta a granel: cobranza, inventario y actualización de costos. Tres personas la usan todos los días. Se construyó para nuestra propia tienda, así que cada atajo habría sido nuestro problema — que resulta una forma útil de construir software.",
        "meta": [
            ("Client", "Cliente", "In-house", "En casa"),
            ("Practice", "Práctica", "Software engineering", "Ingeniería de software"),
            ("Users", "Usuarios", "3, daily", "3, a diario"),
            ("Status", "Estado", "In production", "En producción"),
            ("Form factor", "Formato", "Packaged desktop app", "App de escritorio empaquetada"),
        ],
        "situation_h_en": "Selling by weight breaks most off-the-shelf systems",
        "situation_h_es": "Vender a granel rompe casi cualquier sistema de caja",
        "situation_p1_en": "Retail software generally assumes a unit: one item, one price, one barcode. Goods sold by weight do not behave that way, and the gap shows up exactly where it hurts — in collections, in inventory counts and in keeping costs current when the purchase price moves.",
        "situation_p1_es": "El software de retail normalmente asume una unidad: un artículo, un precio, un código de barras. Los productos a granel no se comportan así, y el hueco aparece justo donde duele — en la cobranza, en el conteo de inventario y en mantener actualizados los costos cuando el precio de compra se mueve.",
        "situation_p2_en": "Those three processes were where the time went. The application was scoped around them rather than around a feature list, and it was packaged as a desktop app because the store needed it to work whether or not the internet did.",
        "situation_p2_es": "En esos tres procesos se iba el tiempo. La aplicación se acotó alrededor de ellos y no alrededor de una lista de funcionalidades, y se empaquetó como app de escritorio porque la tienda necesitaba que funcionara hubiera o no internet.",
        "did": [
            ("Scoped to three processes", "Acotar a tres procesos",
             "Collections, inventory and cost updates — the three places where weight-based selling actually costs time. Everything else was left out of the first version on purpose.",
             "Cobranza, inventario y actualización de costos — los tres lugares donde la venta a granel realmente cuesta tiempo. Todo lo demás quedó fuera de la primera versión a propósito."),
            ("Built full-stack, packaged for the desk", "Construir full-stack, empaquetado para el escritorio",
             "React and Vite on the front end, FastAPI and SQLAlchemy behind it, SQLite for storage, JWT for authentication, and Tauri to package it as an installable desktop application.",
             "React y Vite en el front end, FastAPI y SQLAlchemy detrás, SQLite para almacenamiento, JWT para autenticación y Tauri para empaquetarla como aplicación de escritorio instalable."),
            ("Shipped to real users immediately", "Ponerla en manos reales de inmediato",
             "Three people started using it in a live store, which surfaces design mistakes in days rather than in a UAT session that everyone is trying to finish.",
             "Tres personas empezaron a usarla en una tienda operando, lo que saca los errores de diseño en días en vez de en una sesión de pruebas que todos quieren terminar rápido."),
            ("Kept it in production", "Mantenerla en producción",
             "It is still the system the store runs on. That is the only durability test that means anything.",
             "Sigue siendo el sistema con el que opera la tienda. Esa es la única prueba de durabilidad que significa algo."),
        ],
        "metrics": [
            ("3", "people using it daily", "personas usándola a diario"),
            ("3", "processes replaced: collections, inventory, costs",
             "procesos reemplazados: cobranza, inventario, costos"),
            ("In production", "still the system the store runs on", "sigue siendo el sistema de la tienda"),
            ("Offline-capable", "packaged desktop app, not a web tab",
             "app de escritorio empaquetada, no una pestaña web"),
        ],
        "lesson_h_en": "What this case actually shows",
        "lesson_h_es": "Qué demuestra realmente este caso",
        "lesson_en": "This one is transparent about what it is: an in-house build for our own operation, not a client engagement, and the time saved was never formally measured. What it does demonstrate is a full-stack application scoped around three real processes, shipped to daily users and still running — with the people who wrote it living with every decision. Software built by someone who has to use it on Monday ages differently.",
        "lesson_es": "Este caso es transparente sobre lo que es: una construcción interna para nuestra propia operación, no un proyecto de cliente, y el tiempo ahorrado nunca se midió formalmente. Lo que sí demuestra es una aplicación full-stack acotada alrededor de tres procesos reales, entregada a usuarios diarios y todavía funcionando — con quienes la escribieron viviendo cada decisión. El software que construye alguien que tiene que usarlo el lunes envejece distinto.",
        "consent_en": "In-house project. Published without commercial figures because none were formally measured; the operational facts are stated as they are.",
        "consent_es": "Proyecto interno. Publicado sin cifras comerciales porque ninguna se midió formalmente; los hechos operativos se declaran tal como son.",
        "stack": "React · Vite · FastAPI · SQLAlchemy · SQLite · JWT · Tauri",
    },
    {
        "slug": "aaif",
        "practice": "ai-automation",
        "kicker_en": "AI &amp; Automation · Internal framework",
        "kicker_es": "IA y automatización · Framework interno",
        "client_en": "Internal delivery framework",
        "client_es": "Framework interno de entrega",
        "title_en": "AAIF: An AI Operating Framework of 18 Master Skills That Keeps Delivery Consistent",
        "title_es": "AAIF: un framework de operación con IA de 18 skills maestras que mantiene consistente la entrega",
        "desc_en": "Eighteen master skills, each with its own internal structure, covering standards, playbooks, decision trees and reviewers. A long deliverable takes 12 to 15 minutes and comes back needing minimal changes.",
        "desc_es": "Dieciocho skills maestras, cada una con estructura propia, que cubren estándares, playbooks, árboles de decisión y revisores. Un entregable largo toma de 12 a 15 minutos y regresa necesitando cambios mínimos.",
        "h1_en": "The framework that stops AI output from being a lottery",
        "h1_es": "El framework que evita que la salida de la IA sea una lotería",
        "deck_en": "AI-assisted delivery has a quality problem nobody advertises: it is excellent one week and unusable the next. AAIF is the internal answer — eighteen master skills covering standards, playbooks, decision trees and reviewers, so the output is consistent enough to put a name on.",
        "deck_es": "La entrega asistida por IA tiene un problema de calidad que nadie anuncia: es excelente una semana e inservible la siguiente. AAIF es la respuesta interna — dieciocho skills maestras que cubren estándares, playbooks, árboles de decisión y revisores, para que la salida sea lo bastante consistente como para ponerle nombre.",
        "meta": [
            ("Type", "Tipo", "Internal framework", "Framework interno"),
            ("Practice", "Práctica", "AI &amp; Automation", "IA y automatización"),
            ("Master skills", "Skills maestras", "18", "18"),
            ("Long deliverable", "Entregable largo", "12–15 minutes", "12–15 minutos"),
            ("Rework", "Retrabajo", "Minimal", "Mínimo"),
        ],
        "situation_h_en": "The problem with AI-assisted work is not capability. It is variance",
        "situation_h_es": "El problema del trabajo asistido por IA no es la capacidad. Es la varianza",
        "situation_p1_en": "Anyone can get a good result out of a language model once. Getting the same standard of result on Tuesday that you got on Friday, on a different topic, from a different starting prompt, is a different problem — and it is the one that decides whether AI-assisted delivery is a business or a demo.",
        "situation_p1_es": "Cualquiera puede sacar un buen resultado de un modelo de lenguaje una vez. Obtener el martes el mismo nivel de resultado que obtuviste el viernes, sobre otro tema y desde otro punto de partida, es un problema distinto — y es el que decide si la entrega asistida por IA es un negocio o un demo.",
        "situation_p2_en": "The answer was not better prompting. It was structure: written standards for how a document is built, playbooks for recurring workflows, decision trees for the choices that keep coming back, and reviewers that check the output against a checklist before it reaches anyone.",
        "situation_p2_es": "La respuesta no fue mejorar los prompts. Fue estructura: estándares escritos de cómo se construye un documento, playbooks para flujos recurrentes, árboles de decisión para las elecciones que se repiten, y revisores que verifican la salida contra una lista antes de que llegue a nadie.",
        "did": [
            ("Wrote the standards down", "Escribir los estándares",
             "Writing conventions, documentation structure, diagram notation, architecture and security baselines — the things a senior reviewer would otherwise have to say out loud every time.",
             "Convenciones de escritura, estructura de documentación, notación de diagramas, líneas base de arquitectura y seguridad — lo que de otro modo un revisor senior tendría que decir en voz alta cada vez."),
            ("Turned recurring work into playbooks", "Convertir el trabajo recurrente en playbooks",
             "Step-by-step workflows for software engineering, cybersecurity, data and trade and logistics, so a repeated task follows the same route every time.",
             "Flujos paso a paso para ingeniería de software, ciberseguridad, datos y comercio y logística, para que una tarea repetida siga la misma ruta cada vez."),
            ("Added reviewers and quality gates", "Añadir revisores y quality gates",
             "Checklists with explicit red flags that run before a deliverable is considered finished — the reason the output comes back needing minimal changes.",
             "Listas de verificación con red flags explícitas que corren antes de dar por terminado un entregable — la razón por la que la salida regresa necesitando cambios mínimos."),
            ("Kept it modular", "Mantenerlo modular",
             "Eighteen master skills, each with its own internal structure, so a domain can be improved without rewriting the framework around it.",
             "Dieciocho skills maestras, cada una con estructura propia, para que un dominio se pueda mejorar sin reescribir el framework alrededor."),
        ],
        "metrics": [
            ("18", "master skills, each with internal structure", "skills maestras, cada una con estructura propia"),
            ("12–15 min", "for a long deliverable, end to end", "para un entregable largo, de punta a punta"),
            ("Minimal", "rework needed on the output", "retrabajo necesario sobre la salida"),
            ("Reused", "across every engagement in this studio", "en todos los proyectos de este estudio"),
        ],
        "lesson_h_en": "What this case actually shows",
        "lesson_h_es": "Qué demuestra realmente este caso",
        "lesson_en": "AAIF is not a product for sale — it is the reason the other cases on this site look similar in quality despite covering different domains. It is included here because a client buying AI automation should know whether the person building it has solved the consistency problem for their own work first. Anyone can demo a good output. The question is what happens on the fiftieth one.",
        "lesson_es": "AAIF no es un producto a la venta — es la razón por la que los demás casos de este sitio se parecen en calidad a pesar de cubrir dominios distintos. Se incluye aquí porque un cliente que compra automatización con IA debería saber si quien la construye resolvió antes el problema de consistencia para su propio trabajo. Cualquiera puede demostrar una buena salida. La pregunta es qué pasa en la número cincuenta.",
        "consent_en": "Internal framework. The 12–15 minute figure is the observed run time for a long deliverable, not a benchmark.",
        "consent_es": "Framework interno. La cifra de 12–15 minutos es el tiempo observado de ejecución para un entregable largo, no un benchmark.",
        "stack": "Skills · Playbooks · Decision trees · Reviewers · Quality gates",
    },
]

PRACTICE_NAMES = {
    "cybersecurity": ("Cybersecurity", "Ciberseguridad"),
    "ai-automation": ("AI &amp; Automation", "IA y automatización"),
    "software-engineering": ("Software Engineering", "Ingeniería de software"),
    "data-analytics": ("Data &amp; Analytics", "Datos y analítica"),
    "technical-delivery": ("Technical Delivery", "Entrega técnica"),
}


def nav_html(active_cta="#contact"):
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
      <a class="cta-sm" href="{active_cta}" data-i18n="nav.cta">Book an assessment</a>
    </nav>
  </div>"""


def form_html(selected_value: str) -> str:
    options = [
        ("Software Engineering", "form.o1", "Software Engineering"),
        ("AI &amp; Automation", "form.o2", "AI &amp; Automation"),
        ("Cybersecurity", "form.o3", "Cybersecurity"),
        ("Data &amp; Analytics", "form.o4", "Data &amp; Analytics"),
        ("Technical Delivery", "form.o5", "Technical Delivery &amp; Account Leadership"),
        ("Not sure yet", "form.o6", "Not sure yet"),
    ]
    opts = []
    for value, key, label in options:
        sel = " selected" if value.replace("&amp;", "&") == selected_value else ""
        opts.append(f'          <option value="{value}" data-i18n="{key}"{sel}>{label}</option>')
    return """    <form class="form" id="contactForm" method="post" action="/api/contact" novalidate>
      <label><span data-i18n="form.company">Company</span><input name="company" required maxlength="120" autocomplete="organization" data-i18n-ph="form.ph.company" placeholder="Your company"></label>
      <label><span data-i18n="form.email">Work email</span><input type="email" name="email" required maxlength="254" autocomplete="email" data-i18n-ph="form.ph.email" placeholder="you@company.com"></label>
      <label><span data-i18n="form.practice">Practice</span><select name="practice">
""" + "\n".join(opts) + """
      </select></label>
      <label><span data-i18n="form.problem">The problem</span><textarea name="message" rows="5" required maxlength="4000" data-i18n-ph="form.ph.message" placeholder="What are you trying to fix, build or protect?"></textarea></label>

      <div class="hp" aria-hidden="true"><label>Leave this field empty<input name="website" type="text" tabindex="-1" autocomplete="off"></label></div>
      <input type="hidden" name="rendered_at" id="renderedAt">

      <button type="submit" id="submitBtn" data-i18n="form.send">Send the brief</button>
      <p class="formstatus" id="formStatus" role="status" aria-live="polite"></p>
      <p class="formnote" data-i18n="form.note">We use your message to reply to you. Nothing else — no list, no third parties.</p>
    </form>"""


PRACTICE_VALUE = {
    "cybersecurity": "Cybersecurity",
    "ai-automation": "AI & Automation",
    "software-engineering": "Software Engineering",
    "data-analytics": "Data & Analytics",
    "technical-delivery": "Technical Delivery",
}


def build_case(c: dict) -> str:
    url = f"{DOMAIN}/work/{c['slug']}/"
    practice_en, practice_es = PRACTICE_NAMES[c["practice"]]

    meta_rows = "\n".join(
        f'        <div class="filerow"><dt data-i18n="cs.mk{i+1}">{k_en}</dt>'
        f'<dd data-i18n="cs.mv{i+1}">{v_en}</dd></div>'
        for i, (k_en, k_es, v_en, v_es) in enumerate(c["meta"])
    )

    did = "\n".join(
        f'      <div class="step"><b>{i+1:02d}</b>'
        f'<h3 data-i18n="cs.did{i+1}t">{E(t_en)}</h3>'
        f'<p data-i18n="cs.did{i+1}d">{E(d_en)}</p></div>'
        for i, (t_en, t_es, d_en, d_es) in enumerate(c["did"])
    )

    metrics = "\n".join(
        f'      <div class="metric"><b data-i18n="cs.mn{i+1}">{E(n)}</b>'
        f'<span data-i18n="cs.ml{i+1}">{E(l_en)}</span></div>'
        for i, (n, l_en, l_es) in enumerate(c["metrics"])
    )

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": url + "#case",
                "headline": c["title_en"],
                "description": c["desc_en"],
                "inLanguage": "en",
                "isPartOf": {"@id": DOMAIN + "/work/"},
                "about": {"@type": "Service", "name": practice_en.replace("&amp;", "&")},
                "publisher": {"@id": DOMAIN + "/#studio"},
                "url": url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Case studies", "item": DOMAIN + "/work/"},
                    {"@type": "ListItem", "position": 3,
                     "name": c["title_en"].split(":")[0].strip(), "item": url},
                ],
            },
        ],
    }

    return f"""<!doctype html>
<html lang="en" dir="ltr" data-i18n-page="case-{c['slug']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(c["title_en"])} | Technical Transformation Studio</title>
<meta name="description" content="{E(c["desc_en"])}">

<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0E2439">

<!-- Iconos. El navegador pide /favicon.ico solo, sin que nadie se lo diga:
     por eso, sin archivo, aparece un 404 en la consola. Los <link> hacen el resto:
     el SVG lo prefieren los navegadores modernos, el ICO es el respaldo. -->
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{url}">
<link rel="alternate" hreflang="es" href="{DOMAIN}/es/casos/{c['slug']}/">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{E(c["title_en"])}">
<meta property="og:description" content="{E(c["desc_en"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og/case-{c['slug']}.png">
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
        <a href="/" data-i18n="cs.crumbHome">Home</a>
        <span aria-hidden="true">/</span>
        <a href="/work/" data-i18n="cs.crumbWork">Case studies</a>
        <span aria-hidden="true">/</span>
        <span data-i18n="cs.crumbSelf">{E(c["title_en"].split(":")[0].strip())}</span>
      </nav>
      <p class="kicker" data-i18n="cs.kicker">{c["kicker_en"]}</p>
      <h1 data-i18n="cs.h1">{E(c["h1_en"])}</h1>
      <p class="deck" data-i18n="cs.deck">{E(c["deck_en"])}</p>
      <div class="btnrow">
        <a class="btn btn-fill" href="#contact" data-i18n="cs.cta1">Discuss a similar problem</a>
        <a class="btn btn-line" href="/services/{c['practice']}/" data-i18n="cs.cta2">See the practice</a>
      </div>
    </div>
    <div class="filecard">
      <h2 data-i18n="cs.atAGlance">At a glance</h2>
      <dl>
{meta_rows}
      </dl>
      <p class="stamp" data-i18n="cs.stack">{c["stack"]}</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="cs.sitKicker">The situation</p>
      <h2 class="sect" data-i18n="cs.sitH">{E(c["situation_h_en"])}</h2>
    </div>
    <div class="prose">
      <p data-i18n="cs.sitP1">{E(c["situation_p1_en"])}</p>
      <p data-i18n="cs.sitP2">{E(c["situation_p2_en"])}</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="cs.didKicker">What we did</p>
      <h2 class="sect" data-i18n="cs.didH">Four steps, in this order.</h2>
    </div>
    <div class="ladder">
{did}
    </div>
  </div>
</section>

<section class="band results">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker gold" data-i18n="cs.resKicker">Results</p>
      <h2 class="sect" data-i18n="cs.resH">The numbers, as measured.</h2>
    </div>
    <div class="metrics">
{metrics}
    </div>
    <p class="consent" data-i18n="cs.consent">{E(c["consent_en"])}</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="cs.lessonKicker">The takeaway</p>
      <h2 class="sect" data-i18n="cs.lessonH">{E(c["lesson_h_en"])}</h2>
    </div>
    <div class="prose">
      <p data-i18n="cs.lesson">{E(c["lesson_en"])}</p>
      <p><a class="plink" href="/services/{c['practice']}/" data-i18n="cs.practiceLink">Read about the {practice_en} practice →</a></p>
    </div>
  </div>
</section>

<section class="band contact" id="contact">
  <div class="wrap">
    <div>
      <p class="kicker gold" data-i18n="con.kicker">Start here</p>
      <h2 class="sect" data-i18n="cs.conH">Have a version of this problem?</h2>
      <div class="band-head"><p data-i18n="con.lead">Describe the problem in a few lines. You get a written reply with a first read on it, whether or not there is an engagement in it. The message is sent from this page — no email client, no third-party form service, no trackers.</p></div>
    </div>
{form_html(PRACTICE_VALUE[c["practice"]])}
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


def build_case_dict(c: dict) -> str:
    practice_en, practice_es = PRACTICE_NAMES[c["practice"]]
    d = {
        "cs.crumbHome": "Inicio",
        "cs.crumbWork": "Casos",
        "cs.crumbSelf": c["title_es"].split(":")[0].strip(),
        "cs.kicker": c["kicker_es"],
        "cs.h1": c["h1_es"],
        "cs.deck": c["deck_es"],
        "cs.cta1": "Hablemos de un problema parecido",
        "cs.cta2": "Ver la práctica",
        "cs.atAGlance": "De un vistazo",
        "cs.stack": c["stack"],
        "cs.sitKicker": "La situación",
        "cs.sitH": c["situation_h_es"],
        "cs.sitP1": c["situation_p1_es"],
        "cs.sitP2": c["situation_p2_es"],
        "cs.didKicker": "Qué hicimos",
        "cs.didH": "Cuatro pasos, en este orden.",
        "cs.resKicker": "Resultados",
        "cs.resH": "Los números, como se midieron.",
        "cs.consent": c["consent_es"],
        "cs.lessonKicker": "La conclusión",
        "cs.lessonH": c["lesson_h_es"],
        "cs.lesson": c["lesson_es"],
        "cs.practiceLink": f"Leer sobre la práctica de {practice_es} →",
        "cs.conH": "¿Tienes una versión de este problema?",
        "cs.backWork": "Todos los casos",
    }
    for i, (k_en, k_es, v_en, v_es) in enumerate(c["meta"]):
        d[f"cs.mk{i+1}"] = k_es
        d[f"cs.mv{i+1}"] = v_es
    for i, (t_en, t_es, dd_en, dd_es) in enumerate(c["did"]):
        d[f"cs.did{i+1}t"] = t_es
        d[f"cs.did{i+1}d"] = dd_es
    for i, (n, l_en, l_es) in enumerate(c["metrics"]):
        d[f"cs.mn{i+1}"] = n
        d[f"cs.ml{i+1}"] = l_es

    body = ",\n".join(f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}'
                      for k, v in d.items())
    return (f'/* Español — caso "{c["slug"]}".\n'
            f'   Generado por tools/build_cases.py: edita el contenido allí, no aquí. */\n'
            f'window.ttsRegisterDictionary("es", {{\n{body}\n}});\n')


def build_index() -> str:
    cards = []
    for i, c in enumerate(CASES):
        headline = c["metrics"][0][0]
        headline_label = c["metrics"][0][1]
        cards.append(f"""      <article class="pcase">
        <span data-i18n="wk.k{i+1}">{c["kicker_en"]}</span>
        <h3 data-i18n="wk.t{i+1}">{E(c["title_en"].split(":")[0].strip())}</h3>
        <p data-i18n="wk.d{i+1}">{E(c["desc_en"])}</p>
        <p class="headline-metric"><b data-i18n="wk.n{i+1}">{E(headline)}</b> <span data-i18n="wk.nl{i+1}">{E(headline_label)}</span></p>
        <div class="tech">{c["stack"]}</div>
        <a class="plink" href="/work/{c['slug']}/" data-i18n="wk.a{i+1}">Read the case →</a>
      </article>""")

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "@id": DOMAIN + "/work/",
                "name": "Case studies",
                "description": "Measured results from software engineering, AI automation and cybersecurity engagements.",
                "url": DOMAIN + "/work/",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Case studies", "item": DOMAIN + "/work/"},
                ],
            },
        ],
    }

    return f"""<!doctype html>
<html lang="en" dir="ltr" data-i18n-page="work-index">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Case Studies: Measured Results from Real Engagements | Technical Transformation Studio</title>
<meta name="description" content="Five engagements with the numbers attached: a phishing takedown in three days, an attack surface assessment cut to eight minutes per subdomain, and a weekly report cut from three person-hours to twenty minutes.">

<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="color-scheme" content="light">
<meta name="theme-color" content="#0E2439">

<!-- Iconos. El navegador pide /favicon.ico solo, sin que nadie se lo diga:
     por eso, sin archivo, aparece un 404 en la consola. Los <link> hacen el resto:
     el SVG lo prefieren los navegadores modernos, el ICO es el respaldo. -->
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="canonical" href="{DOMAIN}/work/">
<link rel="alternate" hreflang="en" href="{DOMAIN}/work/">
<link rel="alternate" hreflang="es" href="{DOMAIN}/es/casos/">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}/work/">
<meta property="og:type" content="website">
<meta property="og:title" content="Case studies — measured results from real engagements">
<meta property="og:description" content="Five engagements with the numbers attached.">
<meta property="og:url" content="{DOMAIN}/work/">
<meta property="og:image" content="{DOMAIN}/og/work.png">
<meta name="twitter:card" content="summary_large_image">

<link rel="stylesheet" href="/styles.css">
</head>
<body>
<a class="skip" href="#main" data-i18n="skip">Skip to content</a>

<header class="masthead">
{nav_html("/#contact")}
</header>

<main id="main">
<section class="hero" id="top">
  <div class="wrap">
    <div>
      <nav class="crumbs" aria-label="Breadcrumb">
        <a href="/" data-i18n="wk.crumbHome">Home</a>
        <span aria-hidden="true">/</span>
        <span data-i18n="wk.crumbSelf">Case studies</span>
      </nav>
      <p class="kicker" data-i18n="wk.kicker">Evidence</p>
      <h1><span data-i18n="wk.h1a">Systems that exist, with the</span> <em data-i18n="wk.h1b">numbers attached.</em></h1>
      <p class="deck" data-i18n="wk.deck">Five engagements, written up with what was measured and what was not. Where a figure was never recorded, that is stated rather than estimated — a case study that rounds up is a sales document, not evidence.</p>
      <div class="btnrow">
        <a class="btn btn-fill" href="/#contact" data-i18n="wk.cta1">Book a technical assessment</a>
        <a class="btn btn-line" href="/#practices" data-i18n="wk.cta2">See the five practices</a>
      </div>
    </div>
    <div class="filecard">
      <h2 data-i18n="wk.summaryHead">Published figures</h2>
      <dl>
        <div class="filerow"><dt data-i18n="wk.s1k">Phishing takedown</dt><dd data-i18n="wk.s1v">3 days</dd></div>
        <div class="filerow"><dt data-i18n="wk.s2k">Assessment per subdomain</dt><dd data-i18n="wk.s2v">~8 minutes</dd></div>
        <div class="filerow"><dt data-i18n="wk.s3k">Weekly reporting time</dt><dd data-i18n="wk.s3v">3 h → 20 min</dd></div>
        <div class="filerow"><dt data-i18n="wk.s4k">Hidden assets found</dt><dd data-i18n="wk.s4v">7</dd></div>
        <div class="filerow"><dt data-i18n="wk.s5k">Framework skills</dt><dd data-i18n="wk.s5v">18</dd></div>
      </dl>
      <p class="stamp" data-i18n="wk.stamp">Every figure comes from the client or from a measured run.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="wk.listKicker">Five cases</p>
      <h2 class="sect" data-i18n="wk.listH">What was actually delivered.</h2>
    </div>
    <div class="proof">
{chr(10).join(cards)}
    </div>
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


def build_index_dict() -> str:
    d = {
        "wk.crumbHome": "Inicio",
        "wk.crumbSelf": "Casos",
        "wk.kicker": "Evidencia",
        "wk.h1a": "Sistemas que existen, con los",
        "wk.h1b": "números encima.",
        "wk.deck": "Cinco proyectos, escritos con lo que se midió y lo que no. Donde una cifra nunca se registró, se dice en vez de estimarse — un caso que redondea hacia arriba es un documento de ventas, no evidencia.",
        "wk.cta1": "Agenda un diagnóstico técnico",
        "wk.cta2": "Ver las cinco prácticas",
        "wk.summaryHead": "Cifras publicadas",
        "wk.s1k": "Baja de phishing", "wk.s1v": "3 días",
        "wk.s2k": "Evaluación por subdominio", "wk.s2v": "~8 minutos",
        "wk.s3k": "Tiempo de reporte semanal", "wk.s3v": "3 h → 20 min",
        "wk.s4k": "Activos ocultos hallados", "wk.s4v": "7",
        "wk.s5k": "Skills del framework", "wk.s5v": "18",
        "wk.stamp": "Cada cifra viene del cliente o de una corrida medida.",
        "wk.listKicker": "Cinco casos",
        "wk.listH": "Lo que se entregó de verdad.",
        "wk.backHome": "Volver al inicio",
    }
    for i, c in enumerate(CASES):
        d[f"wk.k{i+1}"] = c["kicker_es"]
        d[f"wk.t{i+1}"] = c["title_es"].split(":")[0].strip()
        d[f"wk.d{i+1}"] = c["desc_es"]
        d[f"wk.n{i+1}"] = c["metrics"][0][0]
        d[f"wk.nl{i+1}"] = c["metrics"][0][2]
        d[f"wk.a{i+1}"] = "Leer el caso →"

    body = ",\n".join(f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}'
                      for k, v in d.items())
    return ('/* Español — índice de casos. Generado por tools/build_cases.py. */\n'
            f'window.ttsRegisterDictionary("es", {{\n{body}\n}});\n')


def main() -> None:
    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "work" / "index.html").write_text(build_index(), encoding="utf-8")
    (ROOT / "i18n" / "work-index.es.js").write_text(build_index_dict(), encoding="utf-8")
    print("  work/index.html  +  i18n/work-index.es.js")

    for c in CASES:
        out = ROOT / "work" / c["slug"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.html").write_text(build_case(c), encoding="utf-8")
        (ROOT / "i18n" / f"case-{c['slug']}.es.js").write_text(build_case_dict(c), encoding="utf-8")
        print(f"  work/{c['slug']}/index.html  +  i18n/case-{c['slug']}.es.js")

    print(f"\n{len(CASES)} casos generados. Corre tools/build_pages.py para el sitemap.")


if __name__ == "__main__":
    main()
