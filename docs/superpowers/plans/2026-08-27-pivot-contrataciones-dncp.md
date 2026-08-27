# Datos Públicos — PIVOT a contratación DNCP multi-entidad — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reestructurar el proyecto para que gire exclusivamente sobre contratación pública DNCP (motor multi-entidad por SICP/año + indicadores OCP + web/lab solo-DNCP), eliminando todo lo de presupuesto.

**Architecture:** Mantener el motor DNCP ya existente (parametrizado por SICP/año); eliminar el módulo de presupuesto; rediseñar web (`gasto.html`→`analisis.html` con indicadores OCP sobre contratos) y lab a solo-DNCP; reescribir `DATA_INVENTORY.md`, `README.md`, `AGENTS.md` y el PDF maestro (local).

**Tech Stack:** Python 3.10 (stdlib), JS vanilla, HTML/CSS (diseño 2026), GitHub Actions, git.

---

## Contexto
- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- Antes del pivot: el repo tiene módulo de contratación (funciona) + módulo de presupuesto (se elimina).
- Git historial conserva todo; se crea un tag de respaldo `v0-pre-pivot`.
- El PDF maestro vive SOLO local (no versionado). Regla AGENTS.md.

---

### Task 1: Tag de respaldo + commit de estado previo

**Files:**
- N/A (git)

- [ ] **Step 1: Push cualquier pendiente y crear tag de respaldo**

```bash
git status --porcelain
git add -A && git commit -m "chore: estado pre-pivot (backup)" || echo "sin cambios"
git tag v0-pre-pivot
git push --tags
```
Expected: tag `v0-pre-pivot` creado (el historial completo queda etiquetado).

---

### Task 2: Eliminar el módulo de presupuesto

**Files:**
- Delete: `scripts/presupuesto_2024.py`
- Delete: `scripts/tests/test_presupuesto_2024.py`
- Delete: `data/presupuesto_ejecucion_2024.csv`
- Delete: `docs/presupuesto/` (carpeta completa)
- Delete: `www/datos/presupuesto-ejecucion-2024.json`
- Delete: `docs/superpowers/specs/2026-08-27-presupuesto-ejecucion-2024.md`
- Delete: `docs/superpowers/specs/2026-08-27-integracion-ciclo-presupuesto-gasto.md`
- Delete: `docs/superpowers/specs/2026-08-26-inventario-presupuesto-2024.md`
- Delete: `docs/superpowers/plans/2026-08-27-presupuesto-ejecucion-2024.md`
- Delete: `docs/superpowers/plans/2026-08-27-integracion-ciclo-presupuesto-gasto.md`
- Delete: `docs/superpowers/plans/2026-08-26-inventario-presupuesto-2024.md`

- [ ] **Step 1: Eliminar archivos con git rm**

```bash
git rm scripts/presupuesto_2024.py scripts/tests/test_presupuesto_2024.py data/presupuesto_ejecucion_2024.csv www/datos/presupuesto-ejecucion-2024.json
git rm -r docs/presupuesto
git rm docs/superpowers/specs/2026-08-27-presupuesto-ejecucion-2024.md docs/superpowers/specs/2026-08-27-integracion-ciclo-presupuesto-gasto.md docs/superpowers/specs/2026-08-26-inventario-presupuesto-2024.md
git rm docs/superpowers/plans/2026-08-27-presupuesto-ejecucion-2024.md docs/superpowers/plans/2026-08-27-integracion-ciclo-presupuesto-gasto.md docs/superpowers/plans/2026-08-26-inventario-presupuesto-2024.md
```

- [ ] **Step 2: Verificar que los tests siguen pasando (los de presupuesto se fueron; el resto debe quedar OK)**

```bash
python -B -m unittest discover -s scripts/tests
```
Expected: corren los tests de contratación (test_dncp, test_generar_web, test_indicadores_gasto, test_publicar_sitio) — TODOS OK. NO deben ejecutarse tests de presupuesto (se eliminaron).

- [ ] **Step 3: Commit**

```bash
git commit -m "refactor: remove budget module (pre-pivot to contracts-only)"
```

- [ ] **Step 4: Limpiar el CSV/JSON de presupuesto también del `_site` si existiera (regenerar build en Task 5)**

(No hace falta ahora; se regenera en deploy.)

---

### Task 3: Rediseñar la web — página "Análisis" (indicadores OCP sobre contratos)

**Files:**
- Create: `www/analisis.html`
- Create: `www/js/analisis.js`
- Delete: `www/gasto.html`
- Delete: `www/js/gasto.js`
- Modify: nav en todas las páginas (`www/index.html`, `www/datos.html`, `www/metodologia.html`, `www/demo.html`) para referenciar `analisis.html` en vez de `gasto.html`

- [ ] **Step 1: Crear `www/js/analisis.js`**

