# Publicar techStudio en GitHub Pages

## Por qué daban 404 About y Work

Los enlaces del sitio están escritos como rutas absolutas: `/about/`, `/work/`,
`/services/cybersecurity/`. Con diagonal al inicio.

**En local** corres `bash run.sh` y el sitio vive en la raíz de
`127.0.0.1:8000`, así que `/about/` resuelve a `127.0.0.1:8000/about/`. Funciona.

**En GitHub Pages** tu sitio NO vive en la raíz: vive en
`agarduno87.github.io/techStudio/`. Ahí `/about/` resuelve a
`agarduno87.github.io/about/`, que está fuera de tu repositorio. 404.

Las páginas siempre estuvieron ahí. Lo que estaba mal eran los enlaces.

## El comando

Desde la raíz del proyecto:

    cd /Users/antoniogarduno/Documents/techStudio/techStudio
    python3 tools/build_github_pages.py --base /techStudio --mailto ing.antoniogz@gmail.com

Eso crea `docs/` con 71 archivos: todo el sitio con las 16 rutas reescritas a
`/techStudio/...`, más `.nojekyll` y una página 404.

**No necesitas nada extra.** No hace falta instalar dependencias: el script solo
usa la biblioteca estándar de Python.

### Los dos argumentos

`--base /techStudio` tiene que coincidir EXACTAMENTE con el nombre del
repositorio. Si el repo se llamara `tech-studio`, sería `--base /tech-studio`.
Si te equivocas aquí, el sitio sale sin diseño.

`--mailto` es el correo al que llega el formulario. En Pages no hay backend, así
que el envío abre el correo del visitante con los datos ya escritos.

## Después de generar

    git add docs tools/build_github_pages.py PUBLICAR.md
    git commit -m "Sitio estatico para GitHub Pages"
    git push

Y en GitHub: **Settings → Pages → Source: Deploy from a branch →
Branch `main`, carpeta `/docs`**.

Hoy está publicando la raíz del repo. Cambiarlo a `/docs` es el paso que faltaba.

## Cada vez que cambies contenido

    python3 tools/build_pages.py              # si tocaste las paginas de servicio
    python3 tools/build_github_pages.py --base /techStudio --mailto ing.antoniogz@gmail.com
    git add -A && git commit -m "..." && git push

El orden importa: primero los generadores de contenido, al final el de Pages.

## Cuidado con el nombre del archivo

Tu proyecto ya tenía un `tools/build_pages.py` que genera las cinco páginas de
`/services/`. Mi generador se llamaba igual y en el paquete que te entregué lo
sobrescribió. Por eso ahora se llama `build_github_pages.py`. Son dos cosas
distintas:

    tools/build_pages.py         -> genera las 5 paginas de /services/
    tools/build_github_pages.py  -> empaqueta el sitio entero en docs/

## Lo que sigue sin funcionar en Pages

El formulario no guarda nada: Pages no corre Python. Y no hay
Content-Security-Policy, porque Pages no deja poner cabeceras propias.
Ambas cosas vuelven cuando el sitio viva en un servidor real.
