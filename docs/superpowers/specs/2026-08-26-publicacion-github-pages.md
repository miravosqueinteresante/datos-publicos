# Datos Públicos — Publicación en GitHub Pages (datospublicos.muchotexto.net)

Fecha: 2026-08-26

## Propósito

Hacer visible públicamente el proyecto (hito mínimo viable, plan maestro sección 31). El dominio `datospublicos.muchotexto.net` (CNAME ya creado y propagado en GoDaddy → `miravosqueinteresante.github.io`) servirá la plataforma (`www/`), y el laboratorio quedará en `datospublicos.muchotexto.net/lab` (Opción A confirmada).

## Mecanismo

GitHub Pages NO sirve una subcarpeta (como `www/`) directamente desde la configuración por rama. La vía estándar es **GitHub Actions con `configure-pages` + `upload-pages-artifact` + `deploy-pages`**, empaquetando un directorio de salida construido.

Se construye `_site/` con un script reproducible `scripts/publicar_sitio.py`:
1. Copia el contenido de `www/` → raíz de `_site/` (index, css, js, datos, CNAME).
2. Copia `lab/` → `_site/lab/`, ajustando las rutas relativas (`../www/...` → `../...`) porquUo en publicación `www/` es la raíz y `lab/` está en `/lab/`.
3. Añade `CNAME` (contenido `datospublicos.muchotexto.net`) en la raíz.

## Estructura del sitio publicado

```
datospublicos.muchotexto.net
├── index.html        # plataforma (explorar)
├── datos.html
├── metodologia.html
├── css/ js/ datos/
└── lab/             # laboratorio en subruta
    ├── index.html
    ├── pipelines.html
    └── datos.html
```

## Archivos

- `www/CNAME` — contiene `datospublicos.muchotexto.net` (se copia a la raíz del sitio).
- `scripts/publicar_sitio.py` — construye `_site/` (con test TDD).
- `.github/workflows/deploy-pages.yml` — build (config + upload) + deploy.
- `.gitignore` — añadir `_site/`.

## Workflow (referencia)

```yaml
name: deploy-pages
on:
  push: { branches: [main] }
  workflow_dispatch:
permissions:
  contents: read
  pages: write
  id-token: write
concurrency:
  group: pages
  cancel-in-progress: true
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.10" }
      - run: python scripts/publicar_sitio.py
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with: { path: _site }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

## Pasa a configuración de Pages

`gh api` para activar source = GitHub Actions (build_type workflow). El `CNAME` en `_site/` hace que GitHub asocie el dominio y emita el certificado HTTPS automáticamente.

## Criterios de éxito

- `scripts/publicar_sitio.py` pasa su test y produce `_site/` con la estructura correcta.
- Workflow `deploy-pages` corriendo y exitoso en GitHub.
- `https://datospublicos.muchotexto.net` carga la plataforma; `.../lab` carga el lab.
- No se modifica la lógica de datos ni el pipeline.
- `_site/` no se versiona.