const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

function renderFichas(lista) {
  const el = document.getElementById("fichas-proveedores");
  el.innerHTML = `<div class="fichas-grid">${lista.map(p => `
    <details class="ficha">
      <summary>
        <span class="rank">${p.posicion}</span> <strong>${p.proveedor}</strong>
        <span class="ficha-resumen">${FMT.format(p.monto_total)} PYG · ${p.adjudicaciones} adjudicaciones · ${p.pct_del_adjudicado}% del adjudicado</span>
      </summary>
      <div class="ficha-detalle">
        <div class="metricas">
          <div class="metrica"><div class="valor num">${FMT.format(p.monto_total)}</div><div class="etiqueta">Monto adjudicado</div></div>
          <div class="metrica"><div class="valor">${p.adjudicaciones}</div><div class="etiqueta">Adjudicaciones</div></div>
          <div class="metrica"><div class="valor">${p.anios_activos}</div><div class="etiqueta">Años activos</div></div>
          <div class="metrica"><div class="valor">${p.categoria_principal || "—"}</div><div class="etiqueta">Categoría principal</div></div>
        </div>
        <h4>Adjudicaciones</h4>
        <div class="tabla-envolvente"><table>
          <thead><tr><th>Objeto</th><th>Año</th><th>Monto</th><th>Procedimiento</th><th>Enlace</th></tr></thead>
          <tbody>${p.adjudicaciones_lista.map(c => `<tr>
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