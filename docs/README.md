# Technical Transformation Studio — sitio comercial (MVP)

Página de servicios "Dossier": cinco prácticas con el mismo peso, cada una con su
ledger de alcance, más la calculadora del costo del trabajo manual. Inglés y español,
con la calculadora en la moneda de cada idioma.

---

## Arrancar (un solo comando)

```bash
cd /Users/antoniogarduno/Documents/techStudio/techStudio
bash run.sh
```

Abre **http://127.0.0.1:8000**

Usa `bash run.sh` y no `./run.sh`: al descomprimir un ZIP, macOS suele perder el bit
de ejecución. Si prefieres el atajo, primero `chmod +x run.sh`.

Otro puerto: `bash run.sh 8080`

`run.sh` verifica la versión de Python, comprueba que el puerto esté libre, crea el
entorno virtual, instala dependencias, copia `api/.env` desde la plantilla si no
existe, y levanta el servidor.

### No abras `index.html` con doble clic

Con `file://` el navegador bloquea partes del sitio y verás errores que no existen al
servirlo: el cambio de idioma no aplica y el formulario no puede enviar porque no hay
servidor detrás. **Ese fue el problema del paquete anterior.** Este ya te avisa en
pantalla si lo abres así, en vez de fallar en silencio — pero la forma correcta sigue
siendo `bash run.sh`.

---

## Probar

**Backend y servidor de estáticos** (18 pruebas, sin dependencias extra):

```bash
source .venv/bin/activate
python api/test_api.py
```

Cubre: la portada se sirve, los assets cargan, las cabeceras de seguridad salen,
**el código fuente y la base de leads NO se pueden descargar**, honeypot, trampa de
tiempo, rate limit, práctica desconocida, correo inválido, caracteres de control,
mensaje sobredimensionado, `/api/leads` cerrado y docs de OpenAPI apagadas.

Con pytest, si lo prefieres: `pip install pytest && pytest api/test_api.py -v`

**Frontend** (27 comprobaciones en un DOM real, opcional, requiere Node):

```bash
npm install jsdom
node tests/frontend.check.js
```

Cubre: el selector aparece, la traducción se aplica a todas las claves, la moneda
cambia con el idioma, la aritmética da el número correcto en ambas monedas, el `value`
de los `<option>` sigue en inglés, el menú expone `aria-expanded`, y la validación del
formulario responde en el idioma activo.

**Prueba manual rápida**

1. http://127.0.0.1:8000 → mueve los sliders, verifica `USD`
2. Cambia a Español → los mismos sliders ahora en `MXN`, y la URL queda con `?lang=es`
3. Llena el formulario y envía → debe decir "Mensaje enviado"
4. `sqlite3 api/leads.db "select * from leads;"` → ahí está el lead

---

## La calculadora y la moneda

Inglés → **USD**. Español → **MXN**. El código de moneda se muestra siempre
(`MXN 460,800`, no `$460,800`) porque el peso y el dólar comparten el símbolo `$` y la
cifra sería ambigua justo donde más importa.

**No hay conversión de tipo de cambio, y es deliberado.** Cada idioma trae su propio
rango de costo por hora: USD 5–120, MXN 100–2,000. Razones:

- El visitante conoce lo que le cuesta una hora de su gente **en su moneda**. Pedirle
  que piense en dólares convertidos le agrega fricción sin darle precisión.
- Un tipo de cambio fijo en el código es mentira en cuestión de semanas.
- Uno en vivo obligaría a llamar a una API de terceros, lo que rompe `connect-src
  'self'` y mete una dependencia externa en una página que hoy no tiene ninguna.

Al cambiar de idioma se conservan *personas* y *horas*; solo la tarifa vuelve a su
valor de referencia para esa moneda. Si prefieres conversión real, se puede hacer con
una tasa que tú actualices en `i18n.js` — dilo y lo cambio.

Los precios de la escalera (Assessment, MVP, Implementación, Retainer) se quedan en
USD en ambos idiomas: son **tus tarifas**, y vendes a varios países. La calculadora
mide el costo interno del cliente, que sí es local. Son dos cosas distintas a propósito.