Base: `indicadores-gasto-2026.json` (contiene procesos, monto_total, proveedores_distintos, por_categoria, por_tipo_procedimiento, top_proveedores). Presentarlos como **indicadores de contratación**:

```javascript
const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

function renderBarras(datos, etiquetaCampo, valorCampo) {
  const total = datos.reduce((s, d) => s + d[valorCampo], 0) || 1;
  return datos.map(d => {
    const pct = (d[valorCampo] / total) * 100;
    return `<div class="barra-fila">
      <div class="etiqueta" title="${d[etiquetaCampo]}">${d[etiquetaCampo]}</div>
      <div class="barra-track"><div class="barra" style="width:${Math.max(pct, 1)}%"></div></div>
      <div class="barra-valores">${FMT.format(d[valorCampo])} · <strong>${FMT2.format(pct)}%</strong></div>
    </div>`;
  }).join("");
}

fetch("datos/indicadores-gasto-2026.json")
  .then(r => r.json())
  .then(d => {
    const metricas = `
      <div class="metricas">
        <div class="metrica"><div class="valor">${FMT.format(d.procesos || 0)}</div><div class="etiqueta">Procesos 2026</div></div>
        <div class="metrica"><div class="valor">${FMT.format(d.monto_total || 0)}</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
        <div class="metrica"><div class="valor">${FMT.format(d.proveedores_distintos || 0)}</div><div class="etiqueta">Proveedores distintos</div></div>
      </div>`;
    const cat = d.por_categoria && d.por_categoria.length
      ? `<h2>Distribución por categoría</h2>${renderBarras(d.por_categoria, "categoria", "monto")}` : "";
    const tipo = d.por_tipo_procedimiento && d.por_tipo_procedimiento.length
      ? `<h2>¿Cómo se contrata? (procedimiento)</h2>${renderBarras(d.por_tipo_procedimiento, "tipo", "monto")}` : "";
    const top = d.top_proveedores && d.top_proveedores.length
      ? `<h2>Concentración por proveedor</h2><div class="tabla-envolvente"><table>
           <thead><tr><th>Proveedor</th><th>Monto (PYG)</th><th>% del total</th></tr></thead>
           <tbody>${d.top_proveedores.map(p => {
             const pct = (p.monto / d.monto_total) * 100;
             return `<tr><td>${p.proveedor}</td><td class="monto">${FMT.format(p.monto)}</td><td class="monto">${FMT2.format(pct)}%</td></tr>`;
           }).join("")}</tbody>
         </table></div>` : "";
    document.getElementById("analisis").innerHTML = metricas + cat + tipo + top;
  })
  .catch(e => { document.getElementById("analisis").innerHTML = `<p class="vacio">Error: ${e.message}</p>`; });
```

- [ ] **Step 2: Crear `www/analisis.html`** (con menú; referencia a `js/analisis.js`; contenedor `#analisis`; nota "indicadores de contratación adjudicada, patrones OCP").

- [ ] **Step 3: Eliminar `gasto.html` y `gasto.js`**

```bash
git rm www/gasto.html www/js/gasto.js
```

