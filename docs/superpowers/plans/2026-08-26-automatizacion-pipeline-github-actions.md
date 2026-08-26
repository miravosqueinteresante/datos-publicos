# Datos Públicos — Automatización del pipeline (GitHub Actions) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear el workflow de GitHub Actions que ejecuta el pipeline de contrataciones de la Muni mensualmente y a pedido, regenera datos y web, y commitea cambios.

**Architecture:** Un solo archivo YAML en `.github/workflows/` que orquesta los scripts existentes y usa `actions/github-script` para el commit condicional. Sin lógica nueva en el pipeline; solo orquestación. La lógica de commit se prueba primero en un script Python local (para validar el "solo si hay cambios") antes de trasladarla al GitHub-script.

**Tech Stack:** GitHub Actions (checkout v4, setup-python v5, github-script v7), Python 3.10, YAML.

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- Scripts existentes (funcionando, con tests): `scripts/dncp_contrataciones.py`, `scripts/generar_datos_web.py`, `scripts/tests/`.
- El ZIP de la DNCP queda ignorado (`.gitignore` → `data/_sin_versionar/`).
- 17 tests pasan actualmente.

---

### Task 1: Script de actualización local (valida la idempotencia del flujo)

**Files:**
- Create: `scripts/actualizar_datos.py`

- [ ] **Step 1: Escribir script que reproduce el flujo del workflow en local**

`scripts/actualizar_datos.py`:

```python
import subprocess, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def paso(comando, cwd=ROOT):
    print(f"==> {comando}")
    subprocess.run(comando, shell=True, cwd=cwd, check=True)


def hay_cambios():
    out = subprocess.run("git status --porcelain",
                         shell=True, capture_output=True, text=True, cwd=ROOT)
    return bool(out.stdout.strip())


def main():
    paso("python scripts/dncp_contrataciones.py")
    paso("python scripts/generar_datos_web.py")
    paso("python -m unittest discover -s scripts/tests")
    if hay_cambios():
        print("Cambios detectados; en CI se commitea. En local: revisar git status.")
    else:
        print("Sin cambios: dataset y web ya están al día.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Verificar localmente en dos pasadas**

Primera pasada:
```bash
python scripts/actualizar_datos.py
```
Expected: corre pipeline, generador, tests (17 OK), y reporta "Cambios detectados" o "Sin cambios" según si el repo está limpio.

- [ ] **Step 3: Commit**

```bash
git add scripts/actualizar_datos.py
git commit -m "feat: add local update orchestrator script (manual primero)"
```

---

### Task 2: Workflow de GitHub Actions

**Files:**
- Create: `.github/workflows/actualizar-datos.yml`

- [ ] **Step 1: Crear el workflow**

Contenido exacto (de la spec aprobada):

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
            const { execSync } = require("child_process");
            const changed = execSync("git status --porcelain").toString().trim();
            if (!changed) {
              console.log("Sin cambios: dataset y web ya están al día.");
            } else {
              execSync('git config user.name "github-actions[bot]"');
              execSync('git config user.email "github-actions[bot]@users.noreply.github.com"');
              execSync("git add data/contrataciones_muni_2026.csv www/datos/contrataciones-2026.json");
              execSync('git commit -m "data: actualizar contrataciones de la Muni (GitHub Actions)"');
              execSync("git push");
            }
```

- [ ] **Step 2: Validar el YAML**

```bash
python -c "import yaml,sys" 2>&1 || pip install pyyaml
python -c "import yaml; yaml.safe_load(open('.github/workflows/actualizar-datos.yml')); print('YAML valido')"
```
Expected: "YAML valido". Si no hay pyyaml, instalar o validar por inspección.

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/actualizar-datos.yml
git commit -m "ci: add monthly+manual pipeline workflow (GitHub Actions)"
git push
```

---

### Task 3: Probar el workflow en GitHub

**Files:**
- N/A (operación en GitHub)

- [ ] **Step 1: Lanzar la primera corrida manual desde la UI**

Abrir GitHub → Actions → `actualizar-datos` → "Run workflow" (rama `main`).

- [ ] **Step 2: Monitorear hasta completar**

Expected: los pasos 1-5 corren sin error; el paso 6 (`github-script`) reporta "Sin cambios" o hace commit+push. El ZIP no se commitea (correr `git status` local y confirmar que `data/_sin_versionar/` sigue ignorado).

- [ ] **Step 3: Verificar idempotencia**

Lanzar una segunda corrida manual inmediata.
Expected: si no hubo cambios en el repo entre corridas, la segunda reporta "Sin cambios" y no genera commit.

---

## Criterios de éxito (verificación final)

- Workflow presente y válido (YAML parsea).
- Primera corrida manual completa sin errores.
- Idempotencia: segunda corrida sin cambios no genera commit.
- La carpeta `_sin_versionar` nunca llega al repo.
- Tests corren dentro del workflow y pasan.
- Trazabilidad: el CSV regenerado es idéntico al local (mismos scripts).