---

## Idiomas

Inglés es el idioma fuente y vive en el HTML. Cada otro idioma es un archivo en
`i18n/` que se carga solo cuando alguien lo elige.

Los diccionarios se cargan como `<script src>`, no por `fetch` de JSON: un fetch local
se bloquea al abrir con `file://`, que es justo el primer escenario en el que uno
prueba. Así funciona por http y por file.

**Agregar un idioma:**

1. `cp i18n/_template.js i18n/<code>.js` — cambia `"xx"` por el código y traduce.
2. Agrega la entrada a `LOCALES` en `i18n.js`, con su moneda y su rango de tarifa.
3. Agrega el `<link rel="alternate" hreflang>` en `index.html`.

Las claves vacías caen automáticamente al inglés, así que puedes traducir por partes
sin romper nada. Para árabe, hebreo, persa o urdu basta `dir: "rtl"`: el CSS ya está.

Para Google, además, pre-renderiza una URL estática por idioma (`/es/`) con `hreflang`
recíproco. El conmutador es para el visitante; la traducción en cliente no se indexa.

---

## Errores comunes y su causa

| Lo que ves | Qué pasa | Solución |
|---|---|---|
| Abres el HTML y el idioma no cambia | Lo abriste con `file://` | `bash run.sh` |
| `Permission denied: ./run.sh` | El ZIP perdió el bit de ejecución | `bash run.sh` o `chmod +x run.sh` |
| `externally-managed-environment` | pip contra el Python del sistema en macOS | `run.sh` ya usa venv; si falla, reintenta solo |
| `Address already in use` | El puerto está ocupado | `bash run.sh 8001` |
| `No se pudo crear el entorno virtual` | Falta `python3-venv` o el disco no soporta symlinks | `run.sh` reintenta con `--copies` y luego sin venv |
| El formulario dice "Problema de conexión" | La API no está corriendo | Levántala con `run.sh` |
| Llega el lead pero no el correo | SMTP vacío en `api/.env` | Normal en local; llena SMTP para producción |
| `ModuleNotFoundError: email_validator` | Falta el extra de pydantic | `pip install "pydantic[email]"` |

---

## Google Search Console

No se programa: es una herramienta gratuita de Google que se configura una vez, en
unos diez minutos, y después solo se consulta. Hace tres cosas que no puedes obtener
de otro lado — te dice por qué búsquedas apareces, en qué posición y cuántos clics
te dan; te avisa si Google no puede indexar una página; y te deja enviar el sitemap
para que descubra las cinco páginas de servicio sin esperar a rastrearlas solo.

**Pasos**

1. Entra a Search Console y agrega una propiedad. Elige **Dominio** si puedes editar
   el DNS (cubre www, no-www, http y https de una vez); elige **Prefijo de URL** si
   prefieres no tocar el DNS.
2. Verifica la propiedad:
   - **Dominio** → Google te da un registro TXT que pegas en el DNS de tu proveedor.
     Es el método recomendado: no toca el código y sobrevive a cualquier rediseño.
   - **Prefijo de URL** → te da un `<meta name="google-site-verification">`. En
     `index.html` ya está el hueco comentado justo antes del canonical: descoméntalo
     y pega el token.
3. Envía el sitemap: en Sitemaps, escribe `sitemap.xml` y dale enviar.
4. Espera. Los datos tardan dos o tres días en aparecer y unas semanas en volverse
   útiles. No es señal de que algo esté mal.

Lo mismo aplica para Bing Webmaster Tools, que además importa la configuración de
Search Console de un clic. Vale los cinco minutos: Bing alimenta a varios
asistentes de IA.


---

## Archivos

