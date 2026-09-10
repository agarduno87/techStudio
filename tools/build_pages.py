#!/usr/bin/env python3
"""
Genera las páginas de servicio a partir del contenido definido aquí abajo.

Por qué un generador y no cinco HTML a mano: las cinco páginas comparten cabecera,
formulario, pie y estructura. Escritas a mano, cualquier cambio en la navegación
obliga a tocar cinco archivos y tarde o temprano una se queda atrás. Aquí el
contenido vive en un solo lugar y el HTML se regenera.

Uso:
    python3 tools/build_pages.py

Salida:
    services/<slug>/index.html
    i18n/<slug>.es.js
    sitemap.xml
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
DOMAIN = "https://tu-dominio.com"

# ---------------------------------------------------------------------------
# CONTENIDO
#
# Cada bloque de "experience" está tomado de la trayectoria real: TAM en una
# plataforma global de verificación publicitaria cotizada en NYSE, Scrum Master en
# Enroute Systems, PM en C.O.C.O.A., consultoría de ciberseguridad en una
# universidad pública y en una consultoría legal, y los proyectos propios.
#
# Nota deliberada: NO se nombra al empleador actual. Ver README, sección
# "Referencias a empleadores y clientes".
# ---------------------------------------------------------------------------

PAGES = [
    {
        "slug": "software-engineering",
        "num": "01",
        "title_en": "Custom Software Development: Internal Tools, APIs and Business Applications",
        "title_es": "Desarrollo de software a la medida: herramientas internas, APIs y aplicaciones de negocio",
        "desc_en": "Custom internal tools, APIs, dashboards and business applications built to a fixed scope and handed over with source code and documentation. Remote from Querétaro, México.",
        "desc_es": "Herramientas internas, APIs, dashboards y aplicaciones de negocio a la medida, construidas a alcance cerrado y entregadas con código fuente y documentación. Remoto desde Querétaro, México.",
        "h1_en": "Custom software your team can actually maintain",
        "h1_es": "Software a la medida que tu equipo sí puede mantener",
        "deck_en": "Internal tools, APIs, dashboards and business applications built to a fixed scope, delivered working, and handed over with the source code and the documentation to keep them running without us.",
        "deck_es": "Herramientas internas, APIs, dashboards y aplicaciones de negocio construidas a alcance cerrado, entregadas funcionando y con el código fuente y la documentación para mantenerlas sin nosotros.",
        "problem_h_en": "The spreadsheet that became a system nobody designed",
        "problem_h_es": "La hoja de cálculo que se volvió un sistema que nadie diseñó",
        "problem_p1_en": "Most internal software starts as a spreadsheet someone built in an afternoon. Then a second file references it, then a macro, then a shared drive nobody dares reorganise. By the time it breaks, four people depend on it and none of them can explain how a number is produced.",
        "problem_p1_es": "Casi todo el software interno empieza como una hoja de cálculo que alguien armó en una tarde. Luego otro archivo la referencia, luego una macro, luego una carpeta compartida que nadie se atreve a reorganizar. Para cuando se rompe, cuatro personas dependen de ella y ninguna puede explicar cómo sale un número.",
        "problem_p2_en": "The fix is not a bigger spreadsheet. It is a small, well-scoped application with permissions, logs and an audit trail — built to be handed over, not to make you dependent on whoever wrote it.",
        "problem_p2_es": "La solución no es una hoja de cálculo más grande. Es una aplicación pequeña y bien acotada, con permisos, logs y trazabilidad — hecha para entregarse, no para dejarte dependiendo de quien la escribió.",
        "in": [
            ("Internal tools, business applications and admin panels",
             "Herramientas internas, aplicaciones de negocio y paneles de administración"),
            ("REST APIs, third-party integrations and workflow systems",
             "APIs REST, integraciones con terceros y sistemas de flujo de trabajo"),
            ("Database design, migration and query performance",
             "Diseño de bases de datos, migración y desempeño de consultas"),
            ("Source code, documentation, deployment notes and a handover session",
             "Código fuente, documentación, notas de despliegue y sesión de entrega"),
        ],
        "out": [
            ("Consumer mobile applications", "Aplicaciones móviles de consumo"),
            ("24/7 production on-call unless a retainer is agreed",
             "Guardia 24/7 en producción salvo retainer acordado"),
            ("Hardware or embedded firmware", "Hardware o firmware embebido"),
        ],
        "steps": [
            ("Walk the process", "Recorrer el proceso",
             "We sit with the people who run it today and map what actually happens, including the workarounds nobody documented.",
             "Nos sentamos con quien lo opera hoy y mapeamos lo que de verdad pasa, incluidos los atajos que nadie documentó."),
            ("Agree the scope in writing", "Acordar el alcance por escrito",
             "Features, data model, integrations and what is explicitly out. You approve it before a line of code exists.",
             "Funcionalidades, modelo de datos, integraciones y lo que queda explícitamente fuera. Lo apruebas antes de que exista una línea de código."),
            ("Build in visible increments", "Construir en incrementos visibles",
             "Working software every week or two, not a demo at the end. If it is going the wrong way you find out early, when it is cheap.",
             "Software funcionando cada una o dos semanas, no un demo al final. Si va por mal camino te enteras temprano, cuando es barato."),
            ("Hand it over properly", "Entregarlo de verdad",
             "Repository, documentation, credentials and a working session with whoever will maintain it. Our access is revoked at closure.",
             "Repositorio, documentación, credenciales y una sesión de trabajo con quien lo va a mantener. Nuestros accesos se revocan al cierre."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("Four parallel software workstreams, at once",
             "Cuatro flujos de software en paralelo, al mismo tiempo",
             "As a certified Scrum Master at a software company, ran four delivery workstreams simultaneously — a CRM platform, a career-path dashboard, a time-off management system and a document-generation tool — owning estimates, cross-team dependencies and every Agile ceremony, tracked in Jira and Confluence.",
             "Como Scrum Master certificado en una empresa de software, llevó cuatro flujos de entrega al mismo tiempo — plataforma CRM, dashboard de plan de carrera, sistema de gestión de ausencias y herramienta de generación de documentos — con los estimados, las dependencias entre equipos y todas las ceremonias ágiles, rastreado en Jira y Confluence."),
            ("Full-stack, end to end",
             "Full-stack, de punta a punta",
             "Mechatronics engineer with full-stack web development training. Recent build: a packaged desktop application for goods sold by weight, combining a React/Vite front end, a FastAPI and SQLAlchemy back end, SQLite, JWT authentication and Tauri packaging.",
             "Ingeniero mecatrónico con formación en desarrollo web full-stack. Construcción reciente: aplicación de escritorio empaquetada para venta a granel, con front end en React/Vite, back end en FastAPI y SQLAlchemy, SQLite, autenticación JWT y empaquetado con Tauri."),
            ("Estimates that hold up",
             "Estimados que se sostienen",
             "Delivery commitments grounded in real internal cost rather than optimism — which is what keeps dates credible with clients and leadership when something slips.",
             "Compromisos de entrega basados en costo interno real y no en optimismo — que es lo que mantiene creíbles las fechas ante clientes y dirección cuando algo se atrasa."),
        ],
        "faq": [
            ("What technologies do you build with?",
             "¿Con qué tecnologías construyen?",
             "Python with FastAPI on the back end, React on the front end, PostgreSQL or SQLite for data, and Tauri when the result needs to be an installable desktop app. The stack is chosen for what your team can maintain, not for what is fashionable.",
             "Python con FastAPI en el back end, React en el front end, PostgreSQL o SQLite para datos, y Tauri cuando el resultado tiene que ser una app de escritorio instalable. El stack se elige por lo que tu equipo puede mantener, no por lo que está de moda."),
            ("Can you work with our existing codebase?",
             "¿Pueden trabajar sobre nuestro código existente?",
             "Yes. It usually starts with a short assessment to read the code, understand what it does and tell you honestly whether extending it or replacing it is the cheaper path.",
             "Sí. Normalmente empieza con un diagnóstico corto para leer el código, entender qué hace y decirte con honestidad si extenderlo o reemplazarlo sale más barato."),
            ("What happens if the scope changes mid-project?",
             "¿Qué pasa si el alcance cambia a medio proyecto?",
             "It gets re-quoted in writing before the work starts, not absorbed silently and billed later. Changes are normal; surprises are not.",
             "Se recotiza por escrito antes de hacer el trabajo, no se absorbe en silencio y se factura después. Los cambios son normales; las sorpresas no."),
            ("Who owns the code?",
             "¿De quién es el código?",
             "You do, from the first commit. The repository, documentation and credentials are yours, and any access we hold is revoked when the engagement closes.",
             "Tuyo, desde el primer commit. El repositorio, la documentación y las credenciales son tuyos, y cualquier acceso que tengamos se revoca al cierre del proyecto."),
        ],
        "form_value": "Software Engineering",
    },
    {
        "slug": "ai-automation",
        "num": "02",
        "title_en": "AI Automation for Business: Reporting Automation and Agentic AI Assistants",
        "title_es": "Automatización con IA para empresas: reportes automáticos y asistentes de IA agénticos",
        "desc_en": "Turn manual reporting into an automated system: Excel and CSV in, analysis and generated Word/PDF reports out. Agentic AI assistants over your own data, with traceable outputs.",
        "desc_es": "Convierte el reporteo manual en un sistema automatizado: entran Excel y CSV, salen análisis y reportes Word/PDF generados. Asistentes de IA agénticos sobre tus propios datos, con resultados rastreables.",
        "h1_en": "Automated reporting and AI agents over your own data",
        "h1_es": "Reportes automatizados y agentes de IA sobre tus propios datos",
        "deck_en": "Spreadsheets in, analysed reports out, on schedule — with every figure traceable back to the row that produced it. Because a number nobody can verify is worse than no number at all.",
        "deck_es": "Entran hojas de cálculo, salen reportes analizados, en calendario — con cada cifra rastreable hasta el renglón que la produjo. Porque un número que nadie puede verificar es peor que no tener número.",
        "problem_h_en": "Someone's Friday disappears into copy-paste",
        "problem_h_es": "El viernes de alguien se va en copiar y pegar",
        "problem_p1_en": "The weekly report is the same shape every week. Someone exports the data, cleans it, pastes it into a template, writes the same three observations, converts it to PDF and emails it. Multiply that by the number of people doing it and the number of weeks in a year, and you are paying a salary for work a system should do.",
        "problem_p1_es": "El reporte semanal tiene la misma forma cada semana. Alguien exporta los datos, los limpia, los pega en una plantilla, escribe las mismas tres observaciones, lo convierte a PDF y lo manda por correo. Multiplica eso por la cantidad de gente que lo hace y las semanas del año, y estás pagando un sueldo por trabajo que debería hacer un sistema.",
        "problem_p2_en": "The trap is automating it badly: an AI that produces confident summaries nobody can check. The output has to be traceable to the source, or you have replaced slow work with fast risk.",
        "problem_p2_es": "La trampa es automatizarlo mal: una IA que produce resúmenes seguros de sí mismos que nadie puede verificar. El resultado tiene que ser rastreable hasta la fuente, o cambiaste trabajo lento por riesgo rápido.",
        "in": [
            ("Agentic AI assistants over your own documents and databases",
             "Asistentes de IA agénticos sobre tus propios documentos y bases de datos"),
            ("Reporting automation: Excel, CSV, email or database → analysis → Word/PDF",
             "Automatización de reportes: Excel, CSV, correo o base de datos → análisis → Word/PDF"),
            ("Document processing, classification and knowledge systems",
             "Procesamiento de documentos, clasificación y sistemas de conocimiento"),
            ("Validation and citations so every figure stays traceable",
             "Validación y citas para que cada cifra siga siendo rastreable"),
        ],
        "out": [
            ("Training foundation models from scratch",
             "Entrenar modelos base desde cero"),
            ("Reselling model licences or credits",
             "Revender licencias o créditos de modelos"),
            ("Autonomous decisions with no human review",
             "Decisiones autónomas sin revisión humana"),
        ],
        "steps": [
            ("Pick one painful process", "Elegir un proceso doloroso",
             "Not the whole department. One report, one workflow, one inbox — the one people complain about by name.",
             "No el departamento completo. Un reporte, un flujo, una bandeja — ese del que la gente se queja por su nombre."),
            ("Measure what it costs today", "Medir lo que cuesta hoy",
             "People, hours per week, fully loaded cost. That number is the budget and the success criterion at the same time.",
             "Personas, horas por semana, costo cargado. Ese número es el presupuesto y el criterio de éxito a la vez."),
            ("Build the pipeline with checks", "Construir el pipeline con controles",
             "Ingestion, rules, AI analysis where it adds value, and validation that flags anything the model is not confident about instead of hiding it.",
             "Ingesta, reglas, análisis con IA donde aporta valor, y validación que marca lo que el modelo no tiene claro en vez de esconderlo."),
            ("Run both in parallel, then switch", "Correr ambos en paralelo y luego cambiar",
             "For a few cycles the manual version and the automated one run side by side and the outputs are compared. You switch when the numbers match, not when the demo looks good.",
             "Durante algunos ciclos la versión manual y la automatizada corren lado a lado y se comparan los resultados. Cambias cuando los números coinciden, no cuando el demo se ve bien."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("An AI reporting assistant used at executive level",
             "Un asistente de reportes con IA usado a nivel directivo",
             "Built an agentic AI assistant that analyses large databases, performs precise calculations and turns the result into VP-level executive reporting — the kind of output that gets read in a leadership meeting rather than filed.",
             "Construyó un asistente de IA agéntico que analiza bases de datos grandes, hace cálculos precisos y convierte el resultado en reportes ejecutivos a nivel VP — del tipo que se lee en una junta directiva en vez de archivarse."),
            ("Certified in the tooling, not just the concept",
             "Certificado en la herramienta, no solo en el concepto",
             "Certified in AI Agents with RAG and LangChain, plus Python (Pontificia Universidad Católica de Chile) and Databases for Data Scientists (University of Colorado Boulder). Working automation stack: Python, n8n, RAG pipelines.",
             "Certificado en Agentes de IA con RAG y LangChain, más Python (Pontificia Universidad Católica de Chile) y Bases de Datos para Científicos de Datos (Universidad de Colorado Boulder). Stack de automatización: Python, n8n, pipelines RAG."),
            ("A framework that keeps AI output consistent",
             "Un framework que mantiene consistente la salida de la IA",
             "Author of a modular AI operating framework built around skills, playbooks, decision trees and reviewers — the discipline that stops AI-assisted delivery from being brilliant one week and unusable the next.",
             "Autor de un framework modular de operación con IA basado en skills, playbooks, árboles de decisión y revisores — la disciplina que evita que la entrega asistida por IA sea brillante una semana e inservible la siguiente."),
        ],
        "faq": [
            ("Will the AI make things up?",
             "¿La IA se va a inventar cosas?",
             "That is the risk the design has to answer. Figures come from your data through code, not from the model's memory; the model writes the narrative around numbers it did not invent, and anything it is unsure about is flagged for a human rather than smoothed over.",
             "Ese es el riesgo que el diseño tiene que resolver. Las cifras salen de tus datos por código, no de la memoria del modelo; el modelo escribe la narrativa alrededor de números que no inventó, y lo que no tiene claro se marca para revisión humana en vez de maquillarse."),
            ("Where does our data go?",
             "¿A dónde van nuestros datos?",
             "That is decided with you before anything is built, and it is written into the scope: which model provider, what leaves your infrastructure, what is retained and for how long. If nothing may leave, the design changes accordingly.",
             "Se decide contigo antes de construir nada, y queda escrito en el alcance: qué proveedor de modelo, qué sale de tu infraestructura, qué se retiene y por cuánto tiempo. Si nada puede salir, el diseño cambia en consecuencia."),
            ("How much does an automation project cost?",
             "¿Cuánto cuesta un proyecto de automatización?",
             "An MVP typically starts around USD 4,500 and the exact figure depends on how many systems it has to touch. The assessment that precedes it starts around USD 1,500 and you keep the roadmap either way.",
             "Un MVP arranca típicamente alrededor de USD 4,500 y la cifra exacta depende de cuántos sistemas tenga que tocar. El diagnóstico previo arranca alrededor de USD 1,500 y te quedas con la hoja de ruta pase lo que pase."),
            ("What if the process changes after we automate it?",
             "¿Y si el proceso cambia después de automatizarlo?",
             "Systems built here are meant to be edited: documented, versioned and handed to your team. Small changes should not require calling us back.",
             "Los sistemas que se construyen aquí están hechos para editarse: documentados, versionados y entregados a tu equipo. Un cambio chico no debería obligarte a llamarnos."),
        ],
        "form_value": "AI & Automation",
    },
    {
        "slug": "cybersecurity",
        "num": "03",
        "title_en": "Web Application Penetration Testing, Vulnerability Assessment and Cyber Risk Governance",
        "title_es": "Pentesting de aplicaciones web, análisis de vulnerabilidades y gobierno del riesgo",
        "desc_en": "Scoped web application penetration testing by a certified tester, external exposure discovery, vulnerability analysis and a risk governance plan. Written authorisation and rules of engagement before anything is tested.",
        "desc_es": "Pentesting de aplicaciones web con alcance acotado por un tester certificado, descubrimiento de exposición externa, análisis de vulnerabilidades y plan de gobierno del riesgo. Autorización escrita y reglas de enfrentamiento antes de probar nada.",
        "h1_en": "See what you expose before someone else does",
        "h1_es": "Mira lo que expones antes de que alguien más lo haga",
        "deck_en": "External exposure discovery, scoped web application penetration testing by a certified tester, and a risk governance plan your leadership can actually run — with owners, deadlines and a monitoring baseline that keeps working after the report is delivered.",
        "deck_es": "Descubrimiento de exposición externa, pentesting de aplicaciones web con alcance acotado por un tester certificado, y un plan de gobierno del riesgo que tu dirección sí puede operar — con responsables, fechas y una base de monitoreo que sigue funcionando después de entregado el reporte.",
        "problem_h_en": "Your attack surface grew while nobody was counting",
        "problem_h_es": "Tu superficie de ataque creció mientras nadie contaba",
        "problem_p1_en": "Every subdomain a marketing agency spun up, every test server someone forgot to shut down, every certificate about to expire, every admin panel reachable from the open internet — it is all public, and an attacker enumerates it in minutes with free tooling.",
        "problem_p1_es": "Cada subdominio que levantó una agencia de marketing, cada servidor de pruebas que alguien olvidó apagar, cada certificado por vencer, cada panel de administración alcanzable desde internet — todo eso es público, y un atacante lo enumera en minutos con herramientas gratuitas.",
        "problem_p2_en": "Most companies without a security team have never seen that list. The first deliverable here is not a fix — it is simply knowing what exists, because you cannot govern a risk you cannot name, and you cannot test an application you forgot you were running.",
        "problem_p2_es": "La mayoría de las empresas sin equipo de seguridad nunca ha visto esa lista. El primer entregable aquí no es un arreglo: es simplemente saber qué existe, porque no puedes gobernar un riesgo que no puedes nombrar, ni probar una aplicación que olvidaste que tenías corriendo.",
        "in": [
            ("Discovery of domains, subdomains, DNS records, IPs, services and certificates",
             "Descubrimiento de dominios, subdominios, registros DNS, IPs, servicios y certificados"),
            ("Scoped web application penetration testing, under written authorisation and agreed rules of engagement",
             "Pentesting de aplicaciones web con alcance acotado, bajo autorización escrita y reglas de enfrentamiento acordadas"),
            ("Vulnerability analysis, severity triage and a mitigation plan with named owners",
             "Análisis de vulnerabilidades, triaje por severidad y plan de mitigación con responsables con nombre"),
            ("Risk register, governance cadence, monitoring and executive reporting",
             "Matriz de riesgo, cadencia de gobierno, monitoreo y reporte ejecutivo"),
        ],
        "out": [
            ("Full-scope red-team, social engineering and physical intrusion exercises",
             "Red team de alcance completo, ingeniería social y ejercicios de intrusión física"),
            ("Certified regulatory audits (ISO 27001, SOC 2 attestation)",
             "Auditorías regulatorias certificadas (ISO 27001, certificación SOC 2)"),
            ("24/7 staffed incident response", "Respuesta a incidentes 24/7 con personal"),
        ],
        "steps": [
            ("Authorisation and rules of engagement", "Autorización y reglas de enfrentamiento",
             "Nothing is scanned or tested before the asset owner authorises it in writing. For a penetration test we also agree the rules of engagement first: which targets, which techniques, which hours, and who to call if something breaks.",
             "No se escanea ni se prueba nada antes de que el dueño de los activos lo autorice por escrito. Para un pentest además se acuerdan primero las reglas de enfrentamiento: qué objetivos, qué técnicas, en qué horario y a quién llamar si algo se rompe."),
            ("Map the external surface", "Mapear la superficie externa",
             "Domains, subdomains, DNS, certificates, exposed services. The inventory almost always contains something nobody in the room knew was online.",
             "Dominios, subdominios, DNS, certificados, servicios expuestos. El inventario casi siempre trae algo que nadie en la sala sabía que estaba en línea."),
            ("Triage by real impact", "Triar por impacto real",
             "Not a raw scanner dump. Each finding gets a severity, a business consequence and an owner, so leadership can decide what is worth money now and what can wait.",
             "No un volcado de escáner. Cada hallazgo lleva severidad, consecuencia de negocio y responsable, para que la dirección decida qué vale dinero ahora y qué puede esperar."),
            ("Install the cadence", "Instalar la cadencia",
             "A risk register your team keeps, monitoring that alerts on change, and a reporting rhythm — so the second month is better than the first instead of identical to it.",
             "Una matriz de riesgo que tu equipo mantiene, monitoreo que alerta ante cambios y un ritmo de reporte — para que el segundo mes sea mejor que el primero en vez de idéntico."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("Certified web penetration tester, currently practising",
             "Web penetration tester certificado, ejerciendo hoy",
             "Certified Web Penetration Tester (American Council for Cybersecurity) — not a course badge but the credential the testing runs under. Two live engagements in parallel during 2026: vulnerability assessments for one of Mexico's largest public universities, and risk management for a legal and real-estate consultancy.",
             "Web Penetration Tester certificado (American Council for Cybersecurity) — no una insignia de curso, sino la credencial bajo la que se ejecutan las pruebas. Dos proyectos vivos en paralelo durante 2026: análisis de vulnerabilidades para una de las universidades públicas más grandes de México, y gestión de riesgos para una consultoría legal e inmobiliaria."),
            ("Real threats, neutralised",
             "Amenazas reales, neutralizadas",
             "Designed a full risk management plan — threat identification, prioritisation and mitigation — and neutralised active phishing and impersonation campaigns aimed at a firm and its clients. Not a tabletop exercise: live attacks, shut down.",
             "Diseñó un plan completo de gestión de riesgos — identificación, priorización y mitigación de amenazas — y neutralizó campañas activas de phishing y suplantación dirigidas a un despacho y a sus clientes. No fue un ejercicio de escritorio: ataques en curso, detenidos."),
            ("Assessment work made repeatable",
             "Trabajo de evaluación hecho repetible",
             "Built automation so recurring security assessments run the same way every time, plus a monitoring dashboard covering DNS visibility, service discovery, change alerting and operational reporting.",
             "Construyó automatización para que las evaluaciones de seguridad recurrentes corran igual cada vez, más un dashboard de monitoreo con visibilidad DNS, descubrimiento de servicios, alertas de cambio y reporte operativo."),
        ],
        "faq": [
            ("Do you perform penetration testing?",
             "¿Hacen pruebas de penetración?",
             "Yes — scoped web application penetration testing, run by a certified Web Penetration Tester under written authorisation and agreed rules of engagement. What is not included is full-scope red-team work, social engineering and physical intrusion: those need a different team, a different contract and a different conversation with your legal counsel. The scope is written down and signed before anything is tested.",
             "Sí — pentesting de aplicaciones web con alcance acotado, ejecutado por un Web Penetration Tester certificado, bajo autorización escrita y reglas de enfrentamiento acordadas. Lo que no se incluye es red team de alcance completo, ingeniería social e intrusión física: eso requiere otro equipo, otro contrato y otra conversación con tu área legal. El alcance se escribe y se firma antes de probar nada."),
            ("Do we need to authorise the testing?",
             "¿Tenemos que autorizar las pruebas?",
             "Yes, in writing, from whoever owns the assets — before anything begins. If the target runs on a third-party platform, that provider usually has to authorise it too. Testing infrastructure without documented authorisation is a legal problem for both sides, so it is a hard prerequisite rather than a formality.",
             "Sí, por escrito y de parte de quien sea dueño de los activos, antes de que empiece nada. Si el objetivo corre sobre una plataforma de terceros, ese proveedor normalmente también tiene que autorizarlo. Probar infraestructura sin autorización documentada es un problema legal para ambas partes, así que es un prerrequisito duro y no una formalidad."),
            ("We are a small company. Is this overkill?",
             "Somos una empresa chica. ¿Esto no es demasiado?",
             "The opposite: companies without a security team are the ones with the largest blind spot, and the discovery step is cheap. Knowing what you expose costs far less than finding out through an incident.",
             "Al revés: las empresas sin equipo de seguridad son las que tienen el punto ciego más grande, y el paso de descubrimiento es barato. Saber qué expones cuesta muchísimo menos que enterarte por un incidente."),
            ("What do we get at the end?",
             "¿Qué recibimos al final?",
             "An inventory of your external footprint, a test report with reproduction steps for each finding, severity and business impact, a mitigation plan with owners and dates, a risk register, and a monitoring baseline that keeps running. Retesting after remediation is agreed up front rather than sold back to you later.",
             "Un inventario de tu huella externa, un reporte de pruebas con los pasos de reproducción de cada hallazgo, severidad e impacto de negocio, un plan de mitigación con responsables y fechas, una matriz de riesgo y una base de monitoreo que sigue corriendo. El retest tras la remediación se acuerda desde el inicio, no se te revende después."),
        ],
        "form_value": "Cybersecurity",
    },
    {
        "slug": "data-analytics",
        "num": "04",
        "title_en": "Data, Analytics and Engineering: Pipelines, Warehousing, Dashboards and BI",
        "title_es": "Datos, analítica e ingeniería: pipelines, warehousing, dashboards y BI",
        "desc_en": "Data pipelines and orchestration, a modelled warehouse (Snowflake, dbt), operational dashboards and business intelligence — with metric definitions agreed with the business and the queries handed over with the analysis.",
        "desc_es": "Pipelines y orquestación de datos, un warehouse modelado (Snowflake, dbt), dashboards operativos e inteligencia de negocio — con las definiciones de métricas acordadas con el negocio y las consultas entregadas junto con el análisis.",
        "h1_en": "Numbers someone is willing to sign",
        "h1_es": "Números que alguien está dispuesto a firmar",
        "deck_en": "Scattered exports turned into dashboards and scheduled reporting — with the metric definitions agreed before the first chart is drawn, and the queries handed over so anyone can check the work.",
        "deck_es": "Exportaciones dispersas convertidas en dashboards y reporteo en calendario — con las definiciones de métricas acordadas antes de dibujar la primera gráfica, y las consultas entregadas para que cualquiera pueda revisar el trabajo.",
        "problem_h_en": "Two people, two dashboards, two different truths",
        "problem_h_es": "Dos personas, dos dashboards, dos verdades distintas",
        "problem_p1_en": "The most expensive meeting in any company is the one that starts by arguing about whose number is right. It usually happens because nobody ever wrote down what the metric means — does a sale count when it is invoiced, when it is paid, or when it ships?",
        "problem_p1_es": "La junta más cara de cualquier empresa es la que empieza discutiendo de quién es el número correcto. Casi siempre pasa porque nadie escribió qué significa la métrica — ¿una venta cuenta cuando se factura, cuando se paga o cuando se embarca?",
        "problem_p2_en": "Tooling does not fix that. Definitions do. The dashboard is the last step, not the first, and it is only as trustworthy as the agreement underneath it.",
        "problem_p2_es": "Las herramientas no arreglan eso. Las definiciones sí. El dashboard es el último paso, no el primero, y solo es tan confiable como el acuerdo que tiene debajo.",
        "in": [
            ("Data pipelines and orchestration (Airflow), cleaning and consolidation across sources",
             "Pipelines y orquestación de datos (Airflow), limpieza y consolidación entre fuentes"),
            ("Data warehousing and modelling (Snowflake, dbt)",
             "Data warehousing y modelado (Snowflake, dbt)"),
            ("Operational dashboards, scheduled reporting and business intelligence",
             "Dashboards operativos, reporteo en calendario e inteligencia de negocio"),
            ("Metric definitions agreed with the business, with the queries handed over",
             "Definiciones de métricas acordadas con el negocio, con las consultas entregadas"),
        ],
        "out": [
            ("Real-time streaming platforms at web scale",
             "Plataformas de streaming en tiempo real a escala web"),
            ("Buying or brokering third-party data",
             "Compra o intermediación de datos de terceros"),
            ("Conclusions the sample size cannot support",
             "Conclusiones que la muestra no alcanza a sostener"),
        ],
        "steps": [
            ("Agree the definitions", "Acordar las definiciones",
             "Before any tooling: what each metric means, which source is authoritative, and who signs off when they disagree.",
             "Antes de cualquier herramienta: qué significa cada métrica, cuál fuente manda y quién decide cuando no coinciden."),
            ("Consolidate the sources", "Consolidar las fuentes",
             "Pipelines that pull, clean and reconcile automatically, so the reconciliation stops being somebody's Friday.",
             "Pipelines que extraen, limpian y cuadran automáticamente, para que la conciliación deje de ser el viernes de alguien."),
            ("Build what gets used", "Construir lo que sí se usa",
             "One dashboard people open daily beats twelve nobody remembers. We start with the decisions you actually make each week.",
             "Un dashboard que la gente abre a diario vale más que doce que nadie recuerda. Empezamos por las decisiones que de verdad tomas cada semana."),
            ("Hand over the queries", "Entregar las consultas",
             "Every number comes with the query that produced it. If we disappear tomorrow, your team can still audit and extend the work.",
             "Cada número viene con la consulta que lo produjo. Si desaparecemos mañana, tu equipo todavía puede auditar y extender el trabajo."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("Big data at enterprise scale",
             "Big data a escala enterprise",
             "Daily work with SQL and Python over Snowflake, AWS and Databricks — measurement, troubleshooting and custom reporting on datasets belonging to Fortune 500 accounts, not tutorial-sized samples.",
             "Trabajo diario con SQL y Python sobre Snowflake, AWS y Databricks — medición, diagnóstico y reporteo a la medida sobre conjuntos de datos de cuentas Fortune 500, no muestras de tutorial."),
            ("Measurement against published standards",
             "Medición contra estándares publicados",
             "Campaign measurement work assessed against IAB and MRC standards, covering viewability, invalid traffic and suitability. When a metric has to survive external scrutiny, the definition matters more than the chart.",
             "Trabajo de medición de campañas evaluado contra estándares IAB y MRC, cubriendo viewability, tráfico inválido y suitability. Cuando una métrica tiene que sobrevivir a escrutinio externo, la definición pesa más que la gráfica."),
            ("Formally trained, not self-taught only",
             "Con formación formal, no solo autodidacta",
             "Certified in Databases for Data Scientists (University of Colorado Boulder) and Python (Pontificia Universidad Católica de Chile), on top of a Mechatronics engineering degree.",
             "Certificado en Bases de Datos para Científicos de Datos (Universidad de Colorado Boulder) y Python (Pontificia Universidad Católica de Chile), además de la licenciatura en Ingeniería Mecatrónica."),
            ("Pipelines, warehouses and BI that run on their own",
             "Pipelines, warehouses y BI que corren solos",
             "The team's data engineering builds the layer under the dashboard: orchestrated pipelines (Apache Airflow), a warehouse modelled with Snowflake and dbt, and the business intelligence on top — so the numbers stay reliable and refresh without someone rebuilding them by hand each week.",
             "La ingeniería de datos del equipo construye la capa debajo del dashboard: pipelines orquestados (Apache Airflow), un warehouse modelado con Snowflake y dbt, y la inteligencia de negocio encima — para que los números sigan confiables y se actualicen sin que alguien los rehaga a mano cada semana."),
        ],
        "faq": [
            ("Which tools do you build dashboards in?",
             "¿En qué herramientas construyen los dashboards?",
             "Whatever your team already has a licence for and knows how to use. If there is nothing in place, a lightweight web dashboard you own outright avoids adding a subscription to maintain.",
             "En lo que tu equipo ya tenga licencia y sepa usar. Si no hay nada, un dashboard web ligero que sea completamente tuyo evita agregar una suscripción más que mantener."),
            ("Our data is messy. Do we need to clean it first?",
             "Nuestros datos están sucios. ¿Hay que limpiarlos primero?",
             "No — that is part of the work. Messy data is the normal starting point, and the cleaning rules get documented so the mess does not silently come back.",
             "No, eso es parte del trabajo. Los datos sucios son el punto de partida normal, y las reglas de limpieza quedan documentadas para que el desorden no regrese en silencio."),
            ("Can you tell us what the data means, not just show it?",
             "¿Nos pueden decir qué significan los datos, no solo mostrarlos?",
             "Yes, within what the data can actually support. Where the sample or the collection method does not justify a conclusion, you will be told that instead of being handed a confident chart.",
             "Sí, dentro de lo que los datos realmente sostienen. Donde la muestra o el método de recolección no justifiquen una conclusión, se te dirá, en vez de entregarte una gráfica segura de sí misma."),
            ("How does this differ from the automation service?",
             "¿En qué se diferencia del servicio de automatización?",
             "Automation is about removing manual work from a process you already understand. This practice is about making the numbers themselves trustworthy. They pair well, and the assessment tells you which one should come first.",
             "La automatización quita trabajo manual de un proceso que ya entiendes. Esta práctica hace confiables los números en sí. Se complementan bien, y el diagnóstico te dice cuál debe ir primero."),
        ],
        "form_value": "Data & Analytics",
    },
    {
        "slug": "technical-delivery",
        "num": "05",
        "title_en": "Fractional Technical Program Management and Enterprise Account Leadership",
        "title_es": "Gestión fraccional de programas técnicos y liderazgo de cuentas enterprise",
        "desc_en": "A senior technical owner between your engineering team and your customers: roadmaps, vendor coordination, escalation handling and executive reporting, on a monthly retainer.",
        "desc_es": "Un dueño técnico senior entre tu equipo de ingeniería y tus clientes: hojas de ruta, coordinación de proveedores, manejo de escalamientos y reporte ejecutivo, en retainer mensual.",
        "h1_en": "The technical owner your delivery is missing",
        "h1_es": "El dueño técnico que le falta a tu entrega",
        "deck_en": "Support answers tickets, sales answers commercials, engineering answers bugs — and the customer experiences three disconnected companies. This practice puts one person in the middle who owns the whole picture.",
        "deck_es": "Soporte contesta tickets, ventas contesta lo comercial, ingeniería contesta bugs — y el cliente vive tres empresas desconectadas. Esta práctica pone en medio a una persona que es dueña del panorama completo.",
        "problem_h_en": "Accounts do not churn over one incident",
        "problem_h_es": "Las cuentas no se pierden por un incidente",
        "problem_p1_en": "They churn because a series of incidents never got translated into a plan the customer could see. Each one was handled competently in isolation; nobody connected them, nobody reported the pattern, and by the time the renewal conversation arrived the trust was already spent.",
        "problem_p1_es": "Se pierden porque una serie de incidentes nunca se tradujo en un plan que el cliente pudiera ver. Cada uno se atendió bien por separado; nadie los conectó, nadie reportó el patrón, y para cuando llegó la conversación de renovación la confianza ya estaba gastada.",
        "problem_p2_en": "The same gap shows up internally: four workstreams, four backlogs, shared dependencies and no single view of what is actually at risk this quarter.",
        "problem_p2_es": "El mismo hueco aparece hacia adentro: cuatro flujos de trabajo, cuatro backlogs, dependencias compartidas y ninguna vista única de qué está realmente en riesgo este trimestre.",
        "in": [
            ("Roadmaps, delivery planning, risk and change management",
             "Hojas de ruta, planeación de entrega, gestión de riesgos y de cambios"),
            ("Vendor and engineering coordination across teams",
             "Coordinación de proveedores e ingeniería entre equipos"),
            ("Escalation handling and incident communication for enterprise accounts",
             "Manejo de escalamientos y comunicación de incidentes en cuentas enterprise"),
            ("Quarterly business reviews and executive reporting",
             "Revisiones trimestrales de negocio y reporte ejecutivo"),
        ],
        "out": [
            ("Quota-carrying new-business sales", "Venta nueva con cuota"),
            ("Tier-1 support staffing", "Cubrir el soporte de primer nivel"),
            ("Contract and legal negotiation", "Negociación contractual y legal"),
        ],
        "steps": [
            ("Read the current state", "Leer la situación actual",
             "Tickets, escalations, roadmap and the last two quarters of what went wrong. Patterns show up fast when someone finally looks across them.",
             "Tickets, escalamientos, hoja de ruta y los últimos dos trimestres de lo que salió mal. Los patrones aparecen rápido cuando por fin alguien los mira en conjunto."),
            ("Name one owner per thread", "Nombrar un dueño por hilo",
             "Every open thread gets a name and a date. Ambiguity about ownership is what turns a two-day fix into a two-month complaint.",
             "Cada hilo abierto recibe un nombre y una fecha. La ambigüedad sobre quién es dueño es lo que convierte un arreglo de dos días en una queja de dos meses."),
            ("Install the reporting rhythm", "Instalar el ritmo de reporte",
             "A cadence the customer and your leadership both see, written so an executive can act on it rather than forward it.",
             "Una cadencia que ven tanto el cliente como tu dirección, escrita para que un directivo actúe sobre ella en vez de reenviarla."),
            ("Transfer it", "Transferirlo",
             "The goal is that the function survives without a retainer: documented, staffed and running before the engagement winds down.",
             "El objetivo es que la función sobreviva sin retainer: documentada, con gente asignada y funcionando antes de que el proyecto termine."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("Fortune 500 technical delivery, for years",
             "Entrega técnica para Fortune 500, durante años",
             "Three and a half years owning technical delivery for Fortune 500 accounts at a NYSE-listed global technology company — coordinating engineering, product and client teams across the US and international markets, and driving root-cause analysis on live incidents under pressure.",
             "Tres años y medio como dueño de la entrega técnica de cuentas Fortune 500 en una compañía global de tecnología cotizada en NYSE — coordinando equipos de ingeniería, producto y cliente en Estados Unidos y mercados internacionales, y dirigiendo el análisis de causa raíz de incidentes en vivo bajo presión."),
            ("Certified in both disciplines",
             "Certificado en ambas disciplinas",
             "Certified Scrum Master and Google-certified Project Manager, with roughly a decade of professional experience and nine years in project and program management across software, industrial operations and consulting.",
             "Scrum Master certificado y Project Manager certificado por Google, con alrededor de una década de experiencia profesional y nueve años en gestión de proyectos y programas entre software, operaciones industriales y consultoría."),
            ("Risk management where mistakes cost something",
             "Gestión de riesgos donde los errores cuestan",
             "Career began running safety, quality and environmental programmes in industrial environments — which is where you learn to manage risk in places where a mistake has physical consequences, and to talk to everyone from the shop floor to the board.",
             "La carrera empezó dirigiendo programas de seguridad, calidad y medio ambiente en entornos industriales — donde se aprende a gestionar riesgo en lugares en los que un error tiene consecuencias físicas, y a hablar con todos, del piso de planta al consejo."),
        ],
        "faq": [
            ("Is this the same as hiring a project manager?",
             "¿Es lo mismo que contratar a un project manager?",
             "It is the same function at part-time allocation, without a headcount. It suits companies that need senior delivery ownership but do not yet have twelve months of full-time work to justify the hire.",
             "Es la misma función con dedicación parcial y sin plaza. Le sirve a empresas que necesitan responsabilidad senior de entrega pero todavía no tienen doce meses de trabajo de tiempo completo que justifiquen la contratación."),
            ("How much of your time do we get?",
             "¿Cuánto de tu tiempo recibimos?",
             "It is agreed at the start as a specific allocation, along with which meetings are attended and what the response expectation is. Vague retainers are how both sides end up disappointed.",
             "Se acuerda al inicio como una dedicación específica, junto con a qué juntas se asiste y cuál es la expectativa de respuesta. Los retainers vagos son la forma en que ambas partes terminan decepcionadas."),
            ("Do you replace our existing team?",
             "¿Reemplazan a nuestro equipo actual?",
             "No. This practice coordinates the team you have and, where there are gaps, makes them visible. Most engagements run alongside an internal team or an existing vendor with ownership defined at the start.",
             "No. Esta práctica coordina al equipo que tienes y, donde hay huecos, los hace visibles. Casi todos los proyectos corren junto a un equipo interno o un proveedor existente, con la propiedad definida desde el inicio."),
            ("What languages and time zones do you cover?",
             "¿Qué idiomas y husos horarios cubren?",
             "English and Spanish, based in Querétaro, México, working remotely. Overlap hours are agreed at the start of the engagement rather than assumed.",
             "Inglés y español, con base en Querétaro, México, trabajando en remoto. Las horas de traslape se acuerdan al inicio del proyecto en vez de darse por supuestas."),
        ],
        "form_value": "Technical Delivery",
    },
    {
        "slug": "web-growth",
        "num": "06",
        "title_en": "Website Development, SEO and Conversion-Focused Landing Pages",
        "title_es": "Desarrollo web, SEO y landing pages enfocadas a conversión",
        "desc_en": "Conversion-focused websites and landing pages with SEO foundations, analytics and forms wired to your CRM, email or WhatsApp. Source and hosting handed over — the site is yours.",
        "desc_es": "Sitios web y landing pages enfocados a conversión, con bases de SEO, analítica y formularios conectados a tu CRM, correo o WhatsApp. Código y hosting entregados — el sitio es tuyo.",
        "h1_en": "A website that brings you work, not just compliments",
        "h1_es": "Un sitio web que te trae trabajo, no solo cumplidos",
        "deck_en": "Public-facing sites and landing pages built to convert — with SEO foundations, analytics you can read, and forms wired to your CRM or WhatsApp so a visit becomes a lead someone actually follows up.",
        "deck_es": "Sitios públicos y landing pages hechos para convertir — con bases de SEO, analítica que sí puedes leer, y formularios conectados a tu CRM o WhatsApp para que una visita se vuelva un prospecto que alguien realmente atiende.",
        "problem_h_en": "A website that looks fine and does nothing",
        "problem_h_es": "Un sitio que se ve bien y no hace nada",
        "problem_p1_en": "Plenty of businesses have a site. Far fewer have a site that turns a visitor into a conversation. The page loads, it looks acceptable, and then nothing happens: no clear next step, no form that reaches anyone, no way to tell whether the last redesign helped or hurt.",
        "problem_p1_es": "Muchos negocios tienen un sitio. Muchos menos tienen un sitio que convierte a un visitante en una conversación. La página carga, se ve aceptable, y luego no pasa nada: sin un siguiente paso claro, sin un formulario que le llegue a alguien, sin forma de saber si el último rediseño ayudó o estorbó.",
        "problem_p2_en": "A site earns its cost when it captures a lead, routes it to a person, and lets you see in the numbers whether it is working. That is an engineering and measurement problem as much as a design one — which is exactly where this team lives.",
        "problem_p2_es": "Un sitio se paga solo cuando captura un prospecto, lo dirige a una persona y te deja ver en los números si está funcionando. Eso es tanto un problema de ingeniería y medición como de diseño — que es justo donde vive este equipo.",
        "in": [
            ("Conversion-focused websites and landing pages",
             "Sitios web y landing pages enfocados a conversión"),
            ("SEO foundations: structure, metadata, sitemap and speed",
             "Bases de SEO: estructura, metadatos, sitemap y velocidad"),
            ("Analytics and forms wired to CRM, email or WhatsApp, with notifications",
             "Analítica y formularios conectados a CRM, correo o WhatsApp, con notificaciones"),
            ("Source code, hosting setup and a handover — the site is yours",
             "Código fuente, configuración de hosting y entrega — el sitio es tuyo"),
        ],
        "out": [
            ("Ongoing content writing and social media management",
             "Redacción de contenido continua y gestión de redes sociales"),
            ("Paid-ads media buying and budget management",
             "Compra de medios y gestión de presupuesto de anuncios"),
            ("Brand identity design from scratch",
             "Diseño de identidad de marca desde cero"),
        ],
        "steps": [
            ("Define the one action", "Definir la acción única",
             "Before any design: what should a visitor do — call, book, fill a form, message on WhatsApp? Everything on the page serves that one action.",
             "Antes de cualquier diseño: ¿qué debe hacer un visitante — llamar, agendar, llenar un formulario, escribir por WhatsApp? Todo en la página sirve a esa única acción."),
            ("Build it fast and light", "Construirlo rápido y ligero",
             "A site that loads quickly and reads well on a phone, built in visible increments instead of one big reveal at the end.",
             "Un sitio que carga rápido y se lee bien en un teléfono, construido en incrementos visibles en vez de una gran revelación al final."),
            ("Wire the plumbing", "Conectar la tubería",
             "Forms to CRM, WhatsApp or email, notifications, analytics and the SEO foundations — so a lead is captured and you can watch it happen.",
             "Formularios a CRM, WhatsApp o correo, notificaciones, analítica y las bases de SEO — para que un prospecto se capture y puedas verlo suceder."),
            ("Hand it over", "Entregarlo",
             "Source, hosting setup, credentials and a short session, so you can edit the site or move it without calling us back.",
             "Código, configuración de hosting, credenciales y una sesión corta, para que puedas editar el sitio o moverlo sin volver a llamarnos."),
        ],
        "exp_h_en": "The experience behind this practice",
        "exp_h_es": "La experiencia detrás de esta práctica",
        "exp": [
            ("Production sites, shipped and handed over",
             "Sitios en producción, entregados",
             "This studio designs, builds and ships production websites end to end — bilingual, accessible and fast — and hands over the source, the hosting setup and the analytics to the owner rather than renting them back.",
             "Este estudio diseña, construye y publica sitios de producción de punta a punta — bilingües, accesibles y rápidos — y entrega el código, la configuración de hosting y la analítica al dueño en vez de rentárselos."),
            ("Integrations that make a form worth having",
             "Integraciones que hacen que un formulario valga la pena",
             "A background in solutions engineering and API and system integrations: connecting sites and forms to CRMs, WhatsApp and notification pipelines, so a lead is captured, routed and answered instead of lost in an inbox.",
             "Trayectoria en ingeniería de soluciones e integraciones de APIs y sistemas: conectar sitios y formularios a CRMs, WhatsApp y flujos de notificación, para que un prospecto se capture, se enrute y se responda en vez de perderse en una bandeja."),
            ("Measured, not guessed",
             "Medido, no adivinado",
             "Analytics and SEO set up so you can see what the site actually does — traffic, sources and conversions — instead of trusting that a redesign simply feels better.",
             "Analítica y SEO configurados para que veas lo que el sitio realmente hace — tráfico, fuentes y conversiones — en vez de confiar en que un rediseño simplemente se siente mejor."),
        ],
        "faq": [
            ("Do you design the brand and write the copy too?",
             "¿También diseñan la marca y escriben los textos?",
             "We build the site and can structure the copy with you, but ongoing content writing, brand identity from scratch and social media management are out of scope by default. We tell you what is needed and can point you to it.",
             "Construimos el sitio y podemos estructurar los textos contigo, pero la redacción de contenido continua, la identidad de marca desde cero y la gestión de redes quedan fuera de alcance por defecto. Te decimos qué hace falta y podemos orientarte."),
            ("Will the site rank on Google?",
             "¿El sitio va a posicionar en Google?",
             "We set the SEO foundations — structure, metadata, sitemap, speed and analytics — which is what makes ranking possible. Ranking itself also depends on content and time, and we are honest about what a technical foundation can and cannot promise.",
             "Ponemos las bases de SEO — estructura, metadatos, sitemap, velocidad y analítica — que es lo que hace posible posicionar. El posicionamiento en sí también depende del contenido y del tiempo, y somos honestos sobre lo que una base técnica sí y no puede prometer."),
            ("Can you connect the form to our WhatsApp or CRM?",
             "¿Pueden conectar el formulario a nuestro WhatsApp o CRM?",
             "Yes — that is the point of this practice. Forms wired to WhatsApp, email or your CRM, with notifications so a lead reaches a person quickly instead of sitting unseen.",
             "Sí — ese es el punto de esta práctica. Formularios conectados a WhatsApp, correo o tu CRM, con notificaciones para que un prospecto le llegue rápido a una persona en vez de quedarse sin ver."),
            ("Who hosts it, and do we own it?",
             "¿Quién lo hospeda y es nuestro?",
             "You own it. We hand over the source, the hosting setup and the credentials; the site can live on your hosting or on one we set up in your name.",
             "Es tuyo. Entregamos el código, la configuración de hosting y las credenciales; el sitio puede vivir en tu hosting o en uno que configuramos a tu nombre."),
        ],
        "form_value": "Web & Growth",
    },
]

E = html.escape


def nav_html():
    return """  <div class="wrap">
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
      <a class="cta-sm" href="#contact" data-i18n="nav.cta">Book an assessment</a>
    </nav>
  </div>"""


def form_html(selected_value: str) -> str:
    options = [
        ("Software Engineering", "form.o1", "Software Engineering"),
        ("AI &amp; Automation", "form.o2", "AI &amp; Automation"),
        ("Cybersecurity", "form.o3", "Cybersecurity"),
        ("Data &amp; Analytics", "form.o4", "Data &amp; Analytics"),
        ("Technical Delivery", "form.o5", "Technical Delivery &amp; Account Leadership"),
        ("Web &amp; Growth", "form.o7", "Web &amp; Growth"),
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


def build_page(p: dict) -> str:
    slug, url = p["slug"], f"{DOMAIN}/services/{p['slug']}/"

    ledger_in = "\n".join(
        f'            <li data-i18n="pg.in{i+1}">{E(en)}</li>' for i, (en, es) in enumerate(p["in"])
    )
    ledger_out = "\n".join(
        f'            <li data-i18n="pg.out{i+1}">{E(en)}</li>' for i, (en, es) in enumerate(p["out"])
    )

    steps = "\n".join(
        f'      <div class="step"><b>{i+1:02d}</b>'
        f'<h3 data-i18n="pg.step{i+1}t">{E(t_en)}</h3>'
        f'<p data-i18n="pg.step{i+1}d">{E(d_en)}</p></div>'
        for i, (t_en, t_es, d_en, d_es) in enumerate(p["steps"])
    )

    exp = "\n".join(
        f'      <article class="pcase"><span data-i18n="pg.exp{i+1}k">Track record</span>'
        f'<h3 data-i18n="pg.exp{i+1}t">{E(t_en)}</h3>'
        f'<p data-i18n="pg.exp{i+1}d">{E(d_en)}</p></article>'
        for i, (t_en, t_es, d_en, d_es) in enumerate(p["exp"])
    )

    faq = "\n".join(
        f'      <details><summary data-i18n="pg.q{i+1}">{E(q_en)}</summary>'
        f'<p data-i18n="pg.a{i+1}">{E(a_en)}</p></details>'
        for i, (q_en, q_es, a_en, a_es) in enumerate(p["faq"])
    )

    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#service",
                "name": p["title_en"].split(":")[0].strip(),
                "description": p["desc_en"],
                "serviceType": p["title_en"].split(":")[0].strip(),
                "provider": {"@id": DOMAIN + "/#studio"},
                "areaServed": ["MX", "LATAM", "US", "CA"],
                "availableLanguage": ["en", "es"],
                "url": url,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": DOMAIN + "/#practices"},
                    {"@type": "ListItem", "position": 3, "name": p["title_en"].split(":")[0].strip(), "item": url},
                ],
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q_en,
                     "acceptedAnswer": {"@type": "Answer", "text": a_en}}
                    for (q_en, q_es, a_en, a_es) in p["faq"]
                ],
            },
        ],
    }

    return f"""<!doctype html>
