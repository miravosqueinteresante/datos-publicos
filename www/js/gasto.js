const FMT = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
const FMT2 = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 1 });

const ANIOS = {
  "2024": {
    presupuesto: "datos/presupuesto-ejecucion-2024.json",
    contratos: "datos/contrataciones-2024.json",
    sub: "¿En qué gastó la Municipalidad de Asunción? (2024)",
    meta: "Datos de la Rendición de Cuentas 2024 y la DNCP · CC BY 4.0 · Contrataciones adjudicadas, no presupuesto total",
    esPresupuesto: true,
  },
  "2026": {
    indicadores: "datos/indicadores-gasto-2026.json",
    contratos: "datos/contrataciones-2026.json",
    sub: "¿En qué gasta la Municipalidad de Asunción en compras adjudicadas? (2026)",
    meta: "Datos de la DNCP · CC BY 4.0 · Contrataciones adjudicadas, no presupuesto total",
    esPresupuesto: false,
  },
};

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

function tablaEjecucion(presupuesto) {
  const rows = presupuesto.map(r => {
    const vig = r.presupuesto_vigente != null ? FMT.format(r.presupuesto_vigente) : "—";
    const obl = r.obligado != null ? FMT.format(r.obligado) : "—";
    const pct = r.porcentaje_ejecucion != null ? FMT2.format(r.porcentaje_ejecucion) + "%" : "—";
    const negrita = r.nivel === "TOTAL" ? " style='font-weight:700'" : "";
    return `<tr${negrita}><td>${r.denominacion}</td><td class="monto">${vig}</td><td class="monto">${obl}</td><td class="monto">${pct}</td></tr>`;
  }).join("");
  return `
    <h2>Ejecución del presupuesto 2024 por objeto del gasto</h2>
    <p class="nota">Montos en millones de guaraníes · Fuente: Rendición de Cuentas 2024</p>
    <div class="tabla-envolvente">
      <table>
        <thead><tr><th>Objeto del gasto</th><th>Vigente</th><th>Obligado</th><th>% eje.</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function tablaContratos(contratos, anio) {
  const rows = contratos.map(d => {
    const monto = d.monto_nulo
      ? `<td class="monto vacio">—</td>`
      : `<td class="monto">${FMT.format(d.monto)}</td>`;
    const prov = d.proveedor || "<span class='vacio'>Sin adjudicación</span>";
    return `<tr>
      <td>${d.objeto}</td>
      <td>${d.categoria || "—"}</td>
      <td>${prov}</td>
      ${monto}
      <td><a href="${d.url_muni}" target="_blank" rel="noopener">ver</a></td>
    </tr>`;
  }).join("");
  return `
    <h2>Contrataciones adjudicadas ${anio}</h2>
    <div class="tabla-envolvente">
      <table>
        <thead><tr><th>Objeto</th><th>Categoría</th><th>Proveedor</th><th>Monto (PYG)</th><th>Enlace</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>`;
}

function render2026(d) {
  const conMonto = d.por_categoria || [];
  const total = d.monto_total || conMonto.reduce((s, x) => s + x.monto, 0);
  const metricas = `
    <div class="metricas">
      <div class="metrica"><div class="valor">${FMT.format(d.procesos || 0)}</div><div class="etiqueta">Procesos</div></div>
      <div class="metrica"><div class="valor">${FMT.format(total)}</div><div class="etiqueta">Monto adjudicado (PYG)</div></div>
      <div class="metrica"><div class="valor">${FMT.format(d.proveedores_distintos || 0)}</div><div class="etiqueta">Proveedores distintos</div></div>
    </div>`;
  const cat = d.por_categoria && d.por_categoria.length
    ? `<h2>Distribución por categoría</h2>${renderBarras(d.por_categoria, "categoria", "monto")}`
    : "";
  const tipo = d.por_tipo_procedimiento && d.por_tipo_procedimiento.length
    ? `<h2>Distribución por tipo de procedimiento</h2>${renderBarras(d.por_tipo_procedimiento, "tipo", "monto")}`
    : "";
  const top = d.top_proveedores && d.top_proveedores.length
    ? `<h2>Principales proveedores</h2>
       <div class="tabla-envolvente"><table>
         <thead><tr><th>Proveedor</th><th>Monto (PYG)</th><th>% del total</th></tr></thead>
         <tbody>${d.top_proveedores.map(p => {
           const pct = (p.monto / total) * 100;
           return `<tr><td>${p.proveedor}</td><td class="monto">${FMT.format(p.monto)}</td><td class="monto">${FMT2.format(pct)}%</td></tr>`;
         }).join("")}</tbody>
       </table></div>`
    : "";
  return `${metricas}${cat}${tipo}${top}`;
}

async function cargarAnio(anio) {
  const cfg = ANIOS[anio];
  const el = document.getElementById("contenido-anual");
  el.innerHTML = "<p class='vacio'>Cargando datos…</p>";
  document.getElementById("subtitulo-anual").textContent = cfg.sub;
  document.getElementById("meta-anual").textContent = cfg.meta;
  try {
    if (cfg.esPresupuesto) {
      const [pres, contratos] = await Promise.all([
        fetch(cfg.presupuesto).then(r => r.json()),
        fetch(cfg.contratos).then(r => r.json()),
      ]);
      el.innerHTML = tablaEjecucion(pres) + tablaContratos(contratos, anio);
    } else {
      const [ind, contratos] = await Promise.all([
        fetch(cfg.indicadores).then(r => r.json()),
        fetch(cfg.contratos).then(r => r.json()),
      ]);
      el.innerHTML = render2026(ind);
    }
  } catch (err) {
    el.innerHTML = `<p class="vacio">Error al cargar datos: ${err.message}</p>`;
  }
}

document.getElementById("sel-anio").addEventListener("change", e => cargarAnio(e.target.value));
cargarAnio("2024");