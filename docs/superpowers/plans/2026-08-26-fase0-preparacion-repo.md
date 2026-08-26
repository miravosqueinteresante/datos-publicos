# Datos Públicos — FASE 0: Preparación del repositorio — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear la infraestructura inicial del proyecto Datos Públicos: repo único en GitHub, estructura base, convenciones y documentación, con el plan maestro restringido a local.

**Architecture:** Repo Git único `datos-publicos` en GitHub (cuenta `miravosqueinteresante`) con subcarpetas para documentación, datos, scripts y las dos webs (lab y www). El plan maestro se mantiene fuera del repo por completo.

**Tech Stack:** Git 2.53, GitHub CLI (`gh` 2.94), Markdown.

---

## Contexto de ejecución

- Carpeta local (raíz de trabajo): `C:\Users\pc\Desktop\Proyectos\Datos Publicos`
- El nombre local tiene espacio; el repo remoto se llama `datos-publicos` (sin espacio). Es normal.
- Git y `gh` ya autenticados como `miravosqueinteresante`.
- El PDF `DATOS PÚBLICOS — DOCUMENTO MAESTRO DEL PROYECTO.pdf` está en la carpeta local padre y **no debe versionarse ni subirse**.

## Estructura destino

```
datos-publicos/
├── README.md
├── AGENTS.md
├── .gitignore
├── docs/
│   └── superpowers/
│       ├── specs/
│       └── plans/
├── data/
├── scripts/
├── lab/
├── www/
└── .github/workflows/
```

---

### Task 1: Crear el repositorio en GitHub

**Files:**
- N/A (operación de red)

- [ ] **Step 1: Crear el repo remoto privado**

El repo debe ser **privado** por ahora (el proyecto aún no está listo para publicación). Comando a ejecutar en la carpeta raíz:

```bash
gh repo create datos-publicos --private --source "C:\Users\pc\Desktop\Proyectos\Datos Publicos" --remote origin --description "Datos Públicos: infraestructura cívica de datos municipales. Primer caso: Municipalidad de Asunción."
```

- [ ] **Step 2: Verificar que se creó y que el remote quedó configurado**

```bash
gh repo view miravosqueinteresante/datos-publicos --json name,visibility,url
git remote -v
```

Expected:
- name: `datos-publicos`
- visibility: `PRIVATE`
- url: `https://github.com/miravosqueinteresante/datos-publicos`
- remote `origin` apunta a ese repo.

---

### Task 2: Crear `.gitignore` (incluida la regla del plan maestro)

**Files:**
- Create: `.gitignore`

- [ ] **Step 1: Crear `.gitignore` en la raíz**

Usar contenido exacto:

```gitignore
# Plan maestro — SOLO LOCAL, nunca versionar
DATOS PÚBLICOS*.pdf
*DOCUMENTO MAESTRO*.pdf

# Sistemas operativos
.DS_Store
Thumbs.db

# Editores / IDE
.vscode/
.idea/

# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/

# Jekyll / GitHub Pages (build)
_site/
.jekyll-cache/
.sass-cache/

# Otros temporales
*.tmp
*.log
```

- [ ] **Step 2: Verificar la regla del plan**

```bash
git check-ignore -v "DATOS PÚBLICOS — DOCUMENTO MAESTRO DEL PROYECTO.pdf"
```

Expected: imprime la línea que coincide con el patrón `*DOCUMENTO MAESTRO*.pdf` (defensa por si el PDF llegara a estar dentro del repo).

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "chore: add gitignore with local-only master plan rule"
```

---

### Task 3: Crear `README.md`

**Files:**
- Create: `README.md`

- [ ] **Step 1: Crear `README.md` en la raíz**

Contenido:

```markdown
# Datos Públicos

Infraestructura cívica de datos abiertos. Toma información pública dispersa y la transforma
en datos estructurados, indicadores, visualizaciones y herramientas útiles.

## Sitios

- **Laboratorio:** lab.muchotexto.net (cómo funciona el sistema)
- **Plataforma pública:** datospublicos.muchotexto.net (qué puede hacer la gente con la información)

## Primer caso de uso

Municipalidad de Asunción. La arquitectura está pensada para extenderse a otros municipios.

## Estado

**FASE 0 — Preparación (en curso):** repositorio, estructura y convenciones.

Próximas fases:
1. Inventario de datos municipales
2. Evaluación de fuentes
3. Primera fuente y primer pipeline
4. Primer producto útil

## Estructura

- `docs/` — documentación del proyecto (specs y planes en `docs/superpowers/`)
- `data/` — datasets procesados
- `scripts/` — pipelines y herramientas
- `lab/` — web del laboratorio
- `www/` — web de la plataforma pública
- `.github/workflows/` — automatización (GitHub Actions)

