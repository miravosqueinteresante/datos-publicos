# Datos Públicos — FASE 4: Primer producto útil (página en www/) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear la primera funcionalidad pública: una página estática en `www/` que responde "¿Qué está haciendo la Municipalidad de Asunción, cuánto y con quién?" con los datos de contratación 2026.

**Architecture:** Un generador Python (CSV→JSON, con test TDD) produce `www/datos/contrataciones-2026.json`. La página es HTML+CSS+JS vanilla de un solo archivo que consume ese JSON (fetch local) y renderiza métricas, tabla filtrable y top proveedores. Sin frameworks, sin build step, lista para GitHub Pages.

**Tech Stack:** Python 3.10 (stdlib), HTML5, CSS, JavaScript vanilla, `unittest`.

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- Dataset existente: `data/contrataciones_muni_2026.csv` (36 filas, columnas de FASE 3).
- `www/` existe vacía (creada en FASE 0). La página no toca el repo de muchotexto.net.

## Estructura de archivos

- `scripts/generar_datos_web.py` — CSV→JSON.
- `scripts/tests/test_generar_web.py` — tests del generador.
- `www/datos/contrataciones-2026.json` — datos web (generado, versionado).
- `www/index.html`, `www/css/style.css`, `www/js/app.js` — página.

---

### Task 1: Generador CSV→JSON (TDD)

**Files:**
- Create: `scripts/generar_datos_web.py`
- Create: `scripts/tests/test_generar_web.py`

- [ ] **Step 1: Escribir el test que falla**

```python
import unittest, json, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_datos_web import fila_a_json, generar

CSV_EJEMPLO = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
ocds-a-1,Compra de insumos,complete,goods,open,Municipalidad de Asunción,PEPE S.A.,150000000,PYG,2026-01-01T00:00:00,2026-01-10T00:00:00,2026-01-20T00:00:00,https://x/1
ocds-a-2,Construcción,active,works,open,Municipalidad de Asunción,,0,PYG,2026-02-01T00:00:00,,,,https://x/2
"""

class TestGenerarWeb(unittest.TestCase):
    def test_fila_a_json_montos_numericos(self):
        fila = {"id": "ocds-1", "objeto": "X", "monto": "150000000", "fecha_publicacion": "2026-01-01T00:00:00"}
        out = fila_a_json(fila)
        self.assertEqual(out["monto"], 150000000)
        self.assertEqual(out["monto_nulo"], False)
    def test_fila_a_json_monto_vacio(self):
        out = fila_a_json({"id": "ocds-2", "objeto": "Y", "monto": "", "fecha_publicacion": ""})
        self.assertEqual(out["monto"], 0)
        self.assertEqual(out["monto_nulo"], True)
    def test_generar_lee_diccionarios(self):
        filas = generar(CSV_EJEMPLO)
        self.assertEqual(len(filas), 2)
        self.assertEqual(filas[0]["proveedor"], "PEPE S.A.")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar el test, debe fallar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: FAIL con `ModuleNotFoundError: No module named 'generar_datos_web'`.

- [ ] **Step 3: Implementar el generador**

```python
import csv
import json
import os

RUTA_ORIGEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "contrataciones_muni_2026.csv")
RUTA_DESTINO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "www", "datos", "contrataciones-2026.json")


def fila_a_json(fila):
    monto = fila.get("monto") or ""
    es_nulo = not monto
    try:
        monto_num = float(monto)
    except ValueError:
        monto_num = 0
        es_nulo = True
    return {
        "id": fila.get("id", ""),
        "objeto": fila.get("objeto", ""),
        "estado": fila.get("estado", ""),
        "categoria": fila.get("categoria", ""),
        "tipo_procedimiento": fila.get("tipo_procedimiento", ""),
        "comprador": fila.get("comprador", ""),
        "proveedor": fila.get("proveedor", ""),
        "monto": monto_num,
        "monto_nulo": es_nulo,
        "moneda": fila.get("moneda", ""),
        "fecha_publicacion": fila.get("fecha_publicacion", ""),
        "fecha_adjudicacion": fila.get("fecha_adjudicacion", ""),
        "fecha_contrato": fila.get("fecha_contrato", ""),
        "url_muni": fila.get("url_muni", ""),
    }