```
index.html              portada
services/<slug>/        cinco páginas de servicio (generadas)
work/                   índice de casos y cinco casos (generados)
tools/build_pages.py    generador de prácticas y sitemap — edita el contenido AQUÍ
tools/build_cases.py    generador de casos — edita el contenido AQUÍ
tools/build_favicon.py  generador de los iconos del sitio
tools/build_about.py    generador de la página About — biografías AQUÍ
tools/build_portraits.py procesa los retratos de assets/portraits/
tools/build_legal.py    aviso de privacidad y términos
tools/build_og.py       tarjetas Open Graph
about/ legal/ img/ og/  salidas generadas
styles.css              sistema visual Dossier (navy + dorado, tipografías del sistema)
app.js                  navegación, calculadora y envío del formulario
i18n.js                 motor de idiomas y monedas
i18n/es.js              diccionario español
i18n/_template.js       plantilla con las 181 claves para un idioma nuevo
run.sh                  arranque de un comando
_headers                cabeceras de seguridad para hosting estático
robots.txt · sitemap.xml
tests/frontend.check.js pruebas de frontend (opcional, jsdom)
api/main.py             servidor: API de contacto + sitio estático
api/test_api.py         pruebas del backend
api/requirements.txt
api/.env.example        plantilla de configuración
```

Un solo proceso sirve el sitio y la API. No es un atajo: elimina de raíz los problemas
de CORS, hace que `/api/contact` resuelva sin proxy y mantiene la CSP cerrada con
`connect-src 'self'`.

---

## Avisos de leads sin montar correo

Un correo transaccional necesita un remitente verificado, y eso normalmente
significa dominio propio. Mientras tanto hay una opción mejor: un webhook.

En `api/.env`:

```
NOTIFY_CHANNEL=telegram
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

**Cómo sacar los dos valores de Telegram**, en unos cinco minutos:

1. En Telegram, escribe a **@BotFather** y manda `/newbot`. Elige nombre y
   usuario. Te devuelve el token.
2. Manda cualquier mensaje a tu bot recién creado.
3. Abre `https://api.telegram.org/bot<TU_TOKEN>/getUpdates` en el navegador. El
   número en `"chat":{"id":...}` es tu `TELEGRAM_CHAT_ID`.

Sirve igual con Slack o Discord: `NOTIFY_CHANNEL=slack` (o `discord`) más
`WEBHOOK_URL` con la URL del webhook entrante del canal.

Por qué webhook y no correo, hoy: no necesita dominio, ni DNS, ni SPF/DKIM, ni
cuidar reputación de remitente, y el lead te llega al teléfono en segundos en
lugar de perderse entre doscientos correos. Cuando tengas dominio, las APIs de
correo transaccional (Resend, Brevo, Postmark) son un POST HTTPS con una llave —
tampoco son SMTP — y conviven con el webhook: puedes tener los dos.

El bloque SMTP sigue en el `.env` por si algún día lo quieres. Se deja apagado.

**Un arreglo que venía de antes:** la notificación ahora corre en
`BackgroundTasks`, después de responderle al visitante. Antes se ejecutaba
dentro del endpoint `async` con un `smtplib` bloqueante de hasta 15 segundos: si
el servidor de correo tardaba, el event loop se congelaba y el sitio entero
dejaba de responder. Una notificación lenta nunca debe hacer esperar a quien
acaba de enviar el formulario.

---

## Página About y retratos

`/about/` presenta a las dos personas del estudio. Se genera con
`tools/build_about.py`, donde viven las biografías en inglés y español.

Los retratos se procesan con `tools/build_portraits.py`: recorta, unifica en
escala de grises y exporta WebP y JPEG en dos anchos. Los originales viven en
`assets/portraits/` y **no se sirven** — el servidor los bloquea, igual que al
código fuente.

```bash
python3 tools/build_portraits.py assets/portraits/1-antonio.jpeg assets/portraits/2-samuel.png
python3 tools/build_about.py
```

Si cambias una foto y el encuadre no queda, ajusta la tupla de esa persona en
`PEOPLE` dentro de `build_portraits.py`: son centro X, centro Y y lado del
recorte, en proporción del original.

**Dos cosas pendientes antes de publicar esta página:**

1. **El visto bueno de Samuel, por escrito**, sobre el texto exacto y la foto
   exacta. Es su imagen y su biografía; el consentimiento verbal no basta.
