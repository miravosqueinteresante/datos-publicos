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