<html lang="en" dir="ltr" data-i18n-page="{slug}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(p["title_en"])} | Technical Transformation Studio</title>
<meta name="description" content="{E(p["desc_en"])}">

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
<link rel="alternate" hreflang="es" href="{DOMAIN}/es/servicios/{slug}/">
<link rel="alternate" hreflang="x-default" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(p["title_en"])}">
<meta property="og:description" content="{E(p["desc_en"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/og/{slug}.png">
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
        <a href="/" data-i18n="pg.crumbHome">Home</a>
        <span aria-hidden="true">/</span>
        <a href="/#practices" data-i18n="pg.crumbServices">Practices</a>
        <span aria-hidden="true">/</span>
        <span data-i18n="pg.crumbSelf">{E(p["title_en"].split(":")[0].strip())}</span>
      </nav>
      <p class="kicker" data-i18n="pg.kicker">Practice {p["num"]}</p>
      <h1 data-i18n="pg.h1">{E(p["h1_en"])}</h1>
      <p class="deck" data-i18n="pg.deck">{E(p["deck_en"])}</p>
      <div class="btnrow">
        <a class="btn btn-fill" href="#contact" data-i18n="pg.cta1">Book a technical assessment</a>
        <a class="btn btn-line" href="/#cost" data-i18n="pg.cta2">Calculate what it costs you today</a>
      </div>
    </div>
    <div class="filecard">
      <h2 data-i18n="file.head">Standard engagement record</h2>
      <dl>
        <div class="filerow"><dt data-i18n="file.k1">Entry point</dt><dd data-i18n="file.v1">Technical assessment</dd></div>
        <div class="filerow"><dt data-i18n="file.k2">Duration</dt><dd data-i18n="file.v2">2 weeks</dd></div>
        <div class="filerow"><dt data-i18n="file.k3">You receive</dt><dd data-i18n="file.v3">Findings + roadmap</dd></div>
        <div class="filerow"><dt data-i18n="file.k4">Commitment after</dt><dd data-i18n="file.v4">None</dd></div>
        <div class="filerow"><dt data-i18n="file.k5">Working languages</dt><dd>EN / ES</dd></div>
      </dl>
      <p class="stamp" data-i18n="file.stamp">Scope agreed in writing before work begins.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="pg.problemKicker">The problem</p>
      <h2 class="sect" data-i18n="pg.problemH">{E(p["problem_h_en"])}</h2>
    </div>
    <div class="prose">
      <p data-i18n="pg.problemP1">{E(p["problem_p1_en"])}</p>
      <p data-i18n="pg.problemP2">{E(p["problem_p2_en"])}</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="pg.scopeKicker">Scope</p>
      <h2 class="sect" data-i18n="pg.scopeH">What this includes, and what it does not.</h2>
      <p data-i18n="pg.scopeIntro">Stated before you ask, so the first call is about your problem rather than about what we do or do not cover.</p>
    </div>
    <div class="ledger">
      <div class="in"><h4 data-i18n="ledger.in">Included</h4><ul>
{ledger_in}
      </ul></div>
      <div class="out"><h4 data-i18n="ledger.out">Not included</h4><ul>
{ledger_out}
      </ul></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="pg.howKicker">How it runs</p>
      <h2 class="sect" data-i18n="pg.howH">Four steps, in this order.</h2>
    </div>
    <div class="ladder">
{steps}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="pg.expKicker">Track record</p>
      <h2 class="sect" data-i18n="pg.expH">{E(p["exp_h_en"])}</h2>
    </div>
    <div class="proof">
{exp}
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="band-head">
      <p class="kicker" data-i18n="faq.kicker">Questions</p>
      <h2 class="sect" data-i18n="pg.faqH">Answered before you have to ask.</h2>
    </div>
    <div class="faq">
{faq}
    </div>
  </div>