2. **Los nombres de los empleadores.** Ninguna de las dos biografías nombra a las
   empresas donde trabajaron, a propósito y explicado en la cabecera de
   `build_about.py`. Cuando el contrato laboral esté revisado, cambiarlo es una
   línea por persona.

---

## Imágenes sociales (Open Graph)

`tools/build_og.py` genera una tarjeta de 1200×630 por página, en `og/`. Es lo
que se ve cuando alguien comparte una liga por WhatsApp, LinkedIn o Slack. Sin
ellas sale una tarjeta gris; con ellas sale el título de la página sobre la
marca. Los títulos se leen de los generadores, así que una página nueva hereda
su tarjeta sin tocar el script.

```bash
python3 tools/build_og.py
```

---

## Auditoría de rendimiento y accesibilidad

Lighthouse corre contra localhost, no hace falta dominio:

```bash
bash run.sh          # en una terminal
```

En otra pestaña de Chrome, ventana de incógnito (para que las extensiones no
contaminen la medición) → DevTools → **Lighthouse** → Analyze page load.

Qué esperar y qué ya está resuelto:

- **Sin JavaScript de terceros, sin tipografías externas, sin imágenes en las
  páginas de contenido.** Las páginas pesan entre 8 y 16 kB.
- Las imágenes de `/about/` llevan `width`, `height`, `loading="lazy"` y
  `srcset`, así que no hay salto de maquetación ni descarga de más.
- Un solo `<h1>` por página, jerarquía de encabezados correcta, `lang` y `dir`
  correctos, foco visible, `prefers-reduced-motion` respetado.
- **Contraste:** todo el texto pasa WCAG AA. El dorado se oscureció de `#9C7A1E`
  a `#826619` justamente por esto: en textos de 10–12 px daba 3.4:1 contra el
  mínimo de 4.5:1. Hay una prueba, `test_gold_on_paper_meets_wcag_aa`, que falla
  si alguien lo aclara.

Lo que Lighthouse marcará y no depende del sitio: en localhost no hay HTTPS ni
compresión del servidor. Ambos aparecen al publicar.


---

## Iconos del sitio (favicon)

Los iconos son la marca del estudio: el monograma TS en dorado sobre navy, el mismo
cuadro de la cabecera. Se generan con un script, no se editan a mano:

```bash
pip install Pillow          # solo para los PNG/ICO
python3 tools/build_favicon.py
```

Produce, en la raíz:

| Archivo | Para qué |
|---|---|
| `favicon.svg` | El que usan los navegadores modernos. Vectorial, nítido en cualquier pantalla |
| `favicon.ico` | Respaldo con 16, 32 y 48 px. Lo pide el navegador **solo**, sin que nadie lo enlace |
| `apple-touch-icon.png` | 180×180, para "Añadir a inicio" en iOS |
| `icon-192.png`, `icon-512.png` | Android y PWA |
| `site.webmanifest` | Nombre y colores al instalar el sitio |

**Por qué el 404 aparecía sin que nadie enlazara nada:** el navegador pide
`/favicon.ico` por convención en cada visita. Si el archivo no existe, el servidor
responde 404 y queda el error en consola y en tus logs. Poner el archivo es la mitad
del arreglo; la otra mitad son los `<link>` en el `<head>`, que ya están en las 12
páginas y en los dos generadores.

**Para cambiar la marca por una imagen tuya:** si tienes un logo, lo más simple es
reemplazar los archivos generados por los tuyos, conservando **los mismos nombres y
tamaños**. Si prefieres seguir generándolos, edita las constantes al inicio de
`tools/build_favicon.py` (colores y letras) y vuelve a ejecutarlo.

Un detalle de diseño que el script resuelve: a 16 px el filete dorado se convierte
en ruido, así que solo se dibuja de 32 px en adelante, y las letras se dibujan más
grandes y en blanco puro para que el antialiasing no las adelgace hasta volverlas
grises. Por eso cada tamaño se dibuja por separado en vez de reescalar uno solo.

