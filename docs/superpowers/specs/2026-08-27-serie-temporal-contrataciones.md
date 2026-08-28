# Datos Públicos — Serie temporal de contrataciones (Municipalidad de Asunción, 2023-2026)

Fecha: 2026-08-27

## Propósito

Construir la **serie temporal** de contrataciones de la Municipalidad de Asunción para los años **2023-2026**, de modo que los indicadores "crezcan con el tiempo" (patrón del plan maestro: "construir → simplificar → serie histórica"). Mantiene el foco exclusivo en la Muni (entidad activa SICP 108); no se publica otra entidad.

## Alcance

- **Datos:** generar `data/contrataciones_muni_{año}.csv` para 2023 y 2025 (2024 y 2026 ya existen) usando el motor multi-entidad (`python scripts/dncp_contrataciones.py <AÑO>` con SICP por defecto 108).
- **Web (Explorar):** selector de año 2023-2026 en `www/index.html` + `app.js` (carga el JSON del año elegido; por defecto el más reciente 2026).
- **Web (Análisis):** nueva sección **"Evolución por año"** con comparativa multi-año (procesos / monto / proveedores) y selector de año para el detalle por indicador.
- **Generador:** `generar_datos_web.py` → años `["2023","2024","2025","2026"]`; `indicadores_gasto.py` → JSON de indicadores por año.
- **Lab:** tabla de datasets actualizada a 4 años.

## Decisiones

1. La entidad es SIEMPRE la Muni (SICP 108) — serie temporal, no multi-entidad en la web.
2. Indicadores por año: `www/datos/indicadores-gasto-{año}.json` (se mantiene el 2026 existente como referencia; se generan los demás).
3. Explorar: select con años disponibles, default = 2026.
4. Análisis: la comparativa multi-año se arma leyendo los 4 JSON de indicadores.

## Estructura de archivos

- `data/contrataciones_muni_2023.csv`, `data/contrataciones_muni_2025.csv` (nuevos).
- `www/datos/contrataciones-2023.json`, `contrataciones-2025.json` (nuevos; 2024/2026 existentes).
- `www/datos/indicadores-gasto-2023.json`, `-2024.json`, `-2025.json` (nuevos; -2026 existente).
- `www/js/app.js` — selector de año.
- `www/index.html` — contenedor del selector.
- `www/js/analisis.js` — comparativa + selector.
- `www/analisis.html` — contenedores de comparativa.
- `lab/datos.html` — tabla de 4 años.

## Criterios de éxito

- 4 CSV (2023-2026) de la Muni generados y validados (verificación SICP/counts).
- 4 JSON de contrataciones + 4 de indicadores generados.
- Explorar tiene selector de año funcional (2023-2026).
- Análisis muestra "Evolución por año" (tabla comparativa) + selector de detalle.
- Tests del generador adaptados/pasando.
- Todo pusheado; deploy refleja la serie.