## Regla importante

El **documento maestro** del proyecto es interno y de distribución limitada: vive solo en local
y NO se versiona ni se publica en este repositorio.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add project readme"
```

---

### Task 4: Crear `AGENTS.md` con convenciones y regla del plan

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Crear `AGENTS.md` en la raíz**

Contenido (convenciones para agentes/OpenCode que trabajen en este repo):

```markdown
# AGENTS.md — Datos Públicos

Guía para agentes de IA y colaboradores al trabajar en este repositorio.

## Regla crítica: el plan maestro es SOLO LOCAL

El documento `DATOS PÚBLICOS — DOCUMENTO MAESTRO DEL PROYECTO.pdf` es interno y de
distribución limitada.

- NO lo añadas al repositorio.
- NO lo transcribas a `docs/` ni a ningún archivo versionado.
- NO subas ninguna copia a GitHub.
- Vive únicamente en la carpeta local del proyecto (fuera del área de Git).

Si un agente lo necesita como referencia, puede leerlo desde el disco local, pero nunca
persistirlo en un archivo del repo.

## Estructura de carpetas

- `docs/` — documentación del proyecto; specs en `docs/superpowers/specs/`, planes en `docs/superpowers/plans/`
- `data/` — datasets procesados
- `scripts/` — pipelines y herramientas (Python)
- `lab/` — web del laboratorio (GitHub Pages)
- `www/` — web de la plataforma pública (GitHub Pages)
- `.github/workflows/` — GitHub Actions

## Convenciones

- Un solo repositorio para todo el sistema (lab y plataforma son interfaces del mismo proyecto).
- Archivos Markdown en español.
- Proceso manual primero; automatizar (GitHub Actions) solo lo que ya se entiende y funciona.
- Datos siempre con trazabilidad: fuente original, URL, fecha de obtención, proceso y limitaciones.

## Flujo de trabajo

- Feature nueva → spec → plan → implementación (TDD cuando aplique código) → revisión.
- Commits pequeños y frecuentes en español.
```

- [ ] **Step 2: Commit**

```bash
git add AGENTS.md
git commit -m "docs: add agents conventions and master plan local rule"
```

---

### Task 5: Añadir README de estructura a cada carpeta y commit inicial completo

**Files:**
- Create: `data/README.md`, `scripts/README.md`, `lab/.gitkeep` (opcional), `www/.gitkeep` (opcional)

- [ ] **Step 1: Crear marcadores de carpetas para que Git las rastree (Git no versiona carpetas vacías)**

Crear un `README.md` mínimo en `data/` y `scripts/`:

```markdown
# data

Datasets procesados por los pipelines. Cada dataset debe documentar: fuente original, URL,
fecha de obtención, actualización, proceso, validaciones, errores y limitaciones.
```

```markdown
# scripts

Pipelines y herramientas de procesamiento de datos (Python). Proceso manual primero;
automatizar solo lo que ya se entiende y funciona.
```

- [ ] **Step 2: Añadir `.gitkeep` a las carpetas de las webs vacías**

```bash
New-Item -ItemType File -Force -Path "lab\.gitkeep","www\.gitkeep"
```

- [ ] **Step 3: Commit inicial completo**

```bash
git add -A
git commit -m "feat: scaffold datos-publicos repository structure"
```

---

### Task 6: Push a GitHub y verificación final

**Files:**
- N/A (operación de red)

- [ ] **Step 1: Enviar `main` al remoto**

```bash
git push -u origin main
```

- [ ] **Step 2: Verificar que el plan maestro NO está en el repo remoto**

```bash
gh api repos/miravosqueinteresante/datos-publicos/git/trees/main?recursive=1 --jq '.tree[].path'
```

Expected: NO aparece ningún archivo con "maestro" ni "DOCUMENTO MAESTRO". La lista incluye `README.md`, `AGENTS.md`, `.gitignore`, `docs/superpowers/...`, `data/`, `scripts/`, `lab/`, `www/`.

- [ ] **Step 3: Verificación final del log**

```bash
git log --oneline
```

Expected: series de commits en orden (gitignore, readme, agents, scaffold, push).

---

## Criterios de éxito (verificación final)

- Repositorio `miravosqueinteresante/datos-publicos` existe, privado, con el historial en `main`.
- `README.md` y `AGENTS.md` presentes y correctos.
- `.gitignore` ignora el plan maestro (verificado con `git check-ignore`).
- Estructura `docs/ data/ scripts/ lab/ www/ .github/workflows/` presente en el remoto.
- Ninguna copia del plan maestro en GitHub (verificado con el árbol del repo).
