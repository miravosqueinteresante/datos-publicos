# Datos Públicos — Hero del inicio y tabla paginada — Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Mejorar espaciado del hero y paginar la tabla de contratos (10 por página).

**Architecture:** CSS en `index.html` + JS de paginación en `municipalidad.js`, sin librerías.

**Tech Stack:** CSS, JS vanilla.

---

### Task 1: Hero (index.html)

- [ ] Step 1: Editar el CSS inline de `.hero` en `www/index.html`:

```css
.hero { background: linear-gradient(135deg,#0f3b5c 0%,#4f46e5 100%); color:#fff; padding: 6rem 1.5rem 5rem; text-align:center; }
.hero h1 { font-size: 2.4rem; line-height:1.15; margin: 0 auto 1rem; max-width:1000px; letter-spacing:-.02em; }
.hero .lead { font-size:1.2rem; max-width:820px; margin: 0 auto 2.75rem; opacity:.92; }
.hero .ctas { display:flex; gap:1rem; justify-content:center; flex-wrap:wrap; }
.btn { display:inline-block; padding:.8rem 1.6rem; border-radius:10px; font-weight:600; text-decoration:none; transition:transform .08s; }
```

- [ ] Step 2: Commit — `git add www/index.html && git commit -m "feat: hero spacing and visual hierarchy"`

---

### Task 2: Paginación de la tabla (HTML + JS)

**Files:**
- Modify: `www/municipalidad.html`
- Modify: `www/js/municipalidad.js`

- [ ] Step 1: En `www/municipalidad.html`, tras la `<table id="tabla">…</table>`, añadir el contenedor de paginación:

```html
<nav class="paginacion" id="paginacion" aria-label="Paginación"></nav>
```

- [ ] Step 2: En `www/js/municipalidad.js`, añadir estado y render de paginación en `renderTabla`:

```javascript
let PAGINA = 1;
const POR_PAGINA = 10;

function renderTabla() {
  const q = normalizar(document.getElementById("busqueda").value);
  const cat = document.getElementById("filtro-categoria").value;
  const filtradas = CONTRATOS.filter(d =>
    (!cat || d.categoria === cat) &&
    (!q || normalizar(d.objeto + " " + (d.proveedor || "")).includes(q))
  );
  const total = filtradas.length;
  const paginas = Math.max(1, Math.ceil(total / POR_PAGINA));
  if (PAGINA > paginas) PAGINA = paginas;
  const inicio = (PAGINA - 1) * POR_PAGINA;
  const visibles = filtradas.slice(inicio, inicio + POR_PAGINA);
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = visibles.length === 0
    ? "<tr><td colspan='7' class='vacio'>Sin resultados</td></tr>"
    : visibles.map(filaContrato).join("");
  const nav = document.getElementById("paginacion");
  if (total <= POR_PAGINA) { nav.innerHTML = ""; return; }
  const desde = inicio + 1;
  const hasta = Math.min(inicio + POR_PAGINA, total);
  nav.innerHTML = `
    <button id="pag-prev" ${PAGINA === 1 ? "disabled" : ""}>Anterior</button>
    <span class="pag-info">Mostrando ${desde}–${hasta} de ${total}</span>
    <button id="pag-next" ${PAGINA === paginas ? "disabled" : ""}>Siguiente</button>`;
}
```

- [ ] Step 3: En `init()`, enlazar botones de paginación (delegando clic en el contenedor):

```javascript
  document.getElementById("paginacion").addEventListener("click", e => {
    if (e.target.id === "pag-prev" && PAGINA > 1) { PAGINA--; renderTabla(); }
    if (e.target.id === "pag-next") { PAGINA++; renderTabla(); }
  });
```

- [ ] Step 4: Al cambiar año, resetear `PAGINA = 1` (en el listener del selector, antes de renderContratos).

- [ ] Step 5: CSS `.paginacion` (en `style.css`):

```css
.paginacion { display:flex; align-items:center; gap:.75rem; justify-content:center; margin-top:1rem; font-size:.9rem; color:var(--texto-suave); }
.paginacion button { padding:.45rem .9rem; border:1px solid var(--borde); border-radius:8px; background:#fff; cursor:pointer; font:inherit; }
.paginacion button:disabled { opacity:.5; cursor:default; }
.paginacion .pag-info { font-variant-numeric:tabular-nums; }
```

- [ ] Step 6: Commit — `git add www/municipalidad.html www/js/municipalidad.js www/css/style.css && git commit -m "feat: paginate contracts table (10 per page)"`

---

### Task 3: Verificación + push

- [ ] Servir local: tabla muestra 10, controles navegan, filtro+búsqueda aplican dentro de la página, año resetea.
- [ ] `python -B -m unittest discover -s scripts/tests` (OK).
- [ ] Commit docs (spec/plan) + `git push`.

---

## Criterios de éxito

- Hero con aire y jerarquía (visual).
- Tabla paginada a 10, con controles y rango; filtros respetados; año resetea.
- Tests OK; desplegado.