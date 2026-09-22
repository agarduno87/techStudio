# Datara Hub  (repositorio: techStudio)

Hub técnico de Antonio Garduño, Samuel González y Ricardo Vázquez. Software,
automatización con IA, ciberseguridad, datos e ingeniería, delivery y web. Base
en Querétaro, México.

**Nombre decidido: Datara Hub.** Dominio elegido: `datarahub.com` (verificado
libre por RDAP; falta comprarlo). El REPOSITORIO sigue llamándose `techStudio`,
así que el build de Pages usa `--base /techStudio`. La marca visible, el logo
(**cometa** esmeralda, ya no el monograma "DH"), títulos, OG y JSON-LD dicen
"Datara Hub". Para cambiar el dominio en todo el repo de un tiro:
`python3 tools/set_domain.py <url>`.

## Estado

- Sitio estático completo: portada, About, Work, 5 páginas de servicio, legales
- **Diseño de producción: "datarahub" (oscuro).** Ganó sobre el "Dossier"
  (claro) y ya es el main en Pages. Ver la sección "El diseño" abajo.
- Backend FastAPI para el formulario, con SQLite (para VPS). Para hosting cPanel
  hay un reemplazo en PHP listo: `php/contact.php` (ver "El formulario").
- 45 pruebas de backend (44 en verde; el rojo `test_openapi_docs_disabled` es
  preexistente: la carpeta `docs/` comprometida ensombrece la ruta `/docs`)
- Publicado en https://agarduno87.github.io/techStudio/
- Repositorio: github.com/agarduno87/techStudio  (PÚBLICO — ver "Material privado")
- Cotizador de marca en `cotizacion/cotizacion.html` (ver "El cotizador")

## El diseño (datarahub, oscuro)

Existían dos pieles: "Dossier" (claro, navy/dorado/paper) y "datarahub"
(oscuro, esmeralda/azul). **Ganó datarahub y se horneó en la fuente**, así que
el build normal ya produce el sitio oscuro. Lo que quedó:

- `styles.css` ES el sistema oscuro (tokens `--bg:#08131A`, `--emerald:#10B981`,
  `--blue:#3B82F6`, `--ink:#EAF1F4`).
- El cometa de la cabecera es esmeralda en todas las páginas (fuente +
  generadores). `theme-color` oscuro (`#08131A`).
- El grid de prácticas "de un vistazo" está horneado en el home (`index.html`).
- Favicon y tarjetas OG en variante esmeralda sobre navy.
- **Se retiró la maquinaria del preview**: ya no existen
  `build_preview_datarahub.py`, `styles-datarahub.css` ni `docs/datarahub/`.
  Si buscas el diseño oscuro, es el único que hay: `styles.css`.

## Hosting

Hoy: GitHub Pages, carpeta `/docs` de la rama `main`.

