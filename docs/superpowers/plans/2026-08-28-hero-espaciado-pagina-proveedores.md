# Datos Públicos — Espaciado hero + página Proveedores — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Aumentar espaciado del hero y crear la página `www/proveedores.html` (10 fichas) con menú y enlace desde el perfil.

**Architecture:** CSS (`index.html` hero) + nueva página `proveedores.html` con JS de fichas extraído de `municipalidad.js`; `municipalidad.html` conserva serie/indicadores, quita fichas y enlaza a la nueva página.

**Tech Stack:** HTML/CSS/JS vanilla. Sin cambios de datos.

---

### Task 1: Espaciado del hero

**Files:**
- Modify: `www/index.html`

- [ ] **Step 1: Aumentar `margin-bottom` del `.lead`**

En la regla `.hero .lead` (línea ~16): `margin: 0 auto 1.4rem` → `margin: 0 auto 2.5rem`.

- [ ] **Step 2: Commit** — `git add www/index.html && git commit -m "feat: more spacing between hero text and CTA buttons"`

---

### Task 2: `www/js/proveedores.js`

**Files:**
- Create: `www/js/proveedores.js`

- [ ] **Step 1: Crear el JS** — extraer de `municipalidad.js` las funciones de fichas (`FMT`, `FMT2`, `renderFichas`) y un `init` que carga `datos/proveedores.json`.

```javascript
const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

function renderFichas(lista) {
  const el = document.getElementById("fichas-proveedores");
  el.innerHTML = `<div class="fichas-grid">${lista.map(p => `
    <details class="ficha">
      <summary>
        <span class="rank">${p.posicion}</span> <strong>${p.proveedor}</strong>
        <span class="ficha-resumen">${FMT.format(p.monto_total)} PYG · ${p.contratos} contratos</span>
      </summary>
      <div class="ficha-detalle">
        <div class="metricas">
          <div class="metrica"><div class="valor">${FMT.format(p.monto_total)}</div><div class="etiqueta">Monto total</div></div>
          <div class="metrica"><div class="valor">${p.contratos}</div><div class="etiqueta">Contratos</div></div>
          <div class="metrica"><div class="valor">${p.anios_activos}</div><div class="etiqueta">Años activos</div></div>
          <div class="metrica"><div class="valor">${p.categoria_principal || "—"}</div><div class="etiqueta">Categoría principal</div></div>
          <div class="metrica"><div class="valor">${FMT2.format(p.pct_directo)}%</div><div class="etiqueta">Por vía directa</div></div>
        </div>
        <h4>Contratos</h4>
        <div class="tabla-envolvente"><table>
          <thead><tr><th>Objeto</th><th>Año</th><th>Monto</th><th>Procedimiento</th><th>Enlace</th></tr></thead>
          <tbody>${p.contratos_lista.map(c => `<tr>
            <td>${c.objeto}</td><td>${c.anio || "—"}</td><td class="monto">${FMT.format(c.monto)}</td>
            <td>${c.procedimiento || "—"}</td>
            <td>${c.url ? `<a href="${c.url}" target="_blank" rel="noopener">ver</a>` : "—"}</td>
          </tr>`).join("")}</tbody>
        </table></div>
      </div>
    </details>`).join("")}</div>`;
}

async function init() {
  try {
    const prov = await (await fetch("datos/proveedores.json")).json();
    renderFichas(prov);
  } catch {}
}
init();
```

- [ ] **Step 2: Commit** — `git add www/js/proveedores.js && git commit -m "feat: supplier fichas JS module"`

---

### Task 3: `www/proveedores.html`

**Files:**
- Create: `www/proveedores.html`

- [ ] **Step 1: Crear la página** — cabecera + contenedor `#fichas-proveedores` + `<script src="js/proveedores.js">`. Menú nuevo (Proveedores activo).

- [ ] **Step 2: Commit** — `git add www/proveedores.html && git commit -m "feat: supplier top-10 page (proveedores.html)"`

---

### Task 4: Ajustar `municipalidad.html` (quitar fichas → enlace) y `municipalidad.js`

**Files:**
- Modify: `www/municipalidad.html`
- Modify: `www/js/municipalidad.js`

- [ ] **Step 1:** En `municipalidad.html`, **eliminar** la sección `id="fichas-proveedores"` y su carga; **añadir** en su lugar una carta/enlace:
  - Un `<div class="ind-bloque">` con `<h2>Principales proveedores</h2>` + párrafo + `<a href="proveedores.html" class="btn btn-primario">Ver principales proveedores →</a>`.
- [ ] **Step 2:** En `municipalidad.js`, quitar `renderFichas` y el `fetch("datos/proveedores.json")` (el `init` deja de cargar fichas; `renderSerie`/`renderDetalle` se mantienen).
- [ ] **Step 3: Commit** — `git add www/municipalidad.html www/js/municipalidad.js && git commit -m "refactor: move supplier fichas from profile to dedicated page"`

---

### Task 5: Menú en index/raíz, datos, metodología + verificación + push

**Files:**
- Modify: `www/index.html`, `www/datos.html`, `www/metodologia.html` (nav con Proveedores)

- [ ] **Step 1:** Añadir `<li><a href="proveedores.html">Proveedores</a></li>` al nav de las 4 páginas (raíz, municipalidad, datos, metodología), en la posición tras Municipalidad.

- [ ] **Step 2: Verificar**
  - `python -B -m unittest discover -s scripts/tests` (OK).
  - Servir local: `proveedores.html`, `js/proveedores.js`, `datos/proveedores.json`, perfiles 200; nav uniforme en 5 páginas.
  - Comprobar que `municipalidad.html` ya no carga fichas (grep `fichas-proveedores`).

- [ ] **Step 3: Commit docs (spec/plan) + `git push`** (deploy automático).

- [ ] **Step 4: Verificar producción** (`proveedores.html` 200, menú).

---

## Criterios de éxito
- Hero con más aire.
- `proveedores.html` con 10 fichas desplegables.
- Menú: Municipalidad · Proveedores · Datos · Metodología.
- Perfil enlaza a la página nueva; sin fichas embebidas.
- Tests OK; desplegado.