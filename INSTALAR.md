# Instalar esta versión

El proyecto viene completo en un `.zip`, así no hay que acomodar carpetas a mano
como la vez pasada.

## 1. Respalda tus leads

La base de leads no viaja en el zip. Si quieres conservar los mensajes de prueba:

```bash
cd /Users/antoniogarduno/Downloads/propuestas/posible_proyecto
cp api/leads.db ~/Desktop/leads-respaldo.db
```

Si no te importan, sáltate este paso.

## 2. Reemplaza la carpeta

```bash
cd /Users/antoniogarduno/Downloads/propuestas
mv posible_proyecto posible_proyecto_anterior
unzip ~/Downloads/posible_proyecto.zip -d .
cd posible_proyecto
find . -type f | sort
```

Deben ser **87 archivos**. Si tu `.env` tenía algo configurado, recupéralo:

```bash
cp ../posible_proyecto_anterior/api/.env api/.env 2>/dev/null || true
cp ~/Desktop/leads-respaldo.db api/leads.db 2>/dev/null || true
```

macOS a veces quita el bit de ejecución al descomprimir. Da igual: se arranca con
`bash run.sh`.

## 3. Levanta

```bash
bash run.sh
```

El primer arranque vuelve a crear el `.venv` porque es una carpeta nueva. Un minuto.

## 4. Revisa

- http://127.0.0.1:8000/ — en **Practices**, cada práctica enlaza ya a su página
- http://127.0.0.1:8000/services/cybersecurity/ — la que cambió: ahora ofrece pentesting
- http://127.0.0.1:8000/services/cybersecurity/?lang=es
- http://127.0.0.1:8000/work/ — los cinco casos, nuevos
- http://127.0.0.1:8000/work/cg-legal-phishing/ — el caso con más números
- http://127.0.0.1:8000/work/reporting-engine/?lang=es
- http://127.0.0.1:8000/about/ — el equipo, nuevo
- http://127.0.0.1:8000/about/?lang=es
- http://127.0.0.1:8000/legal/privacy/ y /legal/terms/
- http://127.0.0.1:8000/og/home.png — la tarjeta social
- http://127.0.0.1:8000/sitemap.xml — 12 URLs

## 5. Pruebas

```bash
source .venv/bin/activate
pip install httpx2 pytest
python api/test_api.py
```

**45 pruebas.** Las nuevas frente a la versión anterior: las cinco páginas se
sirven, cada una tiene título y descripción únicos, traen canonical y datos
estructurados, la portada enlaza a todas, el sitemap las lista, el generador no se
puede descargar desde el navegador, y el alcance del pentesting siempre aparece
junto a la autorización escrita.

Frontend (opcional, requiere `npm install jsdom`):

```bash
node tests/frontend.check.js
for s in software-engineering ai-automation cybersecurity data-analytics technical-delivery; do
  node tests/service-pages.check.js $s
done
for s in cg-legal-phishing attack-surface-automation reporting-engine granelco aaif; do
  node tests/case-pages.check.js $s
done
node tests/about-page.check.js
```

## 7. Avisos de leads (opcional, 5 minutos)

En `api/.env` pon `NOTIFY_CHANNEL=telegram` más el token y el chat id de tu bot.
El README trae los pasos. Con eso, cada lead te llega al celular en segundos sin
necesidad de dominio ni de correo.

## 6. Editar contenido

**No edites los HTML de `services/` a mano** — se regeneran y perderías los cambios.

El contenido vive en dos archivos, con el inglés y el español juntos:

- `tools/build_pages.py` → lista `PAGES`, las cinco prácticas
- `tools/build_cases.py` → lista `CASES`, los cinco casos

Cambias ahí y regeneras, en este orden:

```bash
python3 tools/build_cases.py
python3 tools/build_pages.py
```

El sitemap se arma en `build_pages.py` leyendo los slugs de los casos, por eso va
al final.