</section>

<section class="band contact" id="contact">
  <div class="wrap">
    <div>
      <p class="kicker gold" data-i18n="con.kicker">Start here</p>
      <h2 class="sect" data-i18n="pg.conH">Tell us what is broken, slow or expensive.</h2>
      <div class="band-head"><p data-i18n="con.lead">Describe the problem in a few lines. You get a written reply with a first read on it, whether or not there is an engagement in it. The message is sent from this page — no email client, no third-party form service, no trackers.</p></div>
    </div>
{form_html(p["form_value"])}
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


def build_dictionary(p: dict) -> str:
    d = {
        "pg.crumbHome": "Inicio",
        "pg.crumbServices": "Prácticas",
        "pg.crumbSelf": p["title_es"].split(":")[0].strip(),
        "pg.kicker": "Práctica " + p["num"],
        "pg.h1": p["h1_es"],
        "pg.deck": p["deck_es"],
        "pg.cta1": "Agenda un diagnóstico técnico",
        "pg.cta2": "Calcula lo que te cuesta hoy",
        "pg.problemKicker": "El problema",
        "pg.problemH": p["problem_h_es"],
        "pg.problemP1": p["problem_p1_es"],
        "pg.problemP2": p["problem_p2_es"],
        "pg.scopeKicker": "Alcance",
        "pg.scopeH": "Qué incluye esto y qué no.",
        "pg.scopeIntro": "Declarado antes de que preguntes, para que la primera llamada sea sobre tu problema y no sobre qué cubrimos y qué no.",
        "pg.howKicker": "Cómo se ejecuta",
        "pg.howH": "Cuatro pasos, en este orden.",
        "pg.expKicker": "Trayectoria",
        "pg.expH": p["exp_h_es"],
        "pg.faqH": "Respondidas antes de que tengas que preguntar.",
        "pg.conH": "Cuéntanos qué está roto, lento o caro.",
        "pg.backHome": "Volver a todas las prácticas",
    }
    for i, (en, es) in enumerate(p["in"]):
        d[f"pg.in{i+1}"] = es
    for i, (en, es) in enumerate(p["out"]):
        d[f"pg.out{i+1}"] = es
    for i, (t_en, t_es, d_en, d_es) in enumerate(p["steps"]):
        d[f"pg.step{i+1}t"] = t_es
        d[f"pg.step{i+1}d"] = d_es
    for i, (t_en, t_es, d_en, d_es) in enumerate(p["exp"]):
        d[f"pg.exp{i+1}k"] = "Trayectoria"
        d[f"pg.exp{i+1}t"] = t_es
        d[f"pg.exp{i+1}d"] = d_es
    for i, (q_en, q_es, a_en, a_es) in enumerate(p["faq"]):
        d[f"pg.q{i+1}"] = q_es
        d[f"pg.a{i+1}"] = a_es

    body = ",\n".join(f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}'
                      for k, v in d.items())
    return (f'/* Español — página de servicio "{p["slug"]}".\n'
            f'   Se fusiona sobre i18n/es.js (común). Generado por tools/build_pages.py:\n'
            f'   edita el contenido allí y vuelve a generar, no este archivo. */\n'
            f'window.ttsRegisterDictionary("es", {{\n{body}\n}});\n')


