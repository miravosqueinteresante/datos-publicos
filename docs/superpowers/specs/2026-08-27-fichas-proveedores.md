# Datos Públicos — Fichas de proveedores (top 10) en Análisis

Fecha: 2026-08-27

## Propósito

Agregar a la página **Análisis** una sección "Principales proveedores de la Municipalidad de Asunción" con **10 fichas** (top por monto acumulado en la serie 2023-2026). Cada ficha muestra tarjeta + indicadores + lista de contratos. Solo datos del dataset (trazable, sin inventar).

## Datos

Fuente: la serie `data/contrataciones_muni_2023..2026.csv` (agregación por proveedor). El dataset actual no incluye RUC/rubro/ubicación → la ficha NO lo inventa.

### Top 10 real (verificado 27-ago-2026, por monto acumulado 2023-2026)

| # | Proveedor | Monto (PYG) | Contratos | Años activos |
|---|---|---|---|---|
| 1 | PETROLEOS DEL SUR S.A. | 108.357.991.829 | 2 | 2 |
| 2 | Consorcio CCC-TECSUL | 64.777.837.460 | 1 | 1 |
| 3 | BERNARDA GONZALEZ MORINIGO | 56.504.679.224 | 9 | 4 |
| 4 | RAIZEN PARAGUAY S.A. | 53.697.593.060 | 1 | 1 |
| 5 | TECO S.R.L. | 43.760.328.210 | 2 | 2 |
| 6 | TECNOLOGIA DEL SUR S.A.E. | 40.175.663.895 | 2 | 2 |
| 7 | COMTEL S.A. | 31.799.380.000 | 2 | 2 |
| 8 | COMPAÑIA DE PETROLEO Y ASFALTO S.A. (COMPASA) | 24.139.200.000 | 3 | 2 |
| 9 | Consorcio de Gestión Integral de Residuos | 24.000.000.000 | 1 | 1 |
| 10 | PRESTIGIO DEL SUR S.R.L | 17.762.997.000 | 11 | 3 |

(161 proveedores distintos en la serie; top 10 seleccionado por monto.)

## Contenido de cada ficha

| Bloque | Campos | Cálculo |
|---|---|---|
| Identidad | Nombre del proveedor | directo |
| Métricas | Monto total | suma de montos del proveedor en la serie |
| | Nº de contratos | conteo |
| | Años activos | cuántos de los 4 años tiene contratos |
| | Categoría principal | la que concentra mayor monto del proveedor |
| | % procedimiento directo vs público | monto por procedimiento (directo/otras) / total |
| | Posición en ranking | posición por monto acumulado |
| Lista de contratos | Objeto, año, categoría, monto, procedimiento, fecha adjudicación, enlace DNCP | de los registros del proveedor |

## Decisiones

1. Integrado en la página Análisis (no páginas individuales); fichas desplegables.
2. Datos en un JSON `www/datos/proveedores.json` generado por `scripts/generar_proveedores.py` (TDD).
3. Definiciones honestas: "directo" = todo lo que NO es licitación pública (menor cuantía, directo, excepción); "categoría principal" = mayor monto.
4. Solo top 10 por monto; los proveedores que no tienen adjudicación (sin monto) quedan fuera.

## Estructura de archivos

- `scripts/generar_proveedores.py` — agrega la serie y produce `www/datos/proveedores.json`.
- `scripts/tests/test_generar_proveedores.py` — tests.
- `www/analisis.html` — sección "Proveedores" con contenedor.
- `www/js/analisis.js` — render de las 10 fichas + toggle expandir.

## Criterios de éxito

- `proveedores.json` con el top 10 (por monto), cada uno con métricas y lista de contratos.
- Tests del generador pasan.
- Análisis muestra la sección "Proveedores" con las 10 fichas desplegables.
- Ficha correcta y trazable (datos del dataset, sin inventar RUC/rubro).
- Todo pusheado y desplegado.