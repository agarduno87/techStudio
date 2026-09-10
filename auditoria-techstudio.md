# Auditoría SEO + GEO — techStudio (Technical Transformation Studio)

- **Fecha:** 2026-09-10 (2ª pasada, tras aplicar los fixes de nuestro lado)
- **URL auditada (viva):** https://agarduno87.github.io/techStudio/ (GitHub Pages, project page)
- **Dominio de producción:** ❌ **no existe todavía** — el nombre no está decidido y no hay dominio comprado. Todo el sitio referencia el placeholder `https://tu-dominio.com` (swappable de un tiro con `tools/set_domain.py`).
- **Plataforma:** sitio estático (HTML/CSS/JS) + backend FastAPI (dev); producción prevista en PHP/Neubox.
- **Salud SEO:** 70/100 🟡 (hygiene técnica ya corregida; quedan dominio, deploy y ES indexable).
- **Salud GEO:** 55/100 🟡 (`llms.txt` + `robots.txt` pro-IA + nodo `WebSite`/`Organization` ya listos; falta el dominio vivo e indexable).
- **Pruebas del proyecto:** 44/45 backend + 18/15/27/13 navegador en verde (el 1 rojo es preexistente: `docs/` tapa `/docs`).

### Cambios aplicados en esta 2ª pasada
- ✅ `llms.txt` publicado (espeja el sitio: qué es, 6 prácticas, precios, equipo, fronteras; sin inventar nada).
- ✅ `robots.txt` pro-IA (permite GPTBot/OAI-SearchBot/ChatGPT-User/PerplexityBot/ClaudeBot/Claude-Web/Google-Extended; bloquea CCBot/Bytespider/Applebot-Extended/Amazonbot).
- ✅ Nodo `WebSite` + `Organization` agregados al JSON-LD de la portada.
- ✅ Metadatos acortados: todos los `<title>` ≤ 56 car. y descriptions ≤ 162 (antes: about 252, software-eng title 109). El home decía "Five" → **Six**.
- ✅ hreflang roto (`/es/…` 404) eliminado; canonical auto-referencial + `x-default`.
- ✅ `tools/set_domain.py`: cambia el dominio en todo el repo con un comando.
- ✅ Hardening: los `.md` (README, CLAUDE.md, esta auditoría) ya no se sirven públicamente (bloqueados en el server y en el build de Pages).

---

## 1. Resumen ejecutivo

Lo bueno: la **base de contenido y de datos estructurados es sólida** — JSON-LD rico (ProfessionalService + 6 Service + FAQPage), Open Graph completo, títulos/descripciones únicos por ruta, sitemap con `lastmod` estable, y volumen real (~1,694 palabras en portada, 6 páginas de servicio de 800+ palabras cada una). Como base, está mejor armado que muchos sitios en vivo.

Los cinco problemas de fondo:

1. **No hay dominio ni nombre decidido.** Canonical, og:url, hreflang, JSON-LD `@id` y el sitemap apuntan **52 veces** a `tu-dominio.com`, que no existe. Sin un dominio real y vivo, ni Google ni las IA pueden indexar o citar nada. Es el bloqueo raíz, y está aguas arriba de todo lo demás.
2. **Los enlaces internos son rutas absolutas y se rompen en vivo.** En Pages (project page bajo `/techStudio/`), el nav apunta a `/about/`, `/site.webmanifest`, etc., que resuelven a la raíz de la cuenta → **404**. Las páginas existen en `/techStudio/about/` (200), pero el sitio enlaza mal. Rompe navegación, rastreo y compartir.
3. **hreflang apunta a URLs `/es/` que no existen.** El español se sirve por un toggle de JavaScript en la **misma** URL, pero el HTML declara `hreflang="es" href=".../es/nosotros/"`. Esas URLs dan 404 y, peor, **la versión en español no existe como HTML indexable**: Google solo ve el inglés.
4. **GEO casi ausente.** No hay `llms.txt`, el `robots.txt` es genérico (no da la bienvenida explícita a los bots generativos ni bloquea los de solo-entrenamiento), y falta el nodo `WebSite`/`Organization` en el JSON-LD.
5. **Metadatos largos.** Varios títulos y descripciones exceden el límite y se truncan en el buscador (about description **252** car., software-engineering title **109** car.).

---

## 2. Tabla de hallazgos

