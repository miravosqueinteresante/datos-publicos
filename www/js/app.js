const FORMATO_GUARANI = new Intl.NumberFormat("es-PY", {
  maximumFractionDigits: 0,
});

function normalizar(texto) {
  return (texto || "").toLowerCase()
    .replace(/[áàäâ]/g, "a").replace(/[éèëê]/g, "e")
    .replace(/[íìïî]/g, "i").replace(/[óòöô]/g, "o")
    .replace(/[úùüû]/g, "u").replace(/ñ/g, "n");
}

let DATOS = [];

async function cargarDatos() {
  const res = await fetch("datos/contrataciones-2026.json");
  DATOS = await res.json();
  renderMetricas();
  renderProveedores();
  renderTabla();
}

function renderMetricas() {
  const conMonto = DATOS.filter(d => !d.monto_nulo);
  const total = conMonto.reduce((s, d) => s + d.monto, 0);
  const proveedores = new Set(DATOS.filter(d => d.proveedor).map(d => d.proveedor));
  const categorias = new Set(DATOS.map(d => d.categoria));
  const el = document.getElementById("metricas");
  el.innerHTML = [
    n(DATOS.length, "Procesos"),
    n(total, "Monto adjudicado total"),
    n(proveedores.size, "Proveedores distintos"),
    n(categorias.size, "Categorías"),
  ].join("");
}

function n(valor, etiqueta) {
  return `<div class="metrica"><div class="valor">${typeof valor === "number" ? FORMATO_GUARANI.format(valor) : valor}</div><div class="etiqueta">${etiqueta}</div></div>`;
}

function renderProveedores() {
  const porProv = new Map();
  DATOS.filter(d => d.proveedor).forEach(d => {
    const e = porProv.get(d.proveedor) || { monto: 0, n: 0 };
    e.monto += d.monto; e.n += 1;
    porProv.set(d.proveedor, e);
  });
  const top = [...porProv.entries()]
    .sort((a, b) => b[1].monto - a[1].monto)
    .slice(0, 10);
  const el = document.getElementById("lista-proveedores");
  el.innerHTML = top.length === 0
    ? "<li class='vacio'>Sin datos de proveedores</li>"
    : top.map(([nombre, e]) =>
        `<li>${nombre} — ${FORMATO_GUARANI.format(e.monto)} PYG (${e.n} proceso${e.n === 1 ? "" : "s"})</li>`
      ).join("");
}

function renderTabla() {
  const q = normalizar(document.getElementById("busqueda").value);
  const cat = document.getElementById("filtro-categoria").value;
  const filas = DATOS.filter(d =>
    (!cat || d.categoria === cat) &&
    (!q || normalizar(d.objeto + " " + (d.proveedor || "")).includes(q))
  );
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = filas.length === 0
    ? "<tr><td colspan='7' class='vacio'>Sin resultados</td></tr>"
    : filas.map(filaTabla).join("");
}

function filaTabla(d) {
  const monto = d.monto_nulo
    ? "<td class='monto vacio'>—</td>"
    : `<td class='monto'>${FORMATO_GUARANI.format(d.monto)}</td>`;
  const adjudicacion = d.fecha_adjudicacion ? d.fecha_adjudicacion.slice(0, 10) : "—";
  const contrato = d.fecha_contrato ? d.fecha_contrato.slice(0, 10) : "—";
  const proveedor = d.proveedor || "<span class='vacio'>Sin adjudicación</span>";
  const catClass = d.categoria ? "cat-" + d.categoria.replace(/\s+/g, "") : "";
  const categoria = d.categoria
    ? `<span class="cat-etiqueta ${catClass}">${d.categoria}</span>`
    : "—";
  return `<tr>
    <td>${d.objeto}</td>
    <td>${categoria}</td>
    <td>${proveedor}</td>
    ${monto}
    <td>${adjudicacion}</td>
    <td>${contrato}</td>
    <td><a href="${d.url_muni}" target="_blank" rel="noopener">ver</a></td>
  </tr>`;
}

document.getElementById("busqueda").addEventListener("input", renderTabla);
document.getElementById("filtro-categoria").addEventListener("change", renderTabla);

cargarDatos();