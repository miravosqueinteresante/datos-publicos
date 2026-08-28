# Datos Públicos — Serie temporal 2023-2026 — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generar y publicar la serie temporal de contrataciones de la Municipalidad de Asunción (2023-2026) con comparativa en Análisis y selector de año en Explorar.

**Architecture:** Motor existente por año (SICP 108 default) para generar los CSV faltantes; `generar_datos_web.py` produce JSON por año; `indicadores_gasto.py` produce indicadores por año; web actualizada con select de año + comparativa.

**Tech Stack:** Python 3.10 (stdlib), JS vanilla, HTML/CSS.

---

## Contexto
- Datasets existentes: `data/contrataciones_muni_2024.csv`, `_2026.csv`.
- Web: `www/js/app.js` (Explorar, año fijo 2026), `www/js/analisis.js` (Análisis, un año), `generar_datos_web.py` (2024+2026), `indicadores_gasto.py` (solo 2026 por hardcode en salida).

---

### Task 1: Generar los CSV de 2023 y 2025

**Files:**
- Create: `data/contrataciones_muni_2023.csv`, `data/contrataciones_muni_2025.csv` (generados)

- [ ] **Step 1: Ejecutar el motor para 2023 y 2025**

```bash
python scripts/dncp_contrataciones.py 2023
python scripts/dncp_contrataciones.py 2025
```
Expected: cada corrida descarga el ZIP del año, filtra SICP 108, escribe `data/contrataciones_muni_{año}.csv`.

- [ ] **Step 2: Verificar los CSV** (conteos y consistencia)

```bash
python -c "import csv; rows=list(csv.DictReader(open('data/contrataciones_muni_2023.csv',encoding='utf-8'))); print('2023:', len(rows))"
python -c "import csv; rows=list(csv.DictReader(open('data/contrataciones_muni_2025.csv',encoding='utf-8'))); print('2025:', len(rows))"
```
Expected: n>0, coherente (~decenas de procesos). Si un año da 0 (posible dato faltante), documentarlo.

- [ ] **Step 3: Commit**

```bash
git add data/contrataciones_muni_2023.csv data/contrataciones_muni_2025.csv
git commit -m "data: add contracts datasets 2023 and 2025 (Muni Asuncion)"
```

---

### Task 2: Generador web multi-año + indicadores por año

**Files:**
- Modify: `scripts/generar_datos_web.py`
- Modify: `scripts/indicadores_gasto.py`
- Modify: `scripts/tests/test_generar_web.py` (si aplica)

- [ ] **Step 1: Ampliar años en `generar_datos_web.py::main`**

```python
def main():
    for anio in ["2023", "2024", "2025", "2026"]:
        generar_contrataciones(anio)
```

- [ ] **Step 2: Generar indicadores por año**

En `scripts/indicadores_gasto.py`, `main()` debe generar `www/datos/indicadores-gasto-{año}.json` para cada año con CSV de contrataciones. Revisar el RUTA_JSON actual (puede estar fijo a 2026) → parametrizarlo.

- [ ] **Step 3: Ejecutar ambos generadores**

```bash
python scripts/generar_datos_web.py
python scripts/indicadores_gasto.py
```
Expected: 4 JSON de contrataciones y 4 de indicadores en `www/datos/`.

- [ ] **Step 4: Tests + Commit**

```bash
python -B -m unittest discover -s scripts/tests
git add scripts/... www/datos/
git commit -m "feat: multi-year web data and per-year indicators (2023-2026)"
```

---

### Task 3: Selector de año en Explorar

**Files:**
- Modify: `www/index.html`
- Modify: `www/js/app.js`

- [ ] **Step 1: Añadir selector en `www/index.html`** (cerca del header o arriba de `#metricas`):

```html
<div class="filtros">
  <label for="sel-anio-explorar"><strong>Ejercicio:</strong></label>
  <select id="sel-anio-explorar">
    <option value="2023">2023</option>
    <option value="2024">2024</option>
    <option value="2025">2025</option>
    <option value="2026" selected>2026</option>
  </select>
</div>
```

- [ ] **Step 2: `app.js` — parametrizar carga por año**

```javascript
async function cargarDatos(anio = "2026") {
  const res = await fetch(`datos/contrataciones-${anio}.json`);
  DATOS = await res.json();
  document.getElementById("portada-anio").textContent = año; // o label
  renderMetricas(); renderProveedores(); renderTabla();
}
document.getElementById("sel-anio-explorar").addEventListener("change", e => cargarDatos(e.target.value));
cargarDatos("2026");
```
(Ajustar los textos del header que mencionan el año si son fijos.)

- [ ] **Step 3: Commit** — `git commit -m "feat: year selector in Explorar"`

---

### Task 4: Comparativa por año en Análisis

**Files:**
- Modify: `www/analisis.html`
- Modify: `www/js/analisis.js`

- [ ] **Step 1: Añadir contenedores en `www/analisis.html`**:

```html
<div id="analisis"></div>
<section class="ind-bloque">
  <header class="ind-bloque-head">
    <h2>Evolución por año</h2>
    <p>Comparativa de la contratación adjudicada 2023-2026</p>
  </header>
  <div class="ind-bloque-cuerpo"><div id="serie-anual"></div></div>
</section>
<section class="ind-bloque">
  <header class="ind-bloque-head">
    <h2>Detalle por año</h2>
    <p><select id="sel-anio-analisis">…2023-2026…</select></p>
  </header>
  <div class="ind-bloque-cuerpo"><div id="detalle-anual"></div></div>
</section>
```

- [ ] **Step 2: `analisis.js` — cargar 4 JSON y renderizar comparativa + detalle**

```javascript
const ANIOS = ["2023","2024","2025","2026"];
async function cargarSubcasos() {
  const inds = {};
  for (const a of ANIOS) {
    try { inds[a] = await (await fetch(`datos/indicadores-gasto-${a}.json`)).json(); }
    catch { inds[a] = null; }
  }
  renderSerie(inds);
  renderDetalle(inds, "2026");
}
function renderSerie(inds) { /* tabla: año | procesos | monto | proveedores | (mini barra de monto relativo) */ }
function renderDetalle(inds, anio) { /* reusar bloques de indicadores del año */ }
document.getElementById("sel-anio-analisis").addEventListener("change", e => renderDetalle(inds, e.target.value));
```

- [ ] **Step 3: Commit** — `git commit -m "feat: multi-year evolution and year detail in Analisis"`

---

### Task 5: Lab (datos.html) — tabla de 4 años + verificación + push

**Files:**
- Modify: `lab/datos.html`

- [ ] **Step 1: Tabla de datasets** — añadir 2023 y 2025 (registros según CSV generado).

- [ ] **Step 2: Verificación final**

```bash
python -B -m unittest discover -s scripts/tests
```
- Servir local y verificar: Explorar con selector, Análisis con comparativa.
- Verificar 8 JSON en `www/datos/`.

- [ ] **Step 3: Commit docs (spec/plan) + `git push`** (deploy automático).

---

## Criterios de éxito
- 4 CSV 2023-2026 de la Muni.
- 4 JSON de contrataciones + 4 de indicadores.
- Explorar con selector de año; Análisis con "Evolución por año" + detalle por año.
- Tests OK; lab con 4 años; pusheado y desplegado.