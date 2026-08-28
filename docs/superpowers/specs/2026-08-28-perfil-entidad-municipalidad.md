# Datos Públicos — Perfil de la entidad: Municipalidad de Asunción

Fecha: 2026-08-28

## Propósito

Consolidar todo el análisis de la Municipalidad de Asunción en **una única página de perfil de entidad** (`www/muni.html`), que reúne la serie temporal, los indicadores y las fichas de proveedores. Es el "dashboard de la casa" por entidad que la DNCP NO ofrece (el perfil de convocante es listado + CSV; el SIE es nacional). Menú simplificado.

## Decisión de arquitectura

- **Unificar en "Municipalidad"**: Explorar y Análisis se consolidan en `www/muni.html`.
- Menú nuevo: **Demo · Municipalidad · Datos · Metodología**.
- Explorar (`index.html`) y Análisis (`analisis.html`) se eliminan del menú (su contenido pasa a la página perfil). El deploy copia `www/` → raíz; se genera `www/muni.html`.

## Estructura de la página perfil

1. **Cabecera de entidad**: Municipalidad de Asunción · SICP 108 · nota fuente (DNCP, CC BY 4.0) · selector de año.
2. **Serie temporal 2023-2026**: tabla de evolución (procesos, monto, proveedores, monto relativo).
3. **Indicadores por año** (selector): categorías, procedimientos, concentración de proveedores.
4. **Principales proveedores**: fichas desplegables (top 10 por monto, métricas + contratos).
5. **Metodología / limitaciones** de la entidad.

## Archivos

- `www/muni.html` (nueva, consolidada).
- `www/js/muni.js` (nueva; consolida la lógica de serie + detalle + fichas, reutilizando el patrón de `analisis.js`).
- `www/index.html`, `www/analisis.html` → contenido se absorbe; esos archivos se eliminan (el perfil los reemplaza). Se conserva `www/datos.html`, `www/metodologia.html`, `www/demo.html`, `lab/`.
- Menú actualizado en las páginas restantes (Demo, Municipalidad, Datos, Metodología).

## Datos reutilizados (sin cambios)

- `www/datos/contrataciones-{año}.json` (2023-2026).
- `www/datos/indicadores-gasto-{año}.json`.
- `www/datos/proveedores.json`.

## Criterios de éxito

- `www/muni.html` reúne serie + indicadores por año + fichas de proveedores (todo lo de Explorar+Análisis).
- Menú: Demo · Municipalidad · Datos · Metodología (Explorar/Análisis fuera).
- Conserva la funcionalidad (selector de año, evolución, detalcción por año, fichas desplegables).
- Tests de scripts OK (no se tocan datos).
- Desplegado y verificado en producción `datospublicos.muchotexto.net/muni.html`.