| # | Sev | Hallazgo | Evidencia |
|---|-----|----------|-----------|
| 1 | 🔴 | Sin dominio ni nombre; todo referencia `tu-dominio.com` | `grep -rc tu-dominio.com` → sitemap 52, index 13, about 7, cada servicio 7 |
| 2 | 🔴 | Enlaces internos absolutos → 404 en vivo en Pages | nav a `/about/` → `curl .../about/` = **404**; `/techStudio/about/` = **200**; `site.webmanifest` 404 en consola |
| 3 | 🟠 | hreflang a `/es/` inexistentes; el ES es solo-JS, no indexable | **parcial**: hreflang roto eliminado ✅; el ES indexable (páginas `/es/` reales) sigue pendiente |
| 4 | ✅ | ~~No existe `llms.txt`~~ → **publicado** | `curl <base>/llms.txt` → 200 |
| 5 | ✅ | ~~`robots.txt` no pro-IA~~ → **pro-IA** | `curl <base>/robots.txt` → GPTBot/ClaudeBot allow, CCBot/Bytespider disallow |
| 6 | ✅ | ~~Falta `WebSite`/`Organization`~~ → **agregados** | JSON-LD portada parsea con `WebSite` + `Organization` |
| 7 | ✅ | ~~Metadatos largos~~ → **acortados** | títulos ≤ 56, descriptions ≤ 162; home "Five"→"Six" |
| 8 | 🟡 | Sin Search Console / Bing / analítica | requieren cuentas del cliente + dominio vivo |
| 9 | 🟡 | og:image apunta a `tu-dominio.com` (no cargará al compartir) | se resuelve al fijar el dominio real con `set_domain.py` |

---

## 3. Diagnóstico GEO (para que las IA citen el sitio)

- ✅ **JSON-LD** bueno como base: las IA pueden entender qué es el estudio, sus 6 servicios y el FAQ.
- ❌ **`llms.txt`**: no existe. Es el índice que leen los motores generativos.
- ❌ **`robots.txt` pro-IA**: no da la bienvenida explícita a GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot, Claude-Web, Google-Extended, ni bloquea CCBot/Bytespider/Applebot-Extended/Amazonbot.
- ❌ **Nodo `WebSite`/`Organization`**: falta el ancla de marca.
- ❌ **Bloqueo real:** no hay dominio vivo **ni nombre de marca**. No hice `web_search`/`site:` en vivo porque no hay entidad que consultar — sería 0 resultados por definición. Este es el paso 0.

---

## 4. SERP y competencia

Pendiente hasta que exista nombre + dominio (antes no hay nada que posicionar). Criterio de la metodología: **no pelear genéricos gigantes** ("software", "ciberseguridad", "consultoría" a secas). El ángulo ganable de techStudio:

- **Nicho + localidad + formato:** "diagnóstico técnico de dos semanas Querétaro", "pentesting de aplicación web con autorización México", "automatización de reportes con IA Bajío", "equipo técnico senior fraccional sin contratar".
- **Diferenciador honesto y ya escrito en el sitio:** *alcance por escrito, dos/tres seniors (sin pirámide), te entregamos el código*. Ese copy es material de contenido y de GEO.

---

## 5. Wizard de ejecución

### Pasos de NUESTRO lado (ejecutables — algunos requieren el nombre)

**PASO 1 — Decidir nombre y comprar dominio.** 🔴 BLOQUEO RAÍZ
- Problema: sin dominio, nada indexa ni se cita. Usar la skill `naming-branding` (verificar disponibilidad ANTES de proponer).
- Al cerrarlo: centralizar el dominio en una sola variable (hoy `DOMAIN = "https://tu-dominio.com"` está en `tools/build_pages.py`, `build_about.py` e index.html) y reemplazar de un tiro.
- Verificar: `curl -sI https://<dominio-real>/ | head -1` → `200`.

**PASO 2 — Publicar bien (arreglar los 404 de enlaces internos).** 🔴
- Problema: en Pages los enlaces absolutos rompen; en un dominio a raíz funcionarán solos.
- Opción A (Pages como staging): `python3 tools/build_github_pages.py --base /techStudio --mailto <correo>` (reescribe todo a `/techStudio/...`) + Settings → Pages → carpeta `/docs`.
- Opción B (producción): servir en la **raíz** del dominio en Neubox → las rutas absolutas jalan sin reescritura.
- Verificar: `curl -sI <base>/about/ | head -1` → `200` navegando desde el nav.

**PASO 3 — `llms.txt`.** 🟠 EJECUTABLE YA (espeja el sitio, sin inventar)
- Índice con qué es/qué no es el estudio, las 6 prácticas, el punto de entrada (diagnóstico 2 sem), idiomas, y los precios ya publicados. Usa el dominio real cuando exista; mientras, se puede dejar listo.
- Verificar: `curl -s <base>/llms.txt | head`.

