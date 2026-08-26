# Datos Públicos — FASE 3: Primer pipeline (DNCP → contrataciones de la Muni)

Fecha: 2026-08-26

## Propósito

Construir el primer pipeline de datos de punta a punta del proyecto: obtener los procesos de contratación de la Municipalidad de Asunción desde la DNCP, procesarlos y entregar un dataset estructurado, limpio y validado. Es la prueba de que la arquitectura funciona (plan maestro, sección 15).

## Fuente

**DNCP — CSV masivos OCDS** (ver ficha `docs/fuentes/dncp-evaluacion.md`):
- URL: `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/{AÑO}/masivo.zip`
- Módulo `records` (resumen por proceso), año **2026**.
- Identificación de la Muni: convocante SICP `108` / `compiledRelease/buyer/name` contiene "Municipalidad de Asunción".
- Licencia: CC BY 4.0 (atribución requerida).
- Referencia: 70 procesos de la Muni en records.csv 2026 (verificado FASE 2).

## Alcance

**Incluye (mínimo completo):**
- Descarga del ZIP `masivo.zip` 2026 (~49 MB, anónimo).
- Extracción de `records.csv`.
- Filtrado por "Municipalidad de Asunción".
- Transformación a CSV plano compartible con columnas útiles.
- Validación (conteo, campos clave no vacíos, montos numéricos).
- Salida a `data/contrataciones_muni_2026.csv` (versionado).
- Copy del ZIP a carpeta no versionada para reproceso local.

**Excluye (no en esta fase):**
- Más de un año o más de un módulo.
- Automatización con GitHub Actions (después, según plan: manual primero).
- Visualizaciones / plataforma web.
- API V3 con OAuth.

## CSV de salida

`data/contrataciones_muni_2026.csv` — columnas:

| Columna | Significado | Fuente en records.csv |
|---|---|---|
| `id` | Identificador del proceso (OCID) | `compiledRelease/id` |
| `objeto` | Nombre/objeto de la licitación | `compiledRelease/tender/title` |
| `estado` | Estado del proceso | `compiledRelease/tender/status` (o award/contract status si aplica) |
| `categoria` | Categoría de bienes/servicios | `compiledRelease/tender/...` o campo de categoría |
| `tipo_procedimiento` | Tipo de procedimiento | `compiledRelease/tender/procurementMethod` o `_details` |
| `comprador` | Nombre del comprador (Muni) | `compiledRelease/buyer/name` |
| `proveedor` | Proveedor(s) adjudicado(s) | `compiledRelease/awards/0/suppliers/0/name` (o concatenados) |
| `monto` | Monto (número) | `compiledRelease/awards/0/value/amount` |
| `moneda` | Moneda | `compiledRelease/awards/0/value/currency` |
| `fecha_adjudicacion` | Fecha de adjudicación (ISO) | `compiledRelease/awards/0/date` |
| `fecha_contrato` | Fecha de firma de contrato (ISO) | `compiledRelease/contracts/0/dateSigned` |
| `fecha_publicacion` | Fecha de publicación | `compiledRelease/tender/...` o release date |
| `url_muni` | URL amigable del proceso | construida desde `id` o campo URL si existe |

(Nota: los nombres exactos de columnas OCDS se confirman al inspeccionar el `records.csv` real; los mapeados de arriba son la intención, los nombres exactos pueden variar — el script debe detectar la columna correcta de forma robusta o mapear tras la 1ª ejecución.)

## Validación (criterios de éxito)

- Script pasa los tests (TDD).
- `data/contrataciones_muni_2026.csv` con procesos de la Muni. **Verificado (26-ago-2026): 36 procesos** con `buyer/name = "Municipalidad de Asunción"` en `masivo.zip` 2026 (la referencia previa de ~70 provenía de filtrar el módulo `awa-masivo.zip`, no el `masivo.zip` completo; el dato canónico es 36 sobre el ZIP usado por este pipeline). De esos 36: 17 con proveedor/adjudicación, 9 con fecha de contrato, 36 con monto.
- Todas las filas con `id` (OCID) y `objeto` no vacíos.
- Montos parseados a número cuando están presentes (celdas vacías solo donde el dato no aplica, documentadas).
- El ZIP queda en `data/_sin_versionar/` (ignorado por git).
- Trazabilidad: se documenta fecha de obtención y URL en el `__main__`/README del dataset.

## Estructura de archivos

- `scripts/dncp_contrataciones.py` — pipeline (descarga, extracción, filtro, limpieza, validación).
- `scripts/tests/test_dncp.py` — tests (TDD).
- `data/contrataciones_muni_2026.csv` — dataset versionado.
- `.gitignore` — añadir `data/_sin_versionar/`.

## Decisiones cerradas

1. Un año (2026), un módulo (records), un dataset CSV plano.
2. Descarga anónima por URL construida (sin API).
3. Manual primero; GitHub Actions después.
4. Dataset versionado en `data/`, ZIP en carpeta no versionada.