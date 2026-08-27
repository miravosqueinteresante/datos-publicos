# Datos Públicos — Página "Gasto" — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear `www/gasto.html` mostrando los indicadores de gasto (DNCP) y actualizar el menú de navegación en todas las páginas de la plataforma.

**Architecture:** Página estática + JS vanilla + barras CSS puras, consumiendo `indicadores-gasto-2026.json`. Menú compartido de 4 secciones.

**Tech Stack:** HTML5, CSS (nuevas clases), JS vanilla, JSON.

---

## Contexto
- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`.
- JSON de indicadores: `www/datos/indicadores-gasto-2026.json` (existe, datos reales).
- Páginas actuales con menú: `www/index.html`, `www/datos.html`, `www/metodologia.html` (menú: Explorar · Datos · Metodología).
- CSS compartido: `www/css/style.css`.

---

### Task 1: Añadir clases CSS para barras

**Files:**
- Modify: `www/css/style.css`

- [ ] **Step 1: Añadir al final del CSS**

```css
/* Barras de distribución */
.barra-bloque { margin-bottom: 1rem; }
.barra-fila { display: grid; grid-template-columns: 140px 1fr 150px; align-items: center; gap: .75rem; margin-bottom: .55rem; }
.barra-fila .etiqueta { font-size: .86rem; color: var(--texto-suave); text-align: right; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.barra-track { background: #eef2ff; border-radius: 999px; height: 18px; overflow: hidden; }
.barra { height: 100%; background: var(--primario); border-radius: 999px; min-width: 2px; }
.barra-valores { font-size: .84rem; font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }
.barra-valores strong { color: var(--texto); }
.destacado { color: var(--primario); font-weight: 600; }
```

- [ ] **Step 2: Commit**

```bash
git add www/css/style.css
git commit -m "feat: add bar chart CSS for spend indicators (www)"
```

---

### Task 2: `www/js/gasto.js`

**Files:**
- Create: `www/js/gasto.js`

- [ ] **Step 1: Crear el JS**

```javascript
const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

function renderBarras(contenedorId, datos, etiquetaCampo, valorCampo) {
  const total = datos.reduce((s, d) => s + d[valorCampo], 0) || 1;
  const el = document.getElementById(contenedorId);
  el.innerHTML = datos.map(d => {
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
    document.getElementById("total-procesos").textContent = FMT.format(d.procesos);
    document.getElementById("total-monto").textContent = FMT.format(d.monto_total);
    document.getElementById("total-proveedores").textContent = FMT.format(d.proveedores_distintos);

    renderBarras("barras-categoria", d.por_categoria, "categoria", "monto");

    const provEl = document.getElementById("top-proveedores");
    provEl.innerHTML = d.top_proveedores.map(p => {
      const pct = (p.monto / d.monto_total) * 100;
      return `<tr><td>${p.proveedor}</td><td class="monto">${FMT.format(p.monto)}</td><td class="monto">${FMT2.format(pct)}%</td></tr>`;
    }).join("");

    const tiposEl = document.getElementById("barras-tipo");
    if (d.por_tipo_procedimiento && d.por_tipo_procedimiento.length) {
      renderBarras("barras-tipo", d.por_tipo_procedimiento, "tipo", "monto");
    } else {
      tiposEl.innerHTML = "<p class='vacio'>Sin datos de tipo de procedimiento.</p>";
    }
  })
  .catch(err => {
    document.getElementById("totales").innerHTML =
      `<div class="vacio">Error al cargar indicadores: ${err.message}</div>`;
  });
```

- [ ] **Step 2: Commit**

```bash
git add www/js/gasto.js
git commit -m "feat: add spend indicators renderer (www/js/gasto.js)"
```

---

### Task 3: `www/gasto.html`

**Files:**
- Create: `www/gasto.html`

- [ ] **Step 1: Crear la página**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Gasto en contrataciones</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos</span>
    <ul>
      <li><a href="index.html">Explorar</a></li>
      <li><a href="datos.html">Datos</a></li>
      <li><a href="gasto.html" class="activo">Gasto</a></li>
      <li><a href="metodologia.html">Metodología</a></li>
    </ul>
    <span class="vision">Próximamente: Mapas · Obras · Presupuesto · Indicadores</span>
  </div></nav>

  <header class="portada">
    <h1>Gasto en contrataciones</h1>
    <p class="subtitulo">¿En qué gasta la Municipalidad de Asunción en compras adjudicadas? (2026)</p>
    <p class="meta">Datos de la DNCP · CC BY 4.0 · Contrataciones adjudicadas, no presupuesto total</p>
  </header>

  <main>
    <section id="totales" class="seccion">
      <div class="metricas">
        <div class="metrica"><div class="valor" id="total-procesos">—</div><div class="etiqueta">Procesos</div></div>
        <div class="metrica"><div class="valor" id="total-monto">—</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
        <div class="metrica"><div class="valor" id="total-proveedores">—</div><div class="etiqueta">Proveedores distintos</div></div>
      </div>
    </section>

    <section class="seccion">
      <h2>Distribución por categoría</h2>
      <div id="barras-categoria"></div>
    </section>

    <section class="seccion">
      <h2>Distribución por tipo de procedimiento</h2>
      <div id="barras-tipo"></div>
    </section>

    <section class="seccion">
      <h2>Principales proveedores</h2>
      <div class="tabla-envolvente">
        <table>
          <thead><tr><th>Proveedor</th><th>Monto (PYG)</th><th>% del total</th></tr></thead>
          <tbody id="top-proveedores"></tbody>
        </table>
      </div>
    </section>

    <section class="seccion nota">
      <h2>Metodología</h2>
      <p>Gasto en <strong>contrataciones adjudicadas</strong> de la Municipalidad de Asunción (convocante SICP 108),
      año 2026, desde el portal de datos abiertos de la DNCP (CC BY 4.0). No incluye sueldos ni presupuesto total
      (no publicados en formato abierto; ver <a href="metodologia.html">Metodología</a>).</p>
    </section>
  </main>
  <footer>Datos Públicos — plataforma de infraestructura cívica</footer>
  <script src="js/gasto.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add www/gasto.html
git commit -m "feat: add Gasto page with spend indicators (www)"
```

---

### Task 4: Actualizar el menú en las 3 páginas existentes

**Files:**
- Modify: `www/index.html`, `www/datos.html`, `www/metodologia.html`

- [ ] **Step 1: Añadir el enlace "Gasto" al menú de cada página**

En las 3 páginas, en `<nav class="nav">`, tras el enlace "Datos" añadir:

```html
<li><a href="gasto.html">Gasto</a></li>
```

(Nota: en `gasto.html` el enlace lleva `class="activo"`; en las demás sin clase.)

- [ ] **Step 2: Commit**

```bash
git add www/index.html www/datos.html www/metodologia.html
git commit -m "feat: add Gasto to shared navigation (www)"
```

---

### Task 5: Verificación + push

- [ ] Step 1: Servir local y verificar las 5 rutas: `www/gasto.html`, `www/js/gasto.js`, `www/datos/indicadores-gasto-2026.json`, `www/index.html`, CSS.
- [ ] Step 2: Verificar con node que la lógica de % y barras es correcta sobre el JSON real.
- [ ] Step 3: Commit docs (spec/plan) + `git push` (el deploy de Pages reconstruye `_site/` automáticamente).

---

## Criterios de éxito
- `www/gasto.html` muestra las métricas y barras correctas del JSON.
- Menú de 4 secciones coherente en todas las páginas.
- Etiqueta honesta ("contrataciones adjudicadas").
- Sin dependencias nuevas.