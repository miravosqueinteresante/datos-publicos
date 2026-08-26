# Datos Públicos — FASE 6 mínima: Navegación multi-sección + rediseño 2026 — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convertir `www/` en una web multi-página con navegación y rediseñarla con un sistema visual moderno (claro + acentos vivos), manteniendo la lógica de datos existente y la coherencia con `lab/`.

**Architecture:** Multi-página estática compartiendo un CSS nuevo (`www/css/style.css`) y el JS de tabla existente (`www/js/app.js`). El lab reutiliza el mismo CSS (se beneficia del rediseño). Sin tocar generadores ni datos.

**Tech Stack:** HTML5, CSS (sistema visual nuevo), JS vanilla (existente), Python para verificación.

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- `www/` hoy: `index.html` (página única), `css/style.css` (1.9 KB), `js/app.js`, `datos/contrataciones-2026.json` (36 regs).
- `lab/index.html` usa `../www/css/style.css`.
- La lógica de tabla/filtros funciona (17 tests de scripts; página validada).

---

### Task 1: Nuevo CSS compartido (sistema 2026)

**Files:**
- Modify: `www/css/style.css` (reemplazo completo)

- [ ] **Step 1: Escribir el nuevo estilo**

```css
:root {
  --fondo: #f8fafc;
  --tarjeta: #ffffff;
  --texto: #0f172a;
  --texto-suave: #64748b;
  --primario: #4f46e5;
  --primario-suave: #eef2ff;
  --exito: #10b981;
  --borde: #e2e8f0;
  --sombra: 0 1px 3px rgba(15, 23, 42, .08), 0 4px 12px rgba(15, 23, 42, .05);
  --radio: 12px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Arial, sans-serif;
  background: var(--fondo); color: var(--texto);
  line-height: 1.55;
}
a { color: var(--primario); text-decoration: none; }
a:hover { text-decoration: underline; }

/* Navegación sticky */
.nav {
  position: sticky; top: 0; z-index: 10;
  background: rgba(255,255,255,.92); backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--borde);
}
.nav-inner {
  max-width: 1080px; margin: 0 auto; padding: .75rem 1rem;
  display: flex; align-items: center; gap: 1.25rem; flex-wrap: wrap;
}
.nav .marca { font-weight: 700; color: var(--texto); font-size: 1.05rem; }
.nav ul { list-style: none; display: flex; gap: 1rem; margin: 0; padding: 0; }
.nav ul li a { color: var(--texto-suave); font-weight: 500; padding: .35rem .5rem; border-radius: 8px; }
.nav ul li a:hover { background: var(--primario-suave); color: var(--primario); text-decoration: none; }
.nav ul li a.activo { color: var(--primario); background: var(--primario-suave); }
.nav .vision { margin-left: auto; font-size: .78rem; color: var(--texto-suave); }

/* Portada de página */
.portada {
  max-width: 1080px; margin: 0 auto; padding: 2.5rem 1rem 1rem;
}
.portada h1 { margin: 0 0 .25rem; font-size: 2.1rem; letter-spacing: -.02em; }
.portada .subtitulo { font-size: 1.15rem; color: var(--texto-suave); margin: 0 0 .25rem; }
.portada .meta { font-size: .85rem; color: var(--texto-suave); }

main { max-width: 1080px; margin: 0 auto; padding: 1rem; }
.seccion {
  background: var(--tarjeta); border: 1px solid var(--borde);
  border-radius: var(--radio); padding: 1.25rem; margin-bottom: 1rem;
  box-shadow: var(--sombra);
}
.seccion h2 { margin-top: 0; font-size: 1.25rem; letter-spacing: -.01em; }

/* Métricas */
#metricas, .metricas { display: flex; gap: 1rem; flex-wrap: wrap; }
.metrica {
  flex: 1; min-width: 160px; background: var(--tarjeta);
  border: 1px solid var(--borde); border-radius: var(--radio);
  padding: 1rem 1.1rem; box-shadow: var(--sombra);
}
.metrica .valor {
  font-size: 1.6rem; font-weight: 700; color: var(--primario);
  font-variant-numeric: tabular-nums; letter-spacing: -.02em;
}
.metrica .etiqueta { font-size: .82rem; color: var(--texto-suave); }

/* Filtros */
.filtros { display: flex; gap: .5rem; margin-bottom: .85rem; flex-wrap: wrap; }
.filtros input[type=search], .filtros select {
  padding: .55rem .7rem; border: 1px solid var(--borde); border-radius: 8px;
  font: inherit; background: #fff;
}
.filtros input[type=search]:focus, .filtros select:focus {
  outline: 2px solid var(--primario); outline-offset: 1px; border-color: transparent;
}

/* Tabla */
.tabla-envolvente { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: .92rem; }
th, td { text-align: left; padding: .6rem .6rem; border-bottom: 1px solid var(--borde); }
th { font-size: .8rem; text-transform: uppercase; letter-spacing: .03em; color: var(--texto-suave); font-weight: 600; }
tbody tr:hover { background: #f8fafc; }
td.monto { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.cat-etiqueta {
  display: inline-block; padding: .15rem .55rem; border-radius: 999px;
  background: var(--primario-suave); color: var(--primario); font-size: .78rem; font-weight: 600;
}
.cat-Obras { background: #ecfdf5; color: #047857; }
.cat-Servicios { background: #eff6ff; color: #1d4ed8; }
.cat-Bienes { background: #fef3c7; color: #b45309; }

.vacio { color: var(--texto-suave); font-style: italic; }
.badge-exito {
  display: inline-block; padding: .15rem .6rem; border-radius: 999px;
  background: #ecfdf5; color: #047857; font-size: .8rem; font-weight: 600;
}
.nota { font-size: .87rem; color: var(--texto-suave); }
.nota code, li code { background: #f1f5f9; padding: .1rem .35rem; border-radius: 6px; font-size: .85em; }
ul.sin-estilo { list-style: none; padding-left: 0; }
ul.sin-estilo li { padding: .25rem 0; }

footer { max-width: 1080px; margin: 2rem auto 1rem; padding: 0 1rem; font-size: .8rem; color: var(--texto-suave); }
```