def generar(csv_texto):
    reader = csv.DictReader(csv_texto.splitlines())
    return [fila_a_json(f) for f in reader]


def main():
    with open(RUTA_ORIGEN, encoding="utf-8") as f:
        datos = generar(f.read())
    os.makedirs(os.path.dirname(RUTA_DESTINO), exist_ok=True)
    with open(RUTA_DESTINO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Generados {len(datos)} registros en {RUTA_DESTINO}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Ejecutar los tests, deben pasar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 13 tests PASS (10 previos + 3 nuevos).

- [ ] **Step 5: Commit**

```bash
git add scripts/generar_datos_web.py scripts/tests/test_generar_web.py
git commit -m "feat: add CSV to JSON web data generator (TDD)"
```

---

### Task 2: Generar el JSON web a partir del dataset real

**Files:**
- Create: `www/datos/contrataciones-2026.json` (generado)

- [ ] **Step 1: Ejecutar el generador**

```bash
python scripts/generar_datos_web.py
```
Expected: "Generados 36 registros en .../www/datos/contrataciones-2026.json".

- [ ] **Step 2: Verificar el JSON**

```bash
python -c "import json; d=json.load(open('www/datos/contrataciones-2026.json',encoding='utf-8')); print(len(d), d[0]['monto'], type(d[0]['monto']).__name__)"
```
Expected: `36 550000000 int` (36 filas, monto numérico, primera fila).

- [ ] **Step 3: Commit**

```bash
git add www/datos/contrataciones-2026.json
git commit -m "data: generate web dataset JSON from Asuncion contracts 2026"
```

---

### Task 3: Página HTML (www/index.html)

**Files:**
- Create: `www/index.html`

- [ ] **Step 1: Crear index.html**

Contenido completo (HTML5, enlaza CSS y JS, tiene contenedores para las secciones):

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Contrataciones de la Municipalidad de Asunción</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <header class="cabecera">
    <h1>Datos Públicos</h1>
    <p class="subtitulo">¿Qué está haciendo la Municipalidad de Asunción, cuánto y con quién?</p>
    <p class="meta">Datos de contratación pública — año 2026 · Fuente: DNCP (CC BY 4.0)</p>
  </header>

  <main>
    <section id="metricas" class="seccion"></section>
    <section id="top-proveedores" class="seccion">
      <h2>Principales proveedores</h2>
      <ol id="lista-proveedores"></ol>
    </section>
    <section class="seccion">
      <h2>Procesos</h2>
      <div class="filtros">
        <input type="search" id="busqueda" placeholder="Buscar por objeto o proveedor...">
        <select id="filtro-categoria">
          <option value="">Todas las categorías</option>
          <option value="goods">Bienes (goods)</option>
          <option value="services">Servicios (services)</option>
          <option value="works">Obras (works)</option>
        </select>
      </div>
      <div class="tabla-envolvente">
        <table id="tabla">
          <thead>
            <tr>
              <th>Objeto</th><th>Categoría</th><th>Proveedor</th>
              <th>Monto (PYG)</th><th>Adjudicación</th><th>Contrato</th><th>Enlace</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </section>
    <section class="seccion nota">
      <h2>Metodología</h2>
      <p>Dataset: 36 procesos de la Municipalidad de Asunción, año 2026, obtenidos del portal de datos
      abiertos de la DNCP (CC BY 4.0) el 26-ago-2026. Pipeline: <code>scripts/dncp_contrataciones.py</code>.
      Los procesos sin proveedor son llamados sin adjudicación registrada en el conjunto del año.</p>
      <p>Repo: <a href="https://github.com/miravosqueinteresante/datos-publicos">github.com/miravosqueinteresante/datos-publicos</a></p>
    </section>
  </main>
  <script src="js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add www/index.html
git commit -m "feat: add first public page structure (www)"
```

---

### Task 4: Estilos (www/css/style.css)

**Files:**
- Create: `www/css/style.css`

- [ ] **Step 1: Crear style.css**

```css
:root {
  --color-primario: #0f3b5c;
  --color-fondo: #f4f6f8;
  --color-texto: #1c2733;
  --color-acento: #7fb069;
  --borde: #d4dde5;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
  margin: 0; background: var(--color-fondo); color: var(--color-texto);
}
.cabecera {
  background: var(--color-primario); color: #fff; padding: 2rem 1rem;
}
.cabecera h1 { margin: 0 0 .25rem; font-size: 1.6rem; }
.subtitulo { font-size: 1.15rem; margin: 0 0 .5rem; opacity: .95; }
.meta { font-size: .85rem; opacity: .75; margin: 0; }
main { max-width: 960px; margin: 0 auto; padding: 1rem; }
.seccion { background: #fff; border: 1px solid var(--borde); border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
.seccion h2 { margin-top: 0; color: var(--color-primario); font-size: 1.2rem; }
#metricas { display: flex; gap: 1rem; flex-wrap: wrap; }
.metrica { flex: 1; min-width: 150px; background: #edf3f7; border-radius: 6px; padding: .75rem; }
.metrica .valor { font-size: 1.4rem; font-weight: 700; color: var(--color-primario); }
.metrica .etiqueta { font-size: .8rem; color: #51616f; }
.filtros { display: flex; gap: .5rem; margin-bottom: .75rem; flex-wrap: wrap; }
.filtros input[type=search] { flex: 1; min-width: 200px; padding: .5rem; border: 1px solid var(--borde); border-radius: 4px; }
.filtros select { padding: .5rem; border: 1px solid var(--borde); border-radius: 4px; }
.tabla-envolvente { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .9rem; }
th, td { text-align: left; padding: .5rem; border-bottom: 1px solid var(--borde); }
th { background: #eef3f7; }
tr:hover { background: #f7fafc; }
td.monto { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.nota { font-size: .85rem; color: #51616f; }
a { color: var(--color-primario); }
.vacio { color: #8a97a3; font-style: italic; }
```

- [ ] **Step 2: Commit**

```bash
git add www/css/style.css
git commit -m "feat: add page styles (www/css)"
```

---

### Task 5: Lógica JS (www/js/app.js)

**Files:**
- Create: `www/js/app.js`

- [ ] **Step 1: Crear app.js**

```javascript
const FORMATO_GUARANI = new Intl.NumberFormat("es-PY", {
  maximumFractionDigits: 0,
});

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
  const q = (document.getElementById("busqueda").value || "").toLowerCase();
  const cat = document.getElementById("filtro-categoria").value;
  const filas = DATOS.filter(d =>
    (!cat || d.categoria === cat) &&
    (!q || (d.objeto + " " + (d.proveedor || "")).toLowerCase().includes(q))
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
  return `<tr>
    <td>${d.objeto}</td>
    <td>${d.categoria || "—"}</td>
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
```

- [ ] **Step 2: Prueba manual en navegador**

Abrir `www/index.html` en un navegador (doble clic o servidor local). Verificar sin consola de errores:
- 4 métricas renderizadas.
- Tabla con 36 filas.
- Filtro de categoría y búsqueda funcionan.
- Top proveedores con ranking.

> Nota: si se abre por `file://`, algunos navegadores bloquean `fetch` de JSON local por CORS. Si ocurre, servir con un servidor local simple:
> ```bash
> python -m http.server 8000 --directory www
> ```
> y abrir `http://localhost:8000`.

- [ ] **Step 3: Commit**

```bash
git add www/js/app.js
git commit -m "feat: add page logic and interactivity (www/js)"
```

---

### Task 6: Verificación final y push

**Files:**
- N/A

- [ ] **Step 1: Verificar pruebas**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 13 tests PASS.

- [ ] **Step 2: Verificar JSON de datos**

```bash
python -c "import json; d=json.load(open('www/datos/contrataciones-2026.json',encoding='utf-8')); print(len(d), 'registros;', sum(1 for r in d if r['proveedor']), 'con proveedor')"
```
Expected: `36 registros; 17 con proveedor`.

- [ ] **Step 3: Push**

```bash
git push
```

---

## Criterios de éxito (verificación final)

- 13 tests pasan.
- JSON web con 36 registros, montos numéricos, generado por script reproducible.
- Página en `www/` abre sin errores y muestra métricas + tabla filtrable + top proveedores.
- Sin frameworks, sin build step, sin dependencias de red (solo el JSON local).
- Todo versionado y pusheado.