**Plan decidido: Neubox cPanel** (el usuario quiere correos `@datarahub.com` y
que los leads se guarden). Recomendación: plan **"Tell It" (~$490 MXN el primer
año)** — cubre de sobra un sitio estático + `contact.php` + MySQL + correo, e
incluye dominio gratis el 1er año. Subir a "Sell It" solo si van a alojar varios
sitios de clientes o quieren soporte por teléfono/chat. Al contratar, confirmar:
PHP 8 + MySQL, SSL/HTTPS gratis (Let's Encrypt) y que el dominio gratis sea `.com`.

El registrador es separable del hosting: se puede comprar el dominio donde sea
(OVH salía barato a 3 años) y apuntar DNS a Neubox. Pero si el plan trae dominio
gratis, lo más simple es registrarlo ahí y tener todo en un lugar.

## El formulario

- **En Pages no funciona** (no hay backend): el generador inyecta un script que
  abre el correo del visitante con los datos. No guarda leads.
- **FastAPI** (`api/main.py`): el backend "real", para un VPS. SQLite.
- **PHP** (`php/contact.php`): reemplazo directo de `POST /api/contact` para
  Neubox/cPanel. Mismas defensas (honeypot, trampa de tiempo, rate limit con
  hash de IP salado, validación, IP anonimizada, correo saneado). Guarda en
  MySQL y avisa por `mail()`. Trae `config.sample.php` (→ `config.php` en el
  servidor, fuera de git), `schema.sql`, `.htaccess` y `README.md`.
  **Para activarlo:** cambiar `API_ENDPOINT` a `"/contact.php"` en `app.js`
  (hoy apunta a `/api/contact`; se deja así hasta migrar a Neubox).

## El cotizador

`cotizacion/cotizacion.html` — hoja de cotización de marca, autocontenida
(un solo HTML, tipografías de Google Fonts con fallback). Editable en el
navegador, guarda el borrador en `localStorage` (llave `datarahub-cotizacion-v1`),
se imprime a PDF. Catálogo de servicios con los precios reales, moneda MXN/USD,
IVA 16%, y todo lo monetario en formato peso. Diseño claro/papel a propósito
(se imprime mejor) con acentos navy/esmeralda y el cometa.

Trampas de impresión que ya se resolvieron (por si se vuelven a tocar):
- La marca de agua (cometa de fondo) debe ir `position:absolute` con selector
  específico (`.sheet > .watermark`), o `.sheet > *` le gana y la mete al flujo,
  empujando todo hacia abajo.
- Firmas + pie anclados al fondo con `.sheet{display:flex;flex-direction:column;
  min-height:255mm}` + `.signoff{margin-top:auto}` en `@media print`.
- La ruta `file://`, fecha y número de página que salen al imprimir NO son del
  HTML: son el encabezado/pie del navegador. Se apagan con el check
  "Encabezados y pies de página" del diálogo de impresión.
- La carpeta está en `.gitignore` (material comercial privado, ver abajo).

## Trampas de este proyecto

**Rutas absolutas y GitHub Pages.** Los enlaces del sitio son `/about/`,
`/work/`, `/services/...`. En local el sitio vive en la raíz y funcionan. En
Pages vive en `agarduno87.github.io/techStudio/`, así que `/about/` apunta fuera
del repositorio y da 404. Por eso existe `tools/build_github_pages.py`, que
reescribe las rutas a `/techStudio/...` y deja el resultado en `docs/`.

**Dos generadores con nombre parecido. No confundirlos.**

    tools/build_pages.py         genera las 5 páginas de /services/
    tools/build_github_pages.py  empaqueta el sitio entero en docs/

El segundo se llamaba `build_pages.py` y sobrescribió al primero en un paquete
entregado. De ahí el nombre distinto.

**srcset.** Al reescribir rutas hay que tratar `srcset` aparte: lleva varias
rutas separadas por coma con descriptores, y una expresión que solo cubra
`href` y `src` no las ve. El síntoma es engañoso: la imagen da 404 pero el
navegador cae al `src` de respaldo, así que solo aparece en la consola.

**Content-Security-Policy.** Va por cabecera HTTP, nunca en un `<meta>`. Con el
CSS en un bloque `<style>` inline, `style-src 'self'` bloquea la hoja completa y
la página sale en texto plano. GitHub Pages no permite cabeceras propias, así
que ahí el sitio queda sin CSP.

**El repo es PÚBLICO.** Todo lo que se commitea se ve en GitHub. Para material
comercial hay una carpeta `private/` ignorada por completo (ver "Material
privado"). `.gitignore` sólo evita subir lo que aún NO está en git: si algo
sensible ya se commiteó, hay que sacarlo del historial (pasó con una auditoría;
se purgó con `git filter-branch` + force-push).

**El favicon se cachea con ganas.** El navegador no lo refresca aunque el
archivo cambie. Por eso los `<link rel="icon">` llevan `?v=N` en todas las
páginas; al cambiar el ícono, sube el número (`?v=3`) y se propaga solo.

## Material privado (repo público)

Regla simple: **todo lo sensible va en `private/`**, que git ignora completa.
También `cotizacion/`. En `.gitignore`, además, hay red de seguridad por nombre
(`costos`, `financ`, `estrategia`, `auditoria`, `cotización`). Ahí viven costos,
finanzas, modelos de negocio, estrategia y auditorías — nunca en el repo.
`php/config.php` (credenciales de Neubox) también está ignorado.

## Orden al publicar

    python3 tools/build_pages.py                  # si cambiaron las páginas de servicio
    python3 tools/build_github_pages.py --base /techStudio --mailto ing.antoniogz@gmail.com
    git add -A && git commit -m "..." && git push

El `--base` tiene que coincidir exactamente con el nombre del repositorio.

## Convenciones

- Español informal al conversar; el sitio está en inglés con español completo
- Contenido y presentación separados: los textos no se editan dentro del HTML
  de las páginas generadas, sino en el script que las genera
- Antes de proponer un nombre de marca o dominio, verificarlo. Ver la skill
  `naming-branding`: la regla existe porque se propuso "Groma" sin comprobar y
  el dominio pertenecía a una startup con Serie A de 20 millones

## Pendientes

- **Contratar hosting Neubox** ("Tell It", confirmando PHP/MySQL, SSL y dominio
  `.com` gratis). Nota: el usuario paga; Claude no hace la compra.
- **Comprar / registrar `datarahub.com`** (gratis con el plan, o en OVH y apuntar
  DNS a Neubox).
- **Poner el formulario en producción en Neubox:** crear base MySQL + buzón
  `leads@datarahub.com`, subir `php/`, copiar `config.php`, y cambiar
  `API_ENDPOINT` a `"/contact.php"` en `app.js`.
- Cuando el dominio esté vivo: `python3 tools/set_domain.py https://datarahub.com`.
- Publicar desde `/docs` en Settings → Pages (hoy publica la raíz del repo).
- Editor de contenido para que Samuel también edite sin tocar código.
- (Opcional) Versionar el cotizador para Samuel — hoy está en `cotizacion/`
  pero ignorado por git.