**Si después de instalar sigues viendo el icono viejo o ninguno**, es caché: los
navegadores guardan el favicon con mucha terquedad. Recarga con `Cmd+Shift+R`, o
abre `http://127.0.0.1:8000/favicon.svg` directo para confirmar que se sirve.


---

## Leer la consola del navegador sin ruido

El sitio no carga nada de terceros, así que **la consola debe estar limpia**. Si ves
errores, casi siempre son de tus extensiones de Chrome, no del sitio. Se distinguen
por la ruta: `chrome-extension://...`, `Extension context invalidated`,
`Unchecked runtime.lastError`, o archivos con nombre tipo `Icon-B7XdS5Dl.js`.

Para ver la consola real, abre una ventana de incógnito (las extensiones están
desactivadas por defecto) o crea un perfil limpio de Chrome. En la pestaña Network,
tu sitio son ~10 peticiones y unos 60 kB en total; si ves 100 peticiones y 5 MB,
eso son extensiones.

Sobre SEO: los errores de consola **no son un factor de ranking**. Googlebot no
tiene tus extensiones instaladas y no ejecuta nada de eso. Lo que sí importa es que
el HTML se sirva, que el CSS y el JS carguen, y que la página no dependa de
JavaScript para mostrar su contenido — y aquí no depende.

Lo que sí hay que arreglar siempre es una violación de CSP propia: significa que
algo se está bloqueando de verdad y ese estilo o ese script no se aplica. Hay una
prueba, `test_no_inline_styles_anywhere`, que falla si algún HTML vuelve a traer un
atributo `style=` o un handler `onclick=`.

Nota: la CSP se declara dos veces a propósito — en `<meta>` dentro del HTML y en la
cabecera HTTP del servidor. Por eso una sola violación aparece duplicada en la
consola: cada política la reporta por su cuenta. No son dos problemas.


---

## Casos de estudio

Cinco casos en `/work/`, generados desde `tools/build_cases.py`. Las cifras vienen
del cliente; ninguna se redondea hacia arriba y donde no hubo medición se dice.

| Caso | Cifra principal |
|---|---|
| CG Legal — baja de phishing | 7 activos ocultos, 1 día de análisis, 3 días a la baja |
| Universidad (sin nombrar) — superficie de ataque | 12 h manuales → ~8 min por subdominio |
| Motor de reportes con IA | 3 h-persona/semana → 20 min (~128 h/año) |
| GranelCo | 3 usuarios diarios, en producción |
| AAIF | 18 skills maestras, 12–15 min por entregable largo |

**Consentimiento, y por qué está en el código**

- **CG Legal & Real Estate** aparece con nombre, autorizado. El cliente final
  atacado NO se nombra, y no se publica ningún detalle técnico que permita
  reproducir el ataque.
- **La universidad NO se nombra**, por decisión del cliente. Hay una prueba,
  `test_unnamed_client_stays_unnamed`, que falla si el nombre aparece en cualquier
  página. Un acuerdo de anonimato no debería depender de que alguien se acuerde.
- **GranelCo** se publica como proyecto interno, porque lo es. El caso lo dice.
- Cada caso lleva un bloque `.consent` que declara bajo qué permiso se publica.
  `test_every_case_states_its_consent_and_links_its_practice` lo verifica.

**Antes de publicar**: consigue de CG Legal la autorización **por escrito del texto
exacto**, no un "sí, adelante" verbal. Lo que se publica describe un incidente de
seguridad de su despacho, y eso merece firma.

**Regenerar**

```bash
python3 tools/build_cases.py    # casos
python3 tools/build_pages.py    # prácticas + sitemap (lee los slugs de los casos)
```

En ese orden: el sitemap se arma en `build_pages.py` leyendo la lista de casos.


---

## Alcance de ciberseguridad: qué se ofrece y qué no

La práctica de ciberseguridad **sí incluye pentesting de aplicaciones web**, con
alcance acotado y ejecutado bajo la certificación Web Penetration Tester (American
Council for Cybersecurity).

Condiciones que aparecen en el sitio y que no son decorativas:

