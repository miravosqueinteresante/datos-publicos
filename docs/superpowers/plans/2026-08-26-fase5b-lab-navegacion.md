# Datos Públicos — FASE 5b: Navegación del lab — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Dar al laboratorio (`lab/`) navegación multi-sección con 3 secciones reales (Resumen, Pipelines, Datos), reutilizando el CSS compartido del www.

**Architecture:** 3 páginas estáticas en `lab/` con el mismo menú sticky y CSS del www. Sin lógica nueva de datos; solo estructura y contenido técnico real.

**Tech Stack:** HTML5, CSS compartido (`../www/css/style.css`), JS vanilla (reutilizado para métricas en Resumen).

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`.
- `lab/index.html` actual: página única con métricas (fetch de `../www/datos/contrataciones-2026.json`) + estado del pipeline, usa `../www/css/style.css`.
- `www/css/style.css` ya tiene el menú (`.nav`, `.nav-inner`, `.marca`, `.vision`) y las clases `.cabecera`/`.portada`, `.seccion`, `.metrica`, `.badge-exito`.

---

### Task 1: `lab/index.html` — Resumen con menú

**Files:**
- Modify: `lab/index.html`

- [ ] **Step 1: Reescribir con menú + contenido actual**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Lab · Resumen</title>
  <link rel="stylesheet" href="../www/css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos · Lab</span>
    <ul>
      <li><a href="index.html" class="activo">Resumen</a></li>
      <li><a href="pipelines.html">Pipelines</a></li>
      <li><a href="datos.html">Datos</a></li>
    </ul>
  </div></nav>

  <header class="portada">
    <h1>Laboratorio</h1>
    <p class="subtitulo">Cómo funciona el sistema</p>
    <p class="meta">Estado del pipeline de contrataciones de la Municipalidad de Asunción</p>
  </header>

  <main>
    <section id="metricas" class="seccion"></section>

    <section class="seccion">
      <h2>Estado del pipeline</h2>
      <ul class="sin-estilo">
        <li><strong>Fuente:</strong>
          <a href="https://www.contrataciones.gov.py/datos/open-contracting-info" target="_blank" rel="noopener">DNCP — Portal de Datos Abiertos</a> (CC BY 4.0)</li>
        <li><strong>Pipeline:</strong> <code>scripts/dncp_contrataciones.py</code> → CSV → JSON web</li>
        <li><strong>Última actualización del dataset:</strong> 26-ago-2026</li>
        <li><strong>Última ejecución del workflow (GitHub Actions):</strong> success (26-ago-2026)</li>
      </ul>
      <p><a href="../www/index.html">Ver plataforma pública →</a></p>
    </section>
  </main>

  <footer>Datos Públicos · Lab — cómo funciona el sistema</footer>
  <script>
    const FORMATO = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });
    function cabecera(etiqueta, valor) {
      const v = typeof valor === "number" ? FORMATO.format(valor) : valor;
      return `<div class="metrica"><div class="valor">${v}</div><div class="etiqueta">${etiqueta}</div></div>`;
    }
    fetch("../www/datos/contrataciones-2026.json")
      .then(r => r.json())
      .then(d => {
        const conMonto = d.filter(x => !x.monto_nulo);
        const total = conMonto.reduce((s, x) => s + x.monto, 0);
        const prov = new Set(d.filter(x => x.proveedor).map(x => x.proveedor));
        const cat = new Set(d.map(x => x.categoria));
        document.getElementById("metricas").innerHTML = [
          cabecera("Procesos 2026", d.length),
          cabecera("Monto adjudicado total", total),
          cabecera("Proveedores distintos", prov.size),
          cabecera("Categorías", cat.size),
        ].join("");
      })
      .catch(e => { document.getElementById("metricas").innerHTML = `<div class="vacio">Error: ${e.message}</div>`; });
  </script>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add lab/index.html
git commit -m "feat: add lab Resumen page with nav (FASE 5b)"
```

---

### Task 2: `lab/pipelines.html`

**Files:**
- Create: `lab/pipelines.html`