- [ ] **Step 2: Revisar el HTML de lab para compatibilidad**

El lab usa `<header class="cabecera">` — el nuevo CSS renombra la cabecera a `.portada`. Verificar en Task 4; aquí solo se escribe CSS que cubra ambos: añadir las reglas `.cabecera` para compat (alias de `.portada`):

```css
.cabecera {
  max-width: 1080px; margin: 0 auto; padding: 2.5rem 1rem 1rem;
}
.cabecera h1 { margin: 0 0 .25rem; font-size: 2.1rem; letter-spacing: -.02em; }
.cabecera .subtitulo { font-size: 1.15rem; color: var(--texto-suave); margin: 0 0 .25rem; }
.cabecera .meta { font-size: .85rem; color: var(--texto-suave); }
```

- [ ] **Step 3: Commit**

```bash
git add www/css/style.css
git commit -m "feat: redesign site CSS with 2026 system (www + lab shared)"
```

---

### Task 2: `www/index.html` — portada/explorar rediseñada

**Files:**
- Modify: `www/index.html` (reemplazo)

- [ ] **Step 1: Reescribir index.html**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Explorar contrataciones de la Municipalidad de Asunción</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos</span>
    <ul>
      <li><a href="index.html" class="activo">Explorar</a></li>
      <li><a href="datos.html">Datos</a></li>
      <li><a href="metodologia.html">Metodología</a></li>
    </ul>
    <span class="vision">Próximamente: Mapas · Obras · Presupuesto · Indicadores</span>
  </div></nav>

  <header class="portada">
    <h1>Contrataciones de la Municipalidad de Asunción</h1>
    <p class="subtitulo">¿Qué está haciendo la Municipalidad, cuánto y con quién?</p>
    <p class="meta">Datos de contratación pública — año 2026 · Fuente: DNCP (CC BY 4.0)</p>
  </header>

  <main>
    <section id="metricas" class="seccion"></section>

    <section class="seccion">
      <h2>Principales proveedores</h2>
      <ol id="lista-proveedores"></ol>
    </section>

    <section class="seccion">
      <h2>Procesos</h2>
      <div class="filtros">
        <input type="search" id="busqueda" placeholder="Buscar por objeto o proveedor...">
        <select id="filtro-categoria">
          <option value="">Todas las categorías</option>
          <option value="Bienes">Bienes</option>
          <option value="Servicios">Servicios</option>
          <option value="Obras">Obras</option>
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
  </main>

  <footer>Datos Públicos — plataforma de infraestructura cívica · Repo en GitHub</footer>
  <script src="js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add www/index.html