- **Autorización escrita del dueño de los activos antes de probar nada.** Si el
  objetivo corre sobre una plataforma de terceros (un hosting, un SaaS), ese
  proveedor normalmente también tiene que autorizarlo.
- **Reglas de enfrentamiento acordadas por adelantado**: qué objetivos, qué
  técnicas, en qué horario y a quién llamar si algo se cae.
- **Retest incluido en el acuerdo inicial**, no revendido después.

Queda explícitamente fuera: red team de alcance completo, ingeniería social e
intrusión física. Eso requiere otro equipo, otro contrato y otra conversación con
el área legal del cliente.

Hay una prueba automatizada (`test_pentest_scope_is_stated_consistently`) que
falla si alguien edita el copy y borra la mención a la autorización escrita. La
oferta y su condición legal viajan juntas o no viajan.

**Antes del primer pentest pagado**, dos cosas que el sitio no resuelve: una
plantilla de autorización y reglas de enfrentamiento revisada por un abogado, y
cotizar un seguro de responsabilidad profesional. Son la diferencia entre un
servicio y una exposición personal.


---

## Seguridad

**Frontend**
- CSP sin `'unsafe-inline'`: CSS y JS en archivos propios, cero handlers inline
- Sin `innerHTML`, sin `eval`, sin `localStorage`, sin orígenes de terceros
- Ninguna dirección de correo en el código del cliente
- Honeypot y trampa de tiempo; timeout de 15 s con `AbortController`
- Traducciones aplicadas con `textContent`: un diccionario externo no puede inyectar marcado
- El `value` de cada `<option>` se queda en inglés, así el idioma nunca rompe la validación

**Backend**
- Validación con Pydantic y longitud máxima en todos los campos
- `practice` y `locale` contra listas blancas
- Rechazo de caracteres de control (inyección de encabezados en el correo saliente)
- Correo en texto plano; el asunto no usa texto libre del usuario
- Rate limit por IP: 5 por hora, ventana deslizante
- Límite de cuerpo de 16 KB
- Consultas parametrizadas en SQLite
- `GET /api/leads` exige token y responde 404 sin él
- Docs de OpenAPI apagadas
- Logs sin cuerpo del mensaje, sin correo completo, con IP anonimizada

**Servidor de estáticos con lista negra.** Montar la raíz del proyecto en `/` serviría
`api/main.py`, `api/.env` y `leads.db` como archivos descargables — es el error clásico
de servir la raíz del repositorio. `SafeStaticFiles` bloquea `api/`, los archivos
ocultos y las extensiones `.py`, `.db`, `.env`, `.sh`. Hay una prueba dedicada a esto.

**Pendientes conscientes**
- Rate limit en memoria: con varios workers, muévelo a Redis o al reverse proxy
- Retención de leads: define cuánto los guardas y borra el resto
- `pip-audit` en el CI para revisar dependencias

---

## Antes de publicar

1. Reemplaza `tu-dominio.com` en `index.html`, `robots.txt` y `sitemap.xml`.
2. Nombre y marca definitivos del estudio.
3. Dominio con HTTPS y HSTS.
4. Llena `api/.env` y **confirma que está en `.gitignore`** antes del primer commit.
5. Genera el token: `python3 -c "import secrets;print(secrets.token_urlsafe(32))"`.
6. Manda un mensaje de prueba en cada idioma; verifica correo y lead guardado.
7. Sustituye el texto de los casos por capturas y resultados medibles aprobados por el cliente.
8. Páginas legales: aviso de privacidad, términos, cookies donde aplique.
9. Verifica el dominio en Search Console y sube el sitemap.
10. Abre el Google Business Profile de Querétaro — es tu vía más rápida a visibilidad local.

### nginx en producción

```nginx
server {
    listen 443 ssl http2;
    server_name tu-dominio.com;

    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'; object-src 'none'" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    server_tokens off;
    client_max_body_size 64k;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

`X-Forwarded-For` importa: sin él, el rate limit ve todas las peticiones como una sola IP.

No expongas secretos en el JavaScript del frontend.
