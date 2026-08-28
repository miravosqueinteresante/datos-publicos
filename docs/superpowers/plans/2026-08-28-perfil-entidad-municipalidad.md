# Datos Públicos — Perfil de entidad Municipalidad — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Consolidar Explorar + Análisis en una página de perfil `www/muni.html` para la Municipalidad de Asunción, con menú simplificado (Demo · Municipalidad · Datos · Metodología).

**Architecture:** Nueva página `muni.html` + JS `muni.js` (consolida serie temporal, indicadores por año y fichas de proveedores). Eliminar `index.html`/`analisis.html` del menú y del repo (el perfil los absorbe). Reutiliza los JSON existentes. Sin cambios de datos/pipeline.

**Tech Stack:** HTML5, JS vanilla, CSS (2026). Sin nuevas dependencias.

---

## Contexto
- Existentes: `www/index.html`+`app.js` (Explorar), `www/analisis.html`+`analisis.js` (Análisis + fichas), `www/datos*.html`, `www/demo.html`, `lab/`.
- JSON por año + proveedores.json → se reutilizan.
- El deploy copia `www/` a raíz (`publicar_sitio.py`).

---

### Task 1: `www/muni.html` — página consolidada

**Files:**
- Create: `www/muni.html`

- [ ] **Step 1: Crear la página** (estructura de la spec):

- Cabecera de entidad: "Municipalidad de Asunción" + SICP 108 + subtítulo + selector de año + nota fuente.
- Sección **Evolución por año** (contenedor `#serie-anual`).
- Sección **Indicadores por año** (selector `#sel-anio-muni` + contenedor `#detalle-anual`).
- Sección **Principales proveedores** (contenedor `#fichas-proveedores`).
- Sección "Metodología y limitaciones" (enlace a `metodologia.html` + nota sobre la serie).
- `<script src="js/muni.js">`.

Menú compartido:
```html
<li><a href="demo.html">Demo</a></li>
<li><a href="muni.html" class="activo">Municipalidad</a></li>
<li><a href="datos.html">Datos</a></li>
<li><a href="metodologia.html">Metodología</a></li>
```

- [ ] **Step 2: Commit** — `git add www/muni.html && git commit -m "feat: entity profile page for Municipalidad (muni.html)"`

---

### Task 2: `www/js/muni.js` — lógica consolidada

**Files:**
- Create: `www/js/muni.js`

- [ ] **Step 1: Escribir el JS** — consolida: serie (de analisis.js renderSerie), detalle por año (renderDetalle + bloque + barras), fichas de proveedores (renderFichas). Reutiliza las funciones ya escritas de `analisis.js` (copiarlas a `muni.js`, no importar).

Funciones: `FMT`, `FMT2`, `ANIOS`, `INDICADORES`, `bloque`, `barras`, `renderSerie`, `renderDetalle`, `renderFichas`, `init()`.

- [ ] **Step 2: Commit** — `git add www/js/muni.js && git commit -m "feat: consolidated profile JS (series + indicators + supplier fichas)"`

---

### Task 3: Eliminar Explorar/Análisis y actualizar menú

**Files:**
- Delete: `www/index.html`, `www/js/app.js`
- Delete: `www/analisis.html`, `www/js/analisis.js`
- Modify: `www/demo.html`, `www/datos.html`, `www/metodologia.html` (menú: quitar Explorar/Análisis → Municipalidad)

- [ ] **Step 1: git rm** de los 4 archivos (index/app.js/analisis/analisis.js).

- [ ] **Step 2: Actualizar menú** en `demo.html`, `datos.html`, `metodologia.html`:
  - quitar `<li><a href="index.html">Explorar</a></li>` y `<li><a href="analisis.html">Análisis</a></li>`
  - añadir `<li><a href="muni.html">Municipalidad</a></li>` (en la posición correspondiente).

- [ ] **Step 3: Revisar enlaces** a index/analisis en el resto (demo CTA "Explorar contrataciones" → `muni.html`; "Ver el análisis" → `muni.html`).

- [ ] **Step 4: Commit** — `git add -A && git commit -m "refactor: consolidate Explorar/Análisis into entity profile page"`

---

### Task 4: Verificación + deploy

- [ ] Step 1: `python -B -m unittest discover -s scripts/tests` (sin cambios de datos → OK).
- [ ] Step 2: Servir local (repofood) → verificar `muni.html`, `js/muni.js`, JSONs por año, proveedores.json (200); demo/datos/metodología con menú nuevo.
- [ ] Step 3: Verificar que NO quedan enlaces rotos a `index.html`/`analisis.html` (grep).
- [ ] Step 4: Commit docs (spec/plan) + `git push` (deploy automático).
- [ ] Step 5: Verificar producción: `muni.html` 200, menú nuevo.

---

## Criterios de éxito
- `muni.html` reúne serie + indicadores + fichas.
- Menú: Demo · Municipalidad · Datos · Metodología; sin enlaces a Explorar/Análisis.
- Funcionalidad intacta (selector, evolución, detalle, fichas).
- Tests OK; desplegado.