# Formulario en PHP (Neubox / cPanel)

`contact.php` es el reemplazo del backend FastAPI (`api/main.py`) para cuando el
sitio viva en **Neubox** con PHP + MySQL + correo del dominio, sin un proceso
Python corriendo. Mismas defensas: honeypot, trampa de tiempo, rate limit,
validación con longitudes máximas, práctica en lista blanca, IP anonimizada y
correo en texto plano con cabeceras saneadas.

## Qué contiene

    contact.php          el endpoint (recibe el JSON del formulario, guarda y avisa)
    config.sample.php    plantilla de configuración -> cópiala a config.php EN EL SERVIDOR
    schema.sql           las tablas (opcional: contact.php las crea solas si no existen)
    .htaccess            bloquea config.php/schema.sql y quita el caché del endpoint

`config.php` **no** está en el repositorio (lleva credenciales). Vive solo en el
servidor.

## Puesta en marcha (una vez)

1. **Base de datos.** En cPanel → *Bases de datos MySQL*: crea una base (p. ej.
   `usuario_leads`), un usuario y asígnalo a la base con todos los privilegios.
2. **Buzón de correo.** En cPanel → *Cuentas de correo*: crea `leads@datarahub.com`.
   Ese será el remitente; entrega bien porque es un buzón real del dominio.
3. **Sube los archivos.** Copia `contact.php`, `config.sample.php`, `.htaccess`
   (y opcionalmente `schema.sql`) a `public_html/` (o donde sirvas el sitio).
4. **Configura.** Renombra `config.sample.php` a `config.php` y llena: datos de
   MySQL, `mail_from` (`leads@datarahub.com`), `mail_to` (donde quieres recibir
   el aviso) y un `ip_salt` aleatorio — genéralo con `openssl rand -hex 32`.
5. **Apunta el formulario.** En `app.js`, cambia:

       var API_ENDPOINT = "/contact.php";

   (hoy dice `/api/contact`). Si prefieres no tocar `app.js`, deja el endpoint en
   `/api/contact` y crea una regla en `.htaccess` que reescriba esa ruta a
   `contact.php`.

## Probar que quedó

- Envía el formulario desde el sitio: debe responder rápido y guardar la fila.
- Revísalo en cPanel → *phpMyAdmin* → tabla `leads`.
- Debe llegar el correo a `mail_to`. Si no llega pero la fila sí se guardó, el
  problema es el correo, no el formulario (revisa el buzón remitente y el SPF).

## Notas

- **Sin backend Python en Neubox.** El hosting compartido de Neubox corre PHP,
  no procesos Python de larga vida. Por eso el formulario se reescribe en PHP en
  vez de portar FastAPI. El FastAPI sigue siendo el backend si algún día el sitio
  se mueve a un VPS.
- **El sitio estático no cambia.** Sigue siendo el mismo HTML/CSS/JS; lo único
  que cambia es a qué URL manda el formulario.
- **Privacidad.** Se guarda IP anonimizada (sin el último octeto), igual que el
  backend Python. El rate limit usa un hash de la IP con salt, nunca la IP en
  claro. Esto es lo que promete el Aviso de privacidad del sitio.
