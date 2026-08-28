const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

function bloque(titulo, subtitulo, contenido) {
  return `
    <section class="ind-bloque">
      <header class="ind-bloque-head">
        <h2>${titulo}</h2>
        ${subtitulo ? `<p>${subtitulo}</p>` : ""}
      </header>
      <div class="ind-bloque-cuerpo">${contenido}</div>
    </section>`;
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

fetch("datos/indicadores-gasto-2026.json")
  .then(r => r.json())
  .then(d => {
    const metricas = `
      <div class="metricas">
        <div class="metrica"><div class="valor">${FMT.format(d.procesos || 0)}</div><div class="etiqueta">Procesos 2026</div></div>
        <div class="metrica"><div class="valor">${FMT.format(d.monto_total || 0)}</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
        <div class="metrica"><div class="valor">${FMT.format(d.proveedores_distintos || 0)}</div><div class="etiqueta">Proveedores distintos</div></div>
      </div>`;

    const partes = [];

    partes.push(bloque(
      "Resumen", "Panorama general de la contratación adjudicada en el ejercicio", metricas
    ));

    if (d.por_categoria && d.por_categoria.length) {
      partes.push(bloque(
        "Distribución por categoría",
        "Bienes, servicios y obras: dónde se concentra el monto adjudicado",
        barras(d.por_categoria, "categoria", "monto")
      ));
    }

    if (d.por_tipo_procedimiento && d.por_tipo_procedimiento.length) {
      partes.push(bloque(
        "¿Cómo se contrata?",
        "Monto por método de procedimiento: licitación, menor cuantía, directo…",
        barras(d.por_tipo_procedimiento, "tipo", "monto")
      ));
    }

    if (d.top_proveedores && d.top_proveedores.length) {
      const filas = d.top_proveedores.map((p, i) => {
        const pct = (p.monto / d.monto_total) * 100;
        return `<tr>
          <td><span class="rank">${i + 1}</span> ${p.proveedor}</td>
          <td class="monto">${FMT.format(p.monto)}</td>
          <td class="monto">${FMT2.format(pct)}%</td>
        </tr>`;
      }).join("");
      partes.push(bloque(
        "Concentración por proveedor",
        "Los mayores receptores de contratos adjudicados del ejercicio",
        `<div class="tabla-envolvente"><table>
          <thead><tr><th>Proveedor</th><th>Monto (PYG)</th><th>% del total</th></tr></thead>
          <tbody>${filas}</tbody>
        </table></div>`
      ));
    }

    document.getElementById("analisis").innerHTML = partes.join("");
  })
  .catch(e => {
    document.getElementById("analisis").innerHTML = `<p class="vacio">Error al cargar datos: ${e.message}</p>`;
  });