- [ ] **Step 1: Crear la página**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Lab · Pipelines</title>
  <link rel="stylesheet" href="../www/css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos · Lab</span>
    <ul>
      <li><a href="index.html">Resumen</a></li>
      <li><a href="pipelines.html" class="activo">Pipelines</a></li>
      <li><a href="datos.html">Datos</a></li>
    </ul>
  </div></nav>

  <header class="portada">
    <h1>Pipelines</h1>
    <p class="subtitulo">Procesos de datos del sistema</p>
  </header>

  <main>
    <section class="seccion">
      <h2>P1 — Contrataciones de la Municipalidad de Asunción (DNCP)</h2>
      <p>Extrae los procesos de contratación de la Muni desde la DNCP y produce el dataset.</p>
      <table>
        <thead><tr><th>Atributo</th><th>Valor</th></tr></thead>
        <tbody>
          <tr><td>Fuente</td><td>DNCP — CSV masivos OCDS</td></tr>
          <tr><td>Identificación</td><td>Convocante SICP <code>108</code> (Municipalidad de Asunción)</td></tr>
          <tr><td>Script</td><td><code>scripts/dncp_contrataciones.py</code></td></tr>
          <tr><td>Generador web</td><td><code>scripts/generar_datos_web.py</code></td></tr>
          <tr><td>Automatización</td><td>GitHub Actions: <code>actualizar-datos</code> (mensual + manual)</td></tr>
          <tr><td>Verificación</td><td>Consistencia nombre ↔ SICP 108 (OK en última corrida)</td></tr>
          <tr><td>Tests</td><td>17 (stdlib unittest)</td></tr>
          <tr><td>Estado</td><td><span class="badge-exito">funcionando</span></td></tr>
        </tbody>
      </table>
    </section>
  </main>
  <footer>Datos Públicos · Lab — cómo funciona el sistema</footer>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add lab/pipelines.html
git commit -m "feat: add lab Pipelines page (FASE 5b)"
```

---

### Task 3: `lab/datos.html`

**Files:**
- Create: `lab/datos.html`

- [ ] **Step 1: Crear la página**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Lab · Datos</title>
  <link rel="stylesheet" href="../www/css/style.css">
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <span class="marca">Datos Públicos · Lab</span>
    <ul>
      <li><a href="index.html">Resumen</a></li>
      <li><a href="pipelines.html">Pipelines</a></li>
      <li><a href="datos.html" class="activo">Datos</a></li>
    </ul>
  </div></nav>

  <header class="portada">
    <h1>Datos</h1>
    <p class="subtitulo">Datasets del proyecto y su estado</p>
  </header>

  <main>
    <section class="seccion">
      <h2>contrataciones_muni_2026</h2>
      <p>Procesos de contratación de la Municipalidad de Asunción, 2026 (DNCP).</p>
      <table>
        <thead><tr><th>Atributo</th><th>Valor</th></tr></thead>
        <tbody>
          <tr><td>Ruta</td><td><code>data/contrataciones_muni_2026.csv</code></td></tr>
          <tr><td>Web JSON</td><td><code>www/datos/contrataciones-2026.json</code></td></tr>
          <tr><td>Formato</td><td>CSV plano · JSON</td></tr>
          <tr><td>Licencia</td><td>CC BY 4.0</td></tr>
          <tr><td>Actualización</td><td>Mensual (GitHub Actions)</td></tr>
          <tr><td>Registros</td><td>36 (última corrida)</td></tr>
          <tr><td>Estado</td><td><span class="badge-exito">disponible</span></td></tr>
        </tbody>
      </table>
      <p class="nota">Catálogo completo de fuentes: <code>DATA_INVENTORY.md</code> en el repo.</p>
    </section>
  </main>
  <footer>Datos Públicos · Lab — cómo funciona el sistema</footer>
</body>
</html>
```

- [ ] **Step 2: Commit**

```bash
git add lab/datos.html
git commit -m "feat: add lab Datos page (FASE 5b)"
```

---

### Task 4: Verificación + push

**Files:**
- N/A

- [ ] **Step 1: Verificar las 3 páginas + CSS**

```powershell
python -m http.server 8093 --directory .
```
Fetch de `lab/index.html`, `lab/pipelines.html`, `lab/datos.html`, `www/css/style.css`, `www/datos/contrataciones-2026.json`. Expected: todas 200.

- [ ] **Step 2: Commit docs + push**

```bash
git add docs/superpowers/specs/2026-08-26-fase5b-lab-navegacion.md docs/superpowers/plans/2026-08-26-fase5b-lab-navegacion.md
git commit -m "docs: add FASE 5b spec and plan (lab navigation)"
git push
```

---

## Criterios de éxito (verificación final)

- 3 páginas del lab con menú compartido, abren sin errores.
- Reutilizan el CSS del www (sin estilos nuevos).
- Contenido real en cada sección.
- Tests de scripts siguen OK (17).
- Todo versionado y pusheado.