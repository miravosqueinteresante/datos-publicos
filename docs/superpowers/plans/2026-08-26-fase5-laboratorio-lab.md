# Datos Públicos — FASE 5: Dashboard del laboratorio (lab/) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Crear `lab/index.html`, la página del laboratorio que muestra el estado real del pipeline de contrataciones de la Muni, reutilizando el JSON y CSS existentes.

**Architecture:** Una sola página estática en `lab/` que con JavaScript vanilla lee `../www/datos/contrataciones-2026.json` (ya generado por el pipeline) y renderiza 4 métricas + una sección de estado del pipeline. Reutiliza `www/css/style.css`. Sin generadores nuevos.

**Tech Stack:** HTML5, JS vanilla, CSS (reutilizado), Python 3.10 (solo para tests de validación del JSON).

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- `www/datos/contrataciones-2026.json` ya existe (36 registros, generado por el pipeline).
- `www/css/style.css` existe (mismo look para coherencia).
- Estado del workflow verificado: última corrida `success` el 2026-08-26.

## Estructura de archivos

- `lab/index.html` — página única (HTML + JS inline).
- Reutiliza `www/css/style.css`.

---

### Task 1: Página del laboratorio (`lab/index.html`)

**Files:**
- Create: `lab/index.html`

- [ ] **Step 1: Crear `lab/index.html`**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Datos Públicos — Lab</title>
  <link rel="stylesheet" href="../www/css/style.css">
</head>
<body>
  <header class="cabecera">
    <h1>Datos Públicos — Lab</h1>
    <p class="subtitulo">Cómo funciona el sistema</p>
    <p class="meta">Estado del pipeline de contrataciones de la Municipalidad de Asunción</p>
  </header>

  <main>
    <section id="metricas" class="seccion"></section>

    <section class="seccion">
      <h2>Estado del pipeline</h2>
      <ul class="sin-estilo">
        <li><strong>Fuente:</strong>
          <a href="https://www.contrataciones.gov.py/datos/open-contracting-info" target="_blank" rel="noopener">
            DNCP — Portal de Datos Abiertos</a> (CC BY 4.0)</li>
        <li><strong>Pipeline:</strong> <code>scripts/dncp_contrataciones.py</code> → CSV → JSON web</li>
        <li><strong>Última actualización del dataset:</strong> 2026-08-26 (commit del CSV en main)</li>
        <li><strong>Última ejecución del workflow (GitHub Actions):</strong> success (26-ago-2026)</li>
        <li><strong>Procesos:</strong> año 2026, 36 procesos de la Municipalidad de Asunción</li>
      </ul>
      <p><a href="../www/index.html">Ver plataforma pública →</a></p>
    </section>
  </main>

  <script>
    const FORMATO = new Intl.NumberFormat("es-PY", { maximumFractionDigits: 0 });

    function cabecera(etiqueta, valor) {
      const v = typeof valor === "number" ? FORMATO.format(valor) : valor;
      return `<div class="metrica"><div class="valor">${v}</div><div class="etiqueta">${etiqueta}</div></div>`;
    }

    fetch("../www/datos/contrataciones-2026.json")
      .then(r => r.json())
      .then(datos => {
        const conMonto = datos.filter(d => !d.monto_nulo);
        const total = conMonto.reduce((s, d) => s + d.monto, 0);
        const proveedores = new Set(datos.filter(d => d.proveedor).map(d => d.proveedor));
        const categorias = new Set(datos.map(d => d.categoria));
        const el = document.getElementById("metricas");
        el.innerHTML = [
          cabecera("Procesos 2026", datos.length),
          cabecera("Monto adjudicado total", total),
          cabecera("Proveedores distintos", proveedores.size),
          cabecera("Categorías", categorias.size),
        ].join("");
      })
      .catch(err => {
        document.getElementById("metricas").innerHTML =
          `<div class="vacio">No se pudo cargar el dataset: ${err.message}</div>`;
      });
  </script>
</body>
</html>
```

- [ ] **Step 2: Verificar que el JSON referenciado existe y responde la ruta**

```bash
python -c "import json; d=json.load(open('www/datos/contrataciones-2026.json',encoding='utf-8')); print('registros:', len(d))"
```
Expected: `registros: 36`.

- [ ] **Step 3: Probar la página en servidor local**

```bash
python -m http.server 8091 --directory .
```
Abrir `http://localhost:8091/lab/index.html`. Expected: renderiza las 4 métricas (36 / monto / 17 proveedores / 3 categorías) sin errores de consola.

- [ ] **Step 4: Commit**

```bash
git add lab/index.html
git commit -m "feat: add lab dashboard page (FASE 5)"
```

---

### Task 2: Verificación final y push

**Files:**
- N/A

- [ ] **Step 1: Verificar que la ruta del CSS es correcta desde lab/**

```bash
Test-Path www/css/style.css; Test-Path lab/index.html
```
Expected: ambos True.

- [ ] **Step 2: Push**

```bash
git add docs/superpowers/specs/2026-08-26-fase5-laboratorio-lab.md docs/superpowers/plans/2026-08-26-fase5-laboratorio-lab.md
git commit -m "docs: add FASE 5 spec and plan (lab dashboard)"
git push
```

---

## Criterios de éxito (verificación final)

- `lab/index.html` abre y muestra las métricas reales del JSON (36 procesos, monto, 17 proveedores, 3 categorías).
- Reutiliza el CSS del www (un único `style.css`).
- No duplica generadores: lee el JSON existente.
- Sin errores de consola.
- Todo versionado y pusheado.