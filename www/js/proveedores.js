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