git commit -m "feat: redesign explorer page with navigation (www)"
```

---

### Task 3: `www/app.js` — ajustes visuales (etiquetas de categoría)

**Files:**
- Modify: `www/js/app.js`

- [ ] **Step 1: Rendear categoría con etiqueta visual**

En `filaTabla`, reemplazar la celda de categoría:

```javascript
const catClass = "cat-" + d.categoria.replace(/\s+/g, "");
const categoria = d.categoria
  ? `<span class="cat-etiqueta ${catClass}">${d.categoria}</span>`
  : "—";
```

Y en la plantilla de fila, usar `categoria` en lugar de `d.categoria`.

- [ ] **Step 2: Verificar sin romper la búsqueda**

La búsqueda y filtro siguen usando `d.categoria` (valor crudo en español) — no se toca. Ejecutar verificación con node:

```bash
node -e "const D=require('./www/datos/contrataciones-2026.json'); const cats=[...new Set(D.map(d=>d.categoria))]; console.log(cats);"
```
Expected: `[ 'Obras', 'Bienes', 'Servicios' ]`.

- [ ] **Step 3: Commit**

```bash
git add www/js/app.js
git commit -m "feat: add category badges in table (www)"
```

---

### Task 4: `www/datos.html` — sección Datos

**Files:**
- Create: `www/datos.html`

- [ ] **Step 1: Crear la página**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Datos</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos</span>
    <ul>
      <li><a href="index.html">Explorar</a></li>
      <li><a href="datos.html" class="activo">Datos</a></li>
      <li><a href="metodologia.html">Metodología</a></li>
    </ul>
    <span class="vision">Próximamente: Mapas · Obras · Presupuesto · Indicadores</span>
  </div></nav>

  <header class="portada">
    <h1>Datos</h1>
    <p class="subtitulo">Conjuntos de datos estructurados del proyecto</p>
  </header>

  <main>
    <section class="seccion">
      <h2>Contrataciones de la Municipalidad de Asunción — 2026</h2>
      <p>Procesos de contratación pública de la Municipalidad de Asunción, obtenidos de la DNCP.
      <span class="badge-exito">disponible</span></p>
      <p><strong>Formato:</strong> CSV · <strong>Registros:</strong> 34 (a actualizar) · <strong>Licencia:</strong> CC BY 4.0</p>
      <p><strong>Descargar:</strong>
        <a href="https://github.com/miravosqueinteresante/datos-publicos/raw/main/data/contrataciones_muni_2026.csv">contrataciones_muni_2026.csv</a> ·
        <a href="datos/contrataciones-2026.json">contrataciones-2026.json</a></p>
      <p class="nota">Pipeline: <code>scripts/dncp_contrataciones.py</code> → <code>scripts/generar_datos_web.py</code>.
      Se actualiza mensualmente (GitHub Actions).</p>
    </section>

    <section class="seccion">
      <h2>Próximos datasets</h2>
      <ul class="sin-estilo">
        <li>Mapas (servicios ArcGIS de la Muni) — pendiente de pipeline</li>
        <li>Obras públicas — pendiente de pipeline</li>
        <li>Presupuesto / finanzas — pendiente de pipeline</li>
        <li>Indicadores derivados — a definir</li>
      </ul>
      <p class="nota">Catálogo completo de fuentes: <code>DATA_INVENTORY.md</code> en el repo.</p>
    </section>
  </main>
  <footer>Datos Públicos — plataforma de infraestructura cívica</footer>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add www/datos.html
git commit -m "feat: add Datos page with dataset catalog (www)"
```

---

### Task 5: `www/metodologia.html` — sección Metodología

