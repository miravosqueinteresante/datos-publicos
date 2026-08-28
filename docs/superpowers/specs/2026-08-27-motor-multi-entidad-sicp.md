# Datos Públicos — Parametrización multi-entidad del motor DNCP (SICP)

Fecha: 2026-08-27

## Propósito

Hacer el motor `scripts/dncp_contrataciones.py` **multi-entidad**: que pueda generar datasets de contratación de cualquier entidad pública de la DNCP, identificada por su **código SICP**, manteniendo **Municipalidad de Asunción (SICP 108) como la entidad activa por defecto** (el foco actual del proyecto).

Alineado con el plan maestro post-pivot (paso 2 del motor: "parametrizar entidad por SICP").

## Decisión de diseño

- **Filtro por SICP (ID)** como mecanismo primario: usar `buyer/id = "DNCP-SICP-CODE-{N}"` (campo ya presente en cada fila de records.csv). Es robusto y único, evita ambigüedades de nombre.
- El **nombre** se conserva solo como atributo visible del dataset (`comprador`), no como filtro.
- La **verificación de consistencia** se parametriza por SICP y compara ID vs nombre (control de calidad).
- **Compatibilidad:** la CLI mantiene los usos actuales: `python scripts/dncp_contrataciones.py 2026` sigue produciendo el dataset de la Muni (SICP 108 por defecto); se añade el parámetro opcional de SICP: `python scripts/dncp_contrataciones.py 2026 226`.

## Cambios en `scripts/dncp_contrataciones.py`

1. `es_entidad_por_sicp(fila, sicp)` — filtra por `buyer/id == DNCP-SICP-CODE-{sicp}` (reemplaza `es_de_asuncion`).
2. `verificar_consistencia(filas_records, sicp="108")` — parametrizado; compara ID (SICP) vs nombre (mantiene de fondo por trazabilidad).
3. `main(anio="2026", sicp="108")` — filtra por SICP, nombra el dataset según la entidad: como el foco es la Muni, el archivo sigue `contrataciones_muni_{anio}.csv` para SICP 108; para otra entidad → `contrataciones_{sicp}_{anio}.csv` (decisión: nombres preservar el actual para no romper el flujo web).
4. `args` → añadir SICP como 2º argumento posicional (default "108").

## Compatibilidad y no-ruptura

- `python scripts/dncp_contrataciones.py 2026` → idéntico al actual (dataset Muni 2026).
- El flujo web (`generar_datos_web.py`, indicadores, `_site`) sigue consumiendo `contrataciones_muni_{anio}.csv` → sin cambios en la publicación.
- Tests existentes de `test_dncp.py` deben seguir pasando (adaptando los que usan `es_de_asuncion`).

## Criterios de éxito

- `dncp_contrataciones.py` acepta SICP: corrida `2026 108` produce el mismo resultado que antes (36 procesos).
- Corrida con otro SICP (ej. `2026 226`, UNA) produce un dataset de esa entidad (verificación de que el motor es general).
- Tests adaptados + nuevos pasan.
- La web y el lab no cambian (la Muni sigue siendo la publicada).
- Sin romper el pipeline/generadores existentes.