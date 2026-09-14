# Datara Hub  (repositorio: techStudio)

Hub técnico de Antonio Garduño, Samuel González y Ricardo Vázquez. Software,
automatización con IA, ciberseguridad, datos e ingeniería, delivery y web. Base
en Querétaro, México.

**Nombre decidido: Datara Hub.** Dominio elegido: `datarahub.com` (verificado
libre por RDAP; falta comprarlo). El REPOSITORIO sigue llamándose `techStudio`,
así que el build de Pages usa `--base /techStudio`. La marca visible, el
monograma (**DH**), títulos, OG y JSON-LD ya dicen "Datara Hub". Para cambiar el
dominio en todo el repo de un tiro: `python3 tools/set_domain.py <url>`.

## Estado

- Sitio estático completo: portada, About, Work, 5 páginas de servicio, legales
- Backend FastAPI para el formulario, con SQLite
- 45 pruebas de backend
- Publicado en https://agarduno87.github.io/techStudio/
- Repositorio: github.com/agarduno87/techStudio

## Hosting

Hoy: GitHub Pages, carpeta `/docs` de la rama `main`.

Cuando haya nombre: Cloudflare Pages es gratis y suficiente para un sitio
estático con formulario. Si se quiere el backend real, un VPS de Hetzner
(~5 USD/mes). El dominio, en Cloudflare Registrar, que vende al costo.

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

**El formulario no funciona en Pages.** No hay backend. El generador inyecta un
script que abre el correo del visitante con los datos escritos. No guarda leads.

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

- Decidir el nombre y comprar el dominio
- Publicar desde `/docs` en Settings → Pages (hoy publica la raíz del repo)
- Editor de contenido para que Samuel también edite sin tocar código
