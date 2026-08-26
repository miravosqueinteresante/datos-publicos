# Datos Públicos — Publicación GitHub Pages — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publicar `datospublicos.muchotexto.net` (plataforma + /lab) vía GitHub Actions + Pages.

**Architecture:** Script `scripts/publicar_sitio.py` construye `_site/` (www a raíz, lab a /lab con rutas corregidas), luego workflow `deploy-pages` empaqueta y despliega.

**Tech Stack:** Python 3.10 (construcción), GitHub Actions Pages.

---

### Task 1: `www/CNAME` + `.gitignore`

- [ ] Step 1: Crear `www/CNAME` con contenido `datospublicos.muchotexto.net` (una línea, sin http).

- [ ] Step 2: Añadir `_site/` a `.gitignore`.

- [ ] Step 3: Commit. `git add www/CNAME .gitignore && git commit -m "chore: add Pages CNAME and ignore _site"`

---

### Task 2: `scripts/publicar_sitio.py` (TDD)

- [ ] Step 1: Test que falla — reemplazo de rutas `../www/` → `../` en lab:

```python
from publicar_sitio import ajustar_ruta_lab

class TestPublicar(unittest.TestCase):
    def test_lab_ref_raiz(self):
        html = 'href="../www/index.html" src="../www/css/style.css"'
        out = ajustar_ruta_lab(html)
        self.assertIn('href="../index.html"', out)
        self.assertIn('src="../css/style.css"', out)
        self.assertNotIn("../www/", out)
    def test_sin_www_no_cambia(self):
        self.assertEqual(ajustar_ruta_lab("src='app.js'"), "src='app.js'")
```

- [ ] Step 2: Ejecutar, debe fallar (módulo no existe).

- [ ] Step 3: Implementar:

```python
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WWW = os.path.join(ROOT, "www")
LAB = os.path.join(ROOT, "lab")
SITE = os.path.join(ROOT, "_site")


def ajustar_ruta_lab(texto):
    # en publicación www es la raíz y lab está en /lab: ../www/... -> ../...
    return texto.replace("../www/", "../")


def construir():
    if os.path.exists(SITE):
        shutil.rmtree(SITE)
    shutil.copytree(WWW, SITE)
    shutil.copytree(LAB, os.path.join(SITE, "lab"))
    for nombre in os.listdir(os.path.join(SITE, "lab")):
        if nombre.endswith(".html"):
            ruta = os.path.join(SITE, "lab", nombre)
            with open(ruta, encoding="utf-8") as f:
                contenido = f.read()
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(ajustar_ruta_lab(contenido))
    # CNAME ya viene dentro de www/ y se copió; corroborar
    cname = os.path.join(SITE, "CNAME")
    if not os.path.exists(cname):
        with open(cname, "w", encoding="utf-8") as f:
            f.write("datospublicos.muchotexto.net")
    return SITE


if __name__ == "__main__":
    print("Sitio construido en:", construir())
```

- [ ] Step 4: Tests pasan.

- [ ] Step 5: `git add scripts/publicar_sitio.py scripts/tests/test_publicar_sitio.py && git commit -m "feat: build site folder (www->root, lab->/lab) with TDD"`

---

### Task 3: Workflow `deploy-pages.yml`

- [ ] Step 1: Crear `.github/workflows/deploy-pages.yml` (contenido de la spec).

- [ ] Step 2: Validar YAML con pyyaml.

- [ ] Step 3: Commit. `git add .github/workflows/deploy-pages.yml && git commit -m "ci: deploy site to GitHub Pages"`

---

### Task 4: Activar Pages y desplegar

- [ ] Step 1: Activar Pages (source GitHub Actions):

```bash
gh api -X POST repos/miravosqueinteresante/datos-publicos/pages -f "source[branch]=main" -f "source[path]=/" 2>&1
```
(Nota: con build_type workflow, el source se define por el workflow; si POST falla por Pages ya existente, usar PUT.)

- [ ] Step 2: Lanzar el workflow:

```bash
gh workflow run deploy-pages --ref main
```

- [ ] Step 3: Esperar completar y verificar página:

```bash
gh run list --workflow deploy-pages --limit 1 --json status,conclusion
```

- [ ] Step 4: Verificar online:

```powershell
(Invoke-WebRequest -Uri "https://datospublicos.muchotexto.net" -UseBasicParsing).StatusCode
(Invoke-WebRequest -Uri "https://datospublicos.muchotexto.net/lab" -UseBasicParsing).StatusCode
```
Expected: ambos 200. HTTPS debe funcionar (async, puede demorar minutos para el cert).

- [ ] Step 5: Commit docs + push.

---

## Criterios de éxito

- `_site/` construido, workflow exitoso.
- `https://datospublicos.muchotexto.net` 200 (plataforma) y `.../lab` 200.
- Pipeline/tests intactos.
- `_site/` ignorado.