**Files:**
- Create: `www/metodologia.html`

- [ ] **Step 1: Crear la página**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Metodología</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos</span>
    <ul>
      <li><a href="index.html">Explorar</a></li>
      <li><a href="datos.html">Datos</a></li>
      <li><a href="metodologia.html" class="activo">Metodología</a></li>
    </ul>
    <span class="vision">Próximamente: Mapas · Obras · Presupuesto · Indicadores</span>
  </div></nav>

  <header class="portada">
    <h1>Metodología</h1>
    <p class="subtitulo">De dónde salen los datos, cómo se procesan y qué limitaciones tienen</p>
  </header>

  <main>
    <section class="seccion">
      <h2>Fuente</h2>
      <p>Datos de la <strong>Dirección Nacional de Contrataciones Públicas (DNCP)</strong> de Paraguay,
      obtenidos desde su Portal de Datos Abiertos
      (<a href="https://www.contrataciones.gov.py/datos/" target="_blank" rel="noopener">contrataciones.gov.py/datos</a>),
      licencia <strong>CC BY 4.0</strong>.</p>
      <p>La Municipalidad de Asunción es la convocante SICP <code>108</code>.
      Verificación oficial:
      <a href="https://www.contrataciones.gov.py/convocantes/municipalidad-asuncion/licitaciones/2026.html" target="_blank" rel="noopener">
      perfil de licitaciones de la Muni en la DNCP</a>.</p>
    </section>

    <section class="seccion">
      <h2>Proceso</h2>
      <ol>
        <li><code>scripts/dncp_contrataciones.py</code> — descarga el ZIP anual de la DNCP, une tablas OCDS por OCID, filtra por la Muni, valida y produce el CSV.</li>
        <li><code>scripts/generar_datos_web.py</code> — convierte el CSV a JSON para la web.</li>
        <li>GitHub Actions ejecuta el flujo mensualmente y commitea cambios.</li>
      </ol>
      <p class="nota">Los procesos sin proveedor son llamados sin adjudicación registrada en el conjunto del año.</p>
    </section>

    <section class="seccion">
      <h2>Trazabilidad y limitaciones</h2>
      <ul class="sin-estilo">
        <li><strong>Fecha de obtención:</strong> 26-ago-2026 (actualizable mensualmente).</li>
        <li><strong>Alcance:</strong> solo la Municipalidad de Asunción como comprador (SICP 108); procesos donde es cofinanciante quedan fuera.</li>
        <li><strong>Formato original:</strong> OCDS aplanado (estándar Open Contracting).</li>
        <li><strong>Limitación:</strong> el campo de comprador puede venir vacío en algunas adjudicaciones; se usa <code>records</code> (1 fila por proceso) como base.</li>
      </ul>
    </section>
  </main>
  <footer>Datos Públicos — plataforma de infraestructura cívica</footer>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add www/metodologia.html
git commit -m "feat: add Metodologia page (www)"
```

---

### Task 6: Coherencia con lab + verificación + push

**Files:**
- Maybe: `lab/index.html` (si necesaria)

- [ ] **Step 1: Verificar lab con el CSS nuevo**

Abrir `http://localhost:8000/lab/index.html` (servidor desde raíz del repo). Expected: se ve coherente (el alias `.cabecera` funciona). Si `.cabecera` no se ve bien con el nuevo CSS, ajustar mínimamente.

- [ ] **Step 2: Verificar las 3 páginas del www**

Servidor local + fetch de las 4 URLs (index, datos, metodología, CSS, JSON). Expected: todas 200.

- [ ] **Step 3: Verificar tests de scripts**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 17 tests OK (no se tocó el pipeline).

- [ ] **Step 4: Push**

```bash
git push
```

---

## Criterios de éxito (verificación final)

- 3 páginas del www con navegación compartida, abren sin errores.
- Rediseño aplicado (CSS nuevo), tabla con etiquetas de categoría coloreadas.
- Lógica de búsqueda/filtros intacta.
- Lab coherente con el nuevo diseño.
- Sin páginas vacías: solo 3 + visión en el menú.
- 17 tests pasan; generadores sin cambios.
- Todo pusheado.