# Datos Públicos — Restaurar buscador de contratos — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Añadir la sección "Contratos" (buscador + tabla) en `www/municipalidad.html`, alineada al selector de año.

**Architecture:** Reutilizar `normalizar`/`renderTabla`/`filaTabla` del historial (`app.js`) dentro de `municipalidad.js`, cargando `datos/contrataciones-{año}.json` según el selector existente.

**Tech Stack:** JS vanilla, HTML/CSS.

---

### Task 1: HTML — sección Contratos en municipalidad.html

- [ ] Step 1: En `www/municipalidad.html`, añadir tras la sección "Evolución por año" (antes de "Principales proveedores") un bloque:

```html
<section class="ind-bloque" style="margin-bottom:1.25rem;">
  <header class="ind-bloque-head">
    <h2>Procesos / Contratos</h2>
    <p>La tabla del ejercicio seleccionado. Los procesos sin proveedor son llamados sin adjudicación registrada.</p>
  </header>
  <div class="ind-bloque-cuerpo">
    <div class="filtros">
      <input type="search" id="busqueda" placeholder="Buscar por objeto o proveedor...">
      <select id="filtro-categoria">
        <option value="">Todas las categorías</option>
        <option value="Bienes">Bienes</option>
        <option value="Servicios">Servicios</option>
        <option value="Obras">Obras</option>
      </select>
    </div>
    <div class="tabla-envolvente">
      <table id="tabla">
        <thead><tr><th>Objeto</th><th>Categoría</th><th>Proveedor</th><th>Monto (PYG)</th><th>Adjudicación</th><th>Contrato</th><th>Enlace</th></tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
</section>
```

- [ ] Step 2: Commit — `git add www/municipalidad.html && git commit -m "feat: contracts search section in profile page"`

---

### Task 2: JS — lógica de búsqueda en municipalidad.js

- [ ] Step 1: Añadir a `www/js/municipalidad.js`:

```javascript
function normalizar(texto) {
  return (texto || "").toLowerCase()
    .replace(/[áàäâ]/g, "a").replace(/[éèëê]/g, "e")
    .replace(/[íìïî]/g, "i").replace(/[óòöô]/g, "o")
    .replace(/[úùüû]/g, "u").replace(/ñ/g, "n");
}

let CONTRATOS = [];

async function renderContratos(anio) {
  try { CONTRATOS = await (await fetch(`datos/contrataciones-${anio}.json`)).json(); }
  catch { CONTRATOS = []; }
  renderTabla();
}

function renderTabla() {
  const q = normalizar(document.getElementById("busqueda").value);
  const cat = document.getElementById("filtro-categoria").value;
  const filas = CONTRATOS.filter(d =>
    (!cat || d.categoria === cat) &&
    (!q || normalizar(d.objeto + " " + (d.proveedor || "")).includes(q))
  );
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = filas.length === 0
    ? "<tr><td colspan='7' class='vacio'>Sin resultados</td></tr>"
    : filas.map(filaContrato).join("");
}

function filaContrato(d) {
  const monto = d.monto_nulo ? "<td class='monto vacio'>—</td>" : `<td class='monto'>${FMT.format(d.monto)}</td>`;
  const ad = d.fecha_adjudicacion ? d.fecha_adjudicacion.slice(0, 10) : "—";
  const co = d.fecha_contrato ? d.fecha_contrato.slice(0, 10) : "—";
  const prov = d.proveedor || "<span class='vacio'>Sin adjudicación</span>";
  const cc = d.categoria ? "cat-" + d.categoria.replace(/\s+/g, "") : "";
  const cat = d.categoria ? `<span class="cat-etiqueta ${cc}">${d.categoria}</span>` : "—";
  return `<tr><td>${d.objeto}</td><td>${cat}</td><td>${prov}</td>${monto}<td>${ad}</td><td>${co}</td><td><a href="${d.url_muni}" target="_blank" rel="noopener">ver</a></td></tr>`;
}
```

- [ ] Step 2: En `init()`, tras `renderSerie()`, cargar los contratos del año default y enlazar filtros:

```javascript
  renderContratos("2026");
  document.getElementById("busqueda").addEventListener("input", renderTabla);
  document.getElementById("filtro-categoria").addEventListener("change", renderTabla);
  sel.addEventListener("change", e => { renderDetalle(e.target.value); renderContratos(e.target.value); });
```

- [ ] Step 3: Commit — `git add www/js/municipalidad.js && git commit -m "feat: contracts table search in profile JS"`

---

### Task 3: Verificación + push

- [ ] Servir local: municipalidad con tabla, búsqueda, filtro, cambio de año.
- [ ] `python -B -m unittest discover -s scripts/tests` (OK).
- [ ] Commit docs (spec/plan) + `git push`.

---

## Criterios de éxito
- Municipalidad muestra sección "Procesos/Contratos" con tabla del año.
- Búsqueda por texto y filtro por categoría funcionan (normalización de tildes).
- Cambiar año recarga indicadores + contratos.
- Tests OK; desplegado.