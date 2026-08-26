# Datos Públicos — Automatización del pipeline (GitHub Actions)

Fecha: 2026-08-26

## Propósito

Automatizar el pipeline de contrataciones de la Muni en GitHub Actions, siguiendo el plan maestro (sección 10: "automatizar lo que ya se entiende"; principio 29.10: "construir → probar → entender → documentar → automatizar"). El pipeline manual ya funciona y tiene tests; ahora se ejecuta en la nube de forma repetible.

## Alcance

**Incluye:**
- Workflow `.github/workflows/actualizar-datos.yml` que:
  1. Corre el pipeline (`scripts/dncp_contrataciones.py`) → regenera `data/contrataciones_muni_2026.csv`.
  2. Corre el generador web (`scripts/generar_datos_web.py`) → regenera `www/datos/contrataciones-2026.json`.
  3. Corre los tests (`python -m unittest discover -s scripts/tests`).
  4. Si hay cambios en CSV/JSON: commit + push automático. Si no: no toca el repo.
- Trigger: `workflow_dispatch` (manual) + `schedule` mensual (1º de mes).
- Permisos del workflow: `contents: write` para poder commitear.

**Excluye (no en esta fase):**
- Integración del scraping del perfil institucional de la DNCP (frágil).
- Configuración de subdominio / publicación de la web.
- Dashboard del laboratorio (FASE 5).
- Migración del ZIP a artifact (el runner es efímero; se descarga en cada corrida, aceptable mensual).

## Decisiones

1. Ejecución **mensual + manual** (workflow_dispatch + cron `0 0 1 * *`).
2. El ZIP (~490 MB) queda ignorado por git; el runner lo descarga, procesa y descarta.
3. Commit automático solo si hay cambios (dataset/JSON diferentes al último commit).
4. Sin dependencias nuevas: stdlib de Python, actions disponibles (`actions/checkout@v4`, `actions/setup-python@v5`, `actions/github-script@v7`).
5. El CSV conserva su trazabilidad (fecha de obtención en `data/README.md`).

## Workflow (referencia)

```yaml
name: actualizar-datos

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 1 * *"

permissions:
  contents: write

jobs:
  pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - run: python scripts/dncp_contrataciones.py
      - run: python scripts/generar_datos_web.py
      - run: python -m unittest discover -s scripts/tests
      - uses: actions/github-script@v7
        with:
          script: |
            // si hay cambios, commit + push; si no, no hacer nada
            const { execSync } = require("child_process");
            const changed = execSync("git status --porcelain").toString().trim();
            if (!changed) { console.log("Sin cambios"); }
            else {
              execSync('git config user.name "github-actions[bot]"');
              execSync('git config user.email "github-actions[bot]@users.noreply.github.com"');
              execSync("git add data/contrataciones_muni_2026.csv www/datos/contrataciones-2026.json");
              execSync('git commit -m "data: actualizar contrataciones de la Muni (GitHub Actions)"');
              execSync("git push");
            }
```

## Criterios de éxito

- El workflow aparece en GitHub Actions y se puede lanzar manualmente.
- Una corrida manual completa: descarga, procesa, tests OK, commit (si hay cambios).
- Si se lanza dos veces seguidas sin cambios: la segunda corrida no genera commit (idempotencia).
- El repo nunca contiene el ZIP (verificado post-corrida).
- Trazabilidad intacta (CSV/JSON regenerados por los mismos scripts versionados).