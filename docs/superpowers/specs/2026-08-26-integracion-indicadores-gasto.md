# Datos Públicos — Página "Gasto" en la plataforma (indicadores DNCP)

Fecha: 2026-08-26

## Propósito

Presentar en la plataforma pública los indicadores de gasto derivados de las contrataciones de la Muni, como una nueva página "Gasto" en la navegación. Avanza la FASE 6 (sección "Presupuesto"/"Gasto" del plan) con datos reales.

## Fuente de datos

`www/datos/indicadores-gasto-2026.json` (ya generado por `scripts/indicadores_gasto.py`):
- `procesos`, `monto_total`, `proveedores_distintos`, `procesos_sin_proveedor`.
- `por_categoria` (Bienes/Obras/Servicios, montos).
- `por_tipo_procedimiento` (montos).
- `top_proveedores` (top 10, montos).

**Etiqueta honesta:** los indicadores representan **gasto en contrataciones adjudicadas**, no el presupuesto total de la Muni (la nómina/presupuesto no está publicada en abierto — brecha documentada en `DATA_INVENTORY.md`).

## Diseño

### Estructura
- `www/gasto.html` — nueva página.
- `www/css/style.css` — se añaden clases para barras.
- `www/js/gasto.js` — lógica vanilla (fetch + render).
- Menú actualizado en `www/index.html`, `www/datos.html`, `www/metodologia.html`, `www/gasto.html`: **Explorar · Datos · Gasto · Metodología**.

### Contenido de `gasto.html`
1. Cabecera + nota honesta (contrataciones vs presupuesto).
2. Tarjetas de totales (procesos, monto total, proveedores).
3. Distribución por categoría — barras horizontales CSS (monto + %).
4. Distribución por tipo de procedimiento — barras CSS.
5. Top 10 proveedores — tabla (proveedor, monto, % del total).
6. Nota metodológica corta.

### Barras (CSS puro)
- Contenedor `.barra-fila` con etiqueta, barra `.barra` (ancho %), valor y %.
- Sin librerías ni SVG. Accesible: etiquetas de texto siempre visibles.

## Criterios de éxito
- `www/gasto.html` abre sin errores y muestra los indicadores del JSON real.
- Barras correctas (ancho proporcional a %).
- Menú compartido coherente en las 4 páginas.
- Etiqueta "contrataciones adjudicadas" clara (no "presupuesto").
- Reutiliza el CSS 2026; JS vanilla; sin dependencias nuevas.