- [ ] **Step 4: Actualizar la navegación** de `index.html`, `datos.html`, `metodologia.html`, `demo.html`: reemplazar `gasto.html` por `analisis.html` en el `<ul>` del nav.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: pivot web to contracts-only analysis page (OCP indicators)"
```

---

### Task 4: Rediseñar el lab a solo-DNCP

**Files:**
- Modify: `lab/index.html`, `lab/pipelines.html`, `lab/datos.html`

- [ ] **Step 1: Actualizar contenido del lab**

- `lab/index.html`: métricas del motor de contratación (procesos 2026, proveedores, montos — leer `../www/datos/indicadores-gasto-2026.json`); estado del pipeline (fuente DNCP, última ejecución, tests).
- `lab/pipelines.html`: P1 = motor DNCP (descarga → join OCDS → filtro SICP → validación → publica), parametrizable por entidad/año. Eliminar referencias a presupuesto.
- `lab/datos.html`: datasets de contratación por entidad+año (2024, 2026) con trazabilidad. Eliminar presupuesto.

- [ ] **Step 2: Commit**

```bash
git add lab/ && git commit -m "feat: pivot lab to contracts DNCP engine status"
```

---

### Task 5: Reescribir `DATA_INVENTORY.md`, `README.md`, `AGENTS.md`

**Files:**
- Modify: `DATA_INVENTORY.md`, `README.md`, `AGENTS.md`

- [ ] **Step 1: Reescribir `DATA_INVENTORY.md` a foco contratación DNCP**

Estructura:
1. Resumen: fuente central = DNCP (datos abiertos, CC BY 4.0, API/CSV por año).
2. La fuente DNCP: cómo aislar entidades (SICP), datasets (records/awards/contracts), licencia, limitaciones.
3. Catálogo de entidades con datos (a empezar: Municipalidad de Asunción SICP 108; el motor es parametrizable).
4. Brechas de la contratación (lo que el portal NO da: nómina, ejecución presupuestaria — brechas conocidas, referenciadas).
5. Trazabilidad.

(Se eliminan dominios de presupuesto/salarios/territorial del foco; quedan referenciados como brechas.)

- [ ] **Step 2: Reescribir `README.md`**

Posicionamiento nuevo (multi-entidad DNCP), sitios, estructua, estado, cómo contribuir.

- [ ] **Step 3: Actualizar `AGENTS.md`** — conservar la regla del plan maestro (solo local) y ajustar la estructura a solo-contratación.

- [ ] **Step 4: Commit**

```bash
git add DATA_INVENTORY.md README.md AGENTS.md && git commit -m "docs: pivot inventory/readme/agents to contracts-only"
```

---

### Task 6: Reescribir el PDF maestro a solo-contrataciones (solo local)

**Files:**
- N/A (local, no versionado): `DATOS PÚBLICOS - DOCUMENTO MAESTRO DEL PROYECTO.pdf` en la raíz local.

- [ ] **Step 1: Backup del PDF actual**

```bash
Copy-Item "DATOS PÚBLICOS - DOCUMENTO MAESTRO DEL PROYECTO.pdf" "_plan_backup_pre-pivot.pdf"
```

- [ ] **Step 2: Generar el nuevo PDF maestro** (con PyMuPDF, en el directorio local, NO versionado)

Contenido del nuevo documento maestro (solo contratación DNCP multi-entidad):
1. Identidad: Datos Públicos = contratación pública de Paraguay (DNCP), entidad por entidad. Primer caso: Muni Asunción.
2. Objetivo: hacer la contratación pública comprensible y verificable.
3. Origen de datos: DNCP (datos abiertos, OCDS, CC BY 4.0).
4. Motor: plantilla parametrizada por SICP (entidad) + año; sin reconstruir por entidad.
5. Indicadores (patrones OCP): distribución por categoría, % método (abierto/directo), concentración de proveedores, tiempos de ciclo.
6. Producto web: explorar por entidad/año, análisis, datos, metodología, demo.
7. Laboratorio: estado del motor.
8. Trazabilidad y limitaciones. Regla: solo fuentes que publican datos abiertos (no romper captchas ni OCR).
9. Frontera/incidencia: qué hace falta (nómina, presupuesto) — agenda, no promesa.

(Generar el texto en un archivo temp y construir el PDF con PyMuPDF.)

- [ ] **Step 3: Verificar que el PDF no se versiona (git ignorado)** y el backup también (patrón `_plan_backup*.pdf` ya ignorado).

```bash
git check-ignore "DATOS PÚBLICOS - DOCUMENTO MAESTRO DEL PROYECTO.pdf"
git check-ignore "_plan_backup_pre-pivot.pdf"
```
Expected: ambos ignorados.

- [ ] **Step 4: NO commit** (el PDF es solo local). Registrar en el log del proyecto que se reescribió.

---

### Task 7: Verificación integral + push + deploy

**Files:**
- N/A

- [ ] **Step 1: Tests**

```bash
python -B -m unittest discover -s scripts/tests
```
Expected: tests de contratación OK; no quedan tests de presupuesto.

- [ ] **Step 2: Verificar que no quedan referencias a presupuesto en el repo**

```bash
git grep -i presupuesto -- ':!docs/superpowers/specs/2026-08-27-pivot-contrataciones-dncp.md' || echo "sin referencias"
git grep -i "hesaka\|MEF\|rendición" 2>/dev/null | head -20
```
Expected: no hay referencias en código/web activa (solo en la spec del pivot o brechas puntuales de DATA_INVENTORY).

- [ ] **Step 3: Commit de la spec/plan del pivot + push**

```bash
git add docs/superpowers/specs/2026-08-27-pivot-contrataciones-dncp.md docs/superpowers/plans/2026-08-27-pivot-contrataciones-dncp.md
git commit -m "docs: pivot spec and plan"
git push
git push --tags
```

- [ ] **Step 4: Esperar deploy y verificar el dominio**

```bash
gh run list --workflow deploy-pages --limit 1 --json status,conclusion
```
Verificar `https://datospublicos.muchotexto.net/` y `/analisis.html` (200).

---

## Criterios de éxito (verificación final)

- Repo sin presupuesto/rendición/Hesakã/MEF en actividad.
- Web con página "Análisis" (indicadores OCP sobre contratos) en lugar de "Gasto"; selector entidad/año en Explorar.
- Lab a solo-DNCP.
- DATA_INVENTORY/README/AGENTS reescritos.
- PDF maestro reescrito (local, ignorado).
- Tests pasan; deploy OK; dominio responde.