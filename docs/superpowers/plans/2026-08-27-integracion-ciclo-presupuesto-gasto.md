# Datos Públicos — Integrar ciclo presupuesto 2024 en Gasto — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Publicar el ciclo 2024 en la página Gasto con selector de año fiscal (2024/2026), ejecución por objeto del gasto y contrataciones 2024, reforzando metodología y glosario.

**Architecture:** Extender `scripts/generar_datos_web.py` para producir JSON por año (parametrizado), extender `www/js/gasto.js` con selector + render por año, y ajustar `www/gasto.html` + `www/metodologia.html`. TDD para el generador.

**Tech Stack:** Python 3.10 (stdlib), JS vanilla, HTML/CSS (estilo 2026 existente).

---

## Contexto
- Repo `datos-publicos`. Datos disponibles: `presupuesto_ejecucion_2024.csv`, `contrataciones_muni_2024.csv` (2026 ya en web).
- `scripts/generar_datos_web.py` genera hoy solo el JSON 2026 (funciones fijas a contrincaciones 2026). 
- `www/js/gasto.js` lee `datos/indicadores-gasto-2026.json` y renderiza métricas/barras/top proveedores.

---

### Task 1: Extender generador a multi-año (TDD)

**Files:**
- Modify: `scripts/generar_datos_web.py`
- Modify: `scripts/tests/test_generar_web.py`

- [ ] **Step 1: Test que falla — generación por año para ejecución presupuestaria**

```python
from generar_datos_web import presupuesto_filas_a_json

class TestPresupuestoJson(unittest.TestCase):
    def test_presupuesto_filas_a_json(self):
        filas_csv = [
            ["2024", "100", "Servicios Personales", "788089.0", "727234.0", "92.28", "Rendición de Cuentas 2024", "url"],
            ["2024", "TOTAL", "TOTAL GENERAL", "2360168.0", "1165830.0", "49.4", "Rendición de Cuentas 2024", "url"],
        ]
        out = presupuesto_filas_a_json(filas_csv)
        self.assertEqual(out[0]["nivel"], "100")
        self.assertEqual(out[0]["presupuesto_vigente"], 788089.0)
        self.assertEqual(out[0]["porcentaje_ejecucion"], 92.28)
        self.assertEqual(out[1]["nivel"], "TOTAL")
```

- [ ] **Step 2: Implementar `presupuesto_filas_a_json`**

```python
def presupuesto_filas_a_json(filas):
    # filas esperadas en el orden del CSV: ejercicio,nivel,denominacion,vigente,obligado,pct,fuente,url
    return [
        {
            "ejercicio": f[0], "nivel": f[1], "denominacion": f[2],
            "presupuesto_vigente": float(f[3]) if f[3] else None,
            "obligado": float(f[4]) if f[4] else None,
            "porcentaje_ejecucion": float(f[5]) if f[5] else None,
            "fuente": f[6], "url": f[7],
        }
        for f in filas
    ]
```

- [ ] **Step 3: Test del generador real (main multi-año)** — `main()` debe generar, para cada año dado, los JSON de contrataciones y (si existe CSV de presupuesto) el de presupuesto. Añadir test unitario de la ruta de salida si es posible, o verificar por ejecución.

- [ ] **Step 4: Commit** — `git add scripts/... test... && git commit -m "feat: parametrize web data generator by year (TDD)"`

- [ ] **Step 5: Generar los JSON 2024** — `python scripts/generar_datos_web.py` → verificar `www/datos/contrataciones-2024.json` y `www/datos/presupuesto-ejecucion-2024.json` creados con datos reales.

---

### Task 2: Selector de año en `www/gasto.html`

**Files:**
- Modify: `www/gasto.html`

- [ ] **Step 1: Añadir selector de año** tras la cabecera:

```html
<section class="seccion">
  <label for="sel-anio">Ejercicio fiscal:</label>
  <select id="sel-anio">
    <option value="2024">2024</option>
    <option value="2026">2026</option>
  </select>
</section>
```

- [ ] **Step 2: Envolver/reorganizar los contenedores** para que el JS renderice según año:

```html
<section id="totales-gasto" class="seccion"></section>
<section id="contenido-anual" class="seccion"></section>
```

(Sustituir los contenedores fijos actuales `#metricas`/`#barras-categoria`/`#top-proveedores` por los dos contenedores dinámicos de arriba.)

- [ ] **Step 3: Commit**

---

### Task 3: Lógica por año en `www/js/gasto.js`

**Files:**
- Modify: `www/js/gasto.js`

- [ ] **Step 1: Reestructurar el JS**

- Datos por año (cargar según selección):
  - 2024: `presupuesto-ejecucion-2024.json` + `contrataciones-2024.json`
  - 2026: `indicadores-gasto-2026.json` + `contrataciones-2026.json`
- Función `render2024(presupuesto, contratos)`:
  - Tabla de ejecución por objeto del gasto (vigente/obligado/%).
  - Tabla de contrataciones 2024 (objeto/categoría/proveedor/monto).
- Función `render2026(indicadores, contratos)`: (los indicadores actuales).
- Listener del `<select>` → renderiza el año elegido (2024 por defecto).
- Manejo de error por fetch.

- [ ] **Step 2: Commit**

---

### Task 4: Metodología + glosario

**Files:**
- Modify: `www/metodologia.html`
- Modify: `www/gasto.html` (sección glosario)

- [ ] **Step 1: Ampliar Metodología** con limitaciones del ciclo 2024 (obligado de Transferencias parcial; sin pagos por partida; ejecución agregada anual; Hesakã no extraíble → personal = partida 100).

- [ ] **Step 2: Añadir glosario corto** en `gasto.html`: presupuesto vigente / obligado / comprometido / % ejecución.

- [ ] **Step 3: Commit**

---

### Task 5: Verificación + push

- [ ] Step 1: Servir local y verificar `gasto.html` con 2024 y 2026 (fetch de los 4 JSON + render).
- [ ] Step 2: `python -m unittest discover -s scripts/tests` (todos OK, incluido test nuevo).
- [ ] Step 3: Commit docs + `git push` (el deploy reconstruye `_site/`).

---

## Criterios de éxito
- Selector de año funcional en Gasto.
- 2024: ejecución por objeto + contrataciones 2024. 2026: indicadores actuales.
- JSONs 2024 generados por script.
- Metodología ampliada; glosario presente.
- Tests pasan; desplegado en producción.