const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });
const ANIOS = ["2023", "2024", "2025", "2026"];

let INDICADORES = {};

function bloque(titulo, subtitulo, contenido) {
  return `
    <div class="det-ind">
      <h3>${titulo}</h3>
      ${subtitulo ? `<p class="det-sub">${subtitulo}</p>` : ""}
      <div class="det-cuerpo">${contenido}</div>
    </div>`;
}

function barras(datos, etiquetaCampo, valorCampo) {
  const total = datos.reduce((s, d) => s + d[valorCampo], 0) || 1;
  return `<div class="barras">${datos.map(d => {
    const pct = (d[valorCampo] / total) * 100;
    return `
      <div class="barra-fila">
        <div class="barra-nombre" title="${d[etiquetaCampo]}">${d[etiquetaCampo]}</div>
        <div class="barra-track"><div class="barra" style="width:${Math.max(pct, 1)}%"></div></div>
        <div class="barra-valores">${FMT.format(d[valorCampo])}<span class="barra-pct">${FMT2.format(pct)}%</span></div>
      </div>`;
  }).join("")}</div>`;
}

function renderSerie() {
  const maxMonto = Math.max(...ANIOS.map(a => INDICADORES[a]?.monto_total || 0), 1);
  const filas = ANIOS.map(a => {
    const d = INDICADORES[a];
    if (!d) return `<tr><td>${a}</td><td colspan="4" class="vacio">sin datos</td></tr>`;
    const pct = (d.monto_total / maxMonto) * 100;
    return `<tr>
      <td><strong>${a}</strong></td>
      <td>${FMT.format(d.procesos || 0)}</td>
      <td class="monto">${FMT.format(d.monto_total || 0)}</td>
      <td>${FMT.format(d.proveedores_distintos || 0)}</td>
      <td><div class="barra-track" style="min-width:120px"><div class="barra" style="width:${Math.max(pct, 1)}%"></div></div></td>
    </tr>`;
  }).join("");
  document.getElementById("serie-anual").innerHTML = `
    <table>
      <thead><tr><th>Año</th><th>Procesos</th><th>Monto (PYG)</th><th>Proveedores</th><th>Monto relativo</th></tr></thead>
      <tbody>${filas}</tbody>
    </table>`;
}

function renderDetalle(anio) {
  const d = INDICADORES[anio];
  const el = document.getElementById("detalle-anual");
  if (!d) { el.innerHTML = "<p class='vacio'>Sin datos para " + anio + "</p>"; return; }
  el.innerHTML = `
    <div class="metricas">
      <div class="metrica"><div class="valor">${FMT.format(d.procesos || 0)}</div><div class="etiqueta">Procesos</div></div>
      <div class="metrica"><div class="valor">${FMT.format(d.monto_total || 0)}</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
      <div class="metrica"><div class="valor">${FMT.format(d.proveedores_distintos || 0)}</div><div class="etiqueta">Proveedores distintos</div></div>
    </div>`;
  if (d.por_categoria && d.por_categoria.length) {
    el.insertAdjacentHTML("beforeend", bloque("Distribución por categoría", "Dónde se concentra el monto", barras(d.por_categoria, "categoria", "monto")));
  }
  if (d.por_tipo_procedimiento && d.por_tipo_procedimiento.length) {
    el.insertAdjacentHTML("beforeend", bloque("¿Cómo se contrata?", "Monto por método de procedimiento", barras(d.por_tipo_procedimiento, "tipo", "monto")));
  }
  if (d.top_proveedores && d.top_proveedores.length) {
    el.insertAdjacentHTML("beforeend", bloque("Concentración por proveedor", "Los mayores receptores",
      `<div class="tabla-envolvente"><table><thead><tr><th>Proveedor</th><th>Monto (PYG)</th><th>% del total</th></tr></thead>
       <tbody>${d.top_proveedores.map((p, i) => {
         const pct = (p.monto / d.monto_total) * 100;
         return `<tr><td><span class="rank">${i + 1}</span> ${p.proveedor}</td><td class="monto">${FMT.format(p.monto)}</td><td class="monto">${FMT2.format(pct)}%</td></tr>`;
       }).join("")}</tbody></table></div>`));
  }
}

async function init() {
  for (const a of ANIOS) {
    try { INDICADORES[a] = await (await fetch(`datos/indicadores-gasto-${a}.json`)).json(); }
    catch { INDICADORES[a] = null; }
  }
  renderSerie();
  renderDetalle("2026");
  const sel = document.getElementById("sel-anio-analisis");
  sel.addEventListener("change", e => renderDetalle(e.target.value));
}

init().catch(e => {
  document.getElementById("analisis").innerHTML = `<p class="vacio">Error al cargar datos: ${e.message}</p>`;
});