**PASO 4 — `robots.txt` pro-IA.** 🟠 EJECUTABLE YA
- Permitir bots generativos, bloquear los de solo-entrenamiento, `Disallow: /api/`, y `Sitemap:` con el dominio real.
- Verificar: `curl -s <base>/robots.txt`.

**PASO 5 — Nodo `WebSite` + `Organization` en el JSON-LD.** 🟠 EJECUTABLE YA
- Agregar `WebSite` (con `name`, `url`, `inLanguage`) y `Organization` (con `logo`) al `@graph` de la portada.
- Verificar: `grep -c '"@type":"WebSite"' index.html` → `1`.

**PASO 6 — Acortar metadatos.** 🟠 EJECUTABLE YA
- title ≤ 60 car., description ≤ 160. Prioridad: about (252→~150), software-engineering (109→~60), web-growth (95→~60), home (78→~60). Editar en los generadores, no en el HTML.

**PASO 7 — Resolver el hreflang / el español indexable.** 🟠 DECISIÓN
- Corto plazo: quitar los `hreflang="es"` que apuntan a 404 y dejar canonical auto-referencial + `x-default` (para no declarar URLs que no existen).
- Largo plazo (proyecto aparte): generar páginas `/es/...` reales para que el español sea indexable, no solo un toggle JS.

### Pasos del CLIENTE (pendientes, requieren cuentas/datos)

- **C1** — Search Console + Bing Webmaster (verificar dominio, mandar sitemap). Requiere dominio vivo.
- **C2** — Analítica (Plausible/GA4) — decisión de privacidad.
- **C3** — Foto real de Ricardo (hoy placeholder "RV").
- **C4** — Número/estrategia de leads en Pages: hoy no persisten (sin backend); en Neubox van a PHP.

---

## 6. Roadmap

- **0–30 días (fuego):** PASO 1 (nombre + dominio) → PASO 2 (publicar bien) → PASOS 3–6 (llms.txt, robots pro-IA, WebSite, metadatos) → C1 (Search Console/Bing).
- **30–90 días:** C2 analítica; 3–4 artículos de contenido (qué es un diagnóstico técnico, "alcance por escrito", automatización de reportes con IA, exposición externa) enlazando al formulario; resolver el ES indexable (PASO 7 largo plazo).
- **90–180 días:** monitoreo GEO (¿citan el dominio real?), afinar por queries que traen tráfico, decidir blog sostenido con guardarraíles.

---

## 7. Queries objetivo (sembrado) y no objetivo

**Sí:** "diagnóstico técnico de dos semanas Querétaro", "pentesting de aplicación web con autorización México", "automatización de reportes con IA Bajío", "equipo técnico senior sin contratar", "sitio web que convierte Querétaro".
**No (genéricas gigantes):** "software", "ciberseguridad", "consultoría", "desarrollo web" a secas.

---

## 8. Lo que YA está bien (no tocar)

- JSON-LD rico y válido (ProfessionalService + 6 Service + FAQPage).
- Open Graph completo; títulos/descripciones únicos por ruta.
- Sitemap con `lastmod` estable (2026-08-15) y 13 URLs (portada + 6 prácticas + índice de casos + 5 casos).
- Contenido profundo: portada ~1,694 palabras; 6 páginas de servicio de 800+ palabras; About 919.
- Estructura semántica, accesibilidad, CSP, y el botón de WhatsApp ya en vivo.

---

## Apéndice — comparación con Logistika

| | Logistika | techStudio |
|---|---|---|
| Dominio | `logistika.mx` reservado (falta publicar) | ❌ sin nombre ni dominio |
| Enlaces internos en vivo | OK (raíz) | ❌ 404 (subruta Pages, rutas absolutas) |
| hreflang | ES/EN correcto | ❌ apunta a `/es/` 404 |
| llms.txt | ✅ | ❌ |
| robots pro-IA | ✅ | ❌ |
| WebSite node | ✅ | ❌ |
| Contenido | ~1,840 palabras portada | ~1,694 palabras portada |
| **SEO / GEO** | **80 / 60** | **55 / 35** |

techStudio tiene una base de contenido comparable, pero va una fase atrás: Logistika ya tiene dominio y los tres artefactos de GEO; techStudio necesita primero **nombre + dominio**, y luego los mismos fixes de GEO que ya se hicieron en Logistika.
