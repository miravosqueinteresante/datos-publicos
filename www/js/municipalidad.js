const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });
const ANIOS = ["2023", "2024", "2025", "2026"];

let INDICADORES = {};
let CACHE_V = "";

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
  const maxMonto = Math.max(...ANIOS.map(a => INDICADORES[a]?.monto_adjudicado_total || 0), 1);
  const filas = ANIOS.map(a => {
    const d = INDICADORES[a];
    if (!d) return `<tr><td>${a}</td><td colspan="4" class="vacio">sin datos</td></tr>`;
    const pct = (d.monto_adjudicado_total / maxMonto) * 100;
    return `<tr>
      <td><strong>${a}</strong></td>
      <td>${FMT.format(d.procesos || 0)}</td>
      <td class="monto">${FMT.format(d.monto_adjudicado_total || 0)}</td>
      <td>${FMT.format(d.proveedores_distintos || 0)}</td>
      <td><div class="barra-track" style="min-width:120px"><div class="barra" style="width:${Math.max(pct, 1)}%"></div></div></td>
    </tr>`;
  }).join("");
  document.getElementById("serie-anual").innerHTML = `
    <table>
      <thead><tr><th>Año</th><th>Procesos</th><th>Monto adjudicado (PYG)</th><th>Proveedores</th><th>Monto relativo</th></tr></thead>
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
      <div class="metrica"><div class="valor">${FMT.format(d.valor_estimado_total || 0)}</div><div class="etiqueta">Valor estimado (PYG)</div></div>
      <div class="metrica"><div class="valor">${FMT.format(d.monto_adjudicado_total || 0)}</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
      <div class="metrica"><div class="valor">${FMT.format(d.monto_contratado_total || 0)}</div><div class="etiqueta">Monto contratado (PYG)</div></div>
    </div>
    <p class="nota">Sin adjudicación registrada: ${FMT.format(d.procesos_sin_adjudicacion || 0)} procesos. El monto adjudicado suma solo las adjudicaciones; el valor estimado incluye también los procesos aún no adjudicados.</p>`;
  if (d.por_categoria && d.por_categoria.length) {
    el.insertAdjacentHTML("beforeend", bloque("Distribución por categoría", "Monto adjudicado por categoría", barras(d.por_categoria, "categoria", "monto")));
  }
  if (d.por_tipo_procedimiento && d.por_tipo_procedimiento.length) {
    el.insertAdjacentHTML("beforeend", bloque("¿Cómo se contrata?", "Monto adjudicado por método de procedimiento", barras(d.por_tipo_procedimiento, "tipo", "monto")));
  }
  if (d.top_proveedores && d.top_proveedores.length) {
    el.insertAdjacentHTML("beforeend", bloque("Concentración por proveedor", "Sobre el monto adjudicado total",
      `<div class="tabla-envolvente"><table><thead><tr><th>Proveedor</th><th>Monto adjudicado (PYG)</th><th>% del adjudicado</th></tr></thead>
       <tbody>${d.top_proveedores.map((p, i) => {
         const pct = (p.monto / d.monto_adjudicado_total) * 100;
         return `<tr><td><span class="rank">${i + 1}</span> ${p.proveedor}</td><td class="monto">${FMT.format(p.monto)}</td><td class="monto">${FMT2.format(pct)}%</td></tr>`;
       }).join("")}</tbody></table></div>`));
  }
}

function normalizar(texto) {
  return (texto || "").toLowerCase()
    .replace(/[áàäâ]/g, "a").replace(/[éèëê]/g, "e")
    .replace(/[íìïî]/g, "i").replace(/[óòöô]/g, "o")
    .replace(/[úùüû]/g, "u").replace(/ñ/g, "n");
}

let CONTRATOS = [];
let PAGINA = 1;
const POR_PAGINA = 10;

async function renderContratos(anio) {
  const q = CACHE_V ? `?v=${CACHE_V}` : "";
  try { CONTRATOS = await (await fetch(`datos/contrataciones-${anio}.json${q}`)).json(); }
  catch { CONTRATOS = []; }
  PAGINA = 1;
  renderTabla();
}

function renderTabla() {
  const q = normalizar(document.getElementById("busqueda").value);
  const cat = document.getElementById("filtro-categoria").value;
  const filtradas = CONTRATOS.filter(d =>
    (!cat || d.categoria === cat) &&
    (!q || normalizar(d.objeto + " " + (d.proveedor || "")).includes(q))
  );
  const total = filtradas.length;
  const paginas = Math.max(1, Math.ceil(total / POR_PAGINA));
  if (PAGINA > paginas) PAGINA = paginas;
  const inicio = (PAGINA - 1) * POR_PAGINA;
  const visibles = filtradas.slice(inicio, inicio + POR_PAGINA);
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = visibles.length === 0
    ? "<tr><td colspan='7' class='vacio'>Sin resultados</td></tr>"
    : visibles.map(filaContrato).join("");
  const nav = document.getElementById("paginacion");
  if (total <= POR_PAGINA) { nav.innerHTML = ""; return; }
  const desde = inicio + 1;
  const hasta = Math.min(inicio + POR_PAGINA, total);
  nav.innerHTML = `
    <button id="pag-prev" ${PAGINA === 1 ? "disabled" : ""}>Anterior</button>
    <span class="pag-info">Mostrando ${desde}–${hasta} de ${total}</span>
    <button id="pag-next" ${PAGINA === paginas ? "disabled" : ""}>Siguiente</button>`;
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

async function init() {
  try { const m = await (await fetch("datos/metadata-2026.json")).json(); CACHE_V = m.generado_en || ""; } catch {}
  const q = CACHE_V ? `?v=${CACHE_V}` : "";
  for (const a of ANIOS) {
    try { INDICADORES[a] = await (await fetch(`datos/indicadores-gasto-${a}.json${q}`)).json(); }
    catch { INDICADORES[a] = null; }
  }
  renderDetalle("2026");
  renderSerie();
  renderContratos("2026");
  const sel = document.getElementById("sel-anio-muni");
  sel.addEventListener("change", e => { renderDetalle(e.target.value); renderContratos(e.target.value); });
  document.getElementById("busqueda").addEventListener("input", () => { PAGINA = 1; renderTabla(); });
  document.getElementById("filtro-categoria").addEventListener("change", () => { PAGINA = 1; renderTabla(); });
  document.getElementById("paginacion").addEventListener("click", e => {
    if (e.target.id === "pag-prev" && PAGINA > 1) { PAGINA--; renderTabla(); }
    if (e.target.id === "pag-next") { PAGINA++; renderTabla(); }
  });
}

init().catch(e => {
  document.getElementById("detalle-anual").innerHTML = `<p class="vacio">Error al cargar datos: ${e.message}</p>`;
});