def build_sitemap() -> str:
    """Incluye portada, prácticas, índice de casos y cada caso.
    Los slugs de casos se leen de build_cases.py para no duplicar la lista."""
    try:
        import build_cases
        case_slugs = [c["slug"] for c in build_cases.CASES]
    except Exception:
        case_slugs = []

    urls = [(DOMAIN + "/", "1.0", "")]
    urls += [(f"{DOMAIN}/services/{p['slug']}/", "0.8", p["slug"]) for p in PAGES]
    if case_slugs:
        urls.append((DOMAIN + "/work/", "0.7", "work"))
        urls += [(f"{DOMAIN}/work/{s}/", "0.6", "work/" + s) for s in case_slugs]
    entries = []
    for loc, priority, slug in urls:
        alt_es = f"{DOMAIN}/es/servicios/{slug}/" if slug else f"{DOMAIN}/es/"
        entries.append(f"""  <url>
    <loc>{loc}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="{loc}"/>
    <xhtml:link rel="alternate" hreflang="es" href="{alt_es}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>
    <lastmod>2026-08-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(entries) + "\n</urlset>\n")


def main() -> None:
    for p in PAGES:
        out_dir = ROOT / "services" / p["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_page(p), encoding="utf-8")
        (ROOT / "i18n" / f"{p['slug']}.es.js").write_text(build_dictionary(p), encoding="utf-8")
        print(f"  services/{p['slug']}/index.html  +  i18n/{p['slug']}.es.js")

    (ROOT / "sitemap.xml").write_text(build_sitemap(), encoding="utf-8")
    print("  sitemap.xml")
    print(f"\n{len(PAGES)} páginas generadas.")


if __name__ == "__main__":
    main()
