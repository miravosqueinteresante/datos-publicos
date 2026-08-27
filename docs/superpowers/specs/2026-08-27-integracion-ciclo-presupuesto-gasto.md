# Datos Públicos — Integrar ciclo presupuestario 2024 en la sección "Gasto" (selector de año)

Fecha: 2026-08-27

## Propósito

Publicar el ciclo presupuestario 2024 (ejecución del gasto + contrataciones) dentro de la sección **"Gasto"** de la plataforma, siguiendo los patrones de portales de transparencia fiscal verificados (OpenSpending, GIFT, Civio — investigación en `research_transparencia_fiscal/findings_referentes.md`). **No** se crea una página "Presupuesto" separada.

## Decisión de diseño (confirmada)

1. **Presupuesto = estado inicial de la ejecución**, no página propia. El menú permanece: Explorar · Datos · **Gasto** · Metodología.
2. **Selector de año fiscal** en la página Gasto (patrón OpenSpending): **2024** y **2026**. Cada año muestra su ejecución de gasto y contrataciones.
3. **Contenido por año:**
   - **2024:** ejecución por objeto del gasto (vigente/obligado/%) + contrataciones 2024 (28 procesos, enlace a proveedor).
   - **2026:** indicadores de gasto por categoría (lo existente hoy).
4. **Metacapas:** reforzar Metodología con limitaciones; añadir **glosario corto** ("¿qué significa presupuesto vigente / obligado / devengado?").

## Datos

- `data/presupuesto_ejecucion_2024.csv` → nuevo `www/datos/presupuesto-ejecucion-2024.json` (via generador).
- `data/contrataciones_muni_2024.csv` → `www/datos/contrataciones-2024.json`.
- `www/datos/indicadores-gasto-2026.json` y `www/datos/contrataciones-2026.json` (ya existen).

## Estructura de archivos

- `scripts/generar_datos_web.py` — EXTENDER para también generar los JSON de 2024 (función parametrizada por año).
- `www/JS/gasto.js` — añadir lógica de selector de año y render por año.
- `www/gasto.html` — añadir selector `<select>` de año y contenedores condicionales.
- `www/metodologia.html` — ampliar limitaciones (2024 parcial, no hay pagos por partida).
- Nuevo `www/glosario` dentro de `gasto.html` (sección colapsada/visible) o `www/glosario.html` → decidir en plan (mínimo: sección en gasto.html).

## Criterios de éxito

- La página Gasto muestra un selector de año funcional (2024/2026).
- Con 2024: tabla de ejecución (vigente/obligado/%) y contrataciones 2024.
- Con 2026: los indicadores actuales por categoría.
- JSONs de 2024 generados por script (trazable, parametrizado por año).
- Metodología ampliada con limitaciones reales.
- Sin página "Presupuesto" separada.
- Tests pasan (incluido test del generador por año).
- Desplegado en `datospublicos.muchotexto.net/gasto.html`.