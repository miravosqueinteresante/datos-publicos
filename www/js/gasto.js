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