# Datos Públicos — Pipeline de indicadores de gasto (DNCP) + brecha de salarios

Fecha: 2026-08-26

## Propósito

Avanzar la pregunta "¿en qué gasta la Municipalidad de Asunción?" con los datos **disponibles y estructurados** hoy (contrataciones de la DNCP), produciendo un **dataset de indicadores de gasto** (distribución por categoría y por proveedor). A la vez, documentar con evidencia la **brecha de salarios** (nómina) investigada en esta sesión.

## Contexto — investigación realizada (26-ago-2026)

Se evaluaron las 3 vías para obtener la masa salarial de la Muni, con evidencia real:

| Vía | Resultado | Estado |
|---|---|---|
| **Nómina nacional** (datos.gov.py / datos.hacienda.gov.py) | `datos.hacienda.gov.py` → **403 Forbidden**; API DKAN sin endpoint JSON consumible; la página del dataset no expone recursos descargables | ❌ Bloqueada |
| **Portal SFP** (datos.sfp.gov.py) | **API REST real descubierta**: `datos.sfp.gov.py/api/rest` (JBoss, JSON). `/funcionarios/partitions` 200, `/oee/data` 200 (434 organismos), `/funcionarios/data` 200 (43.376.600 registros) | ⚠️ Funciona PERO filtrar por la Muni requiere replicar el payload exacto de filtros del SPA (por códigos entidad/oee/nivel, no por nombre; el `search` del DataTables no filtra). Ingeniería inversa pendiente |
| **Hesakã** (asuncion.gov.py) | PDFs públicos (140, patrón de URL predecible) pero **escaneados** (364 págs/mes, sin texto extraíble) → requiere OCR | ❌ OCR = proyecto pesado (instalar tesseract/easyocr + modelos; riesgo en números) |

**Conclusión:** la masa salarial exacta de la Muni **no es accesible hoy** como formato estructurado de bajo esfuerzo. Se documenta como **BRECHA** (no como dato), y se prioriza el indicador de gasto con los datos de contrataciones ya pipelinezados (DNCP, estructurados, CC BY 4.0).

## Alcance

**Incluye:**
- `scripts/indicadores_gasto.py` — lee `data/contrataciones_muni_2026.csv`, calcula indicadores de gasto y produce JSON.
- Dataset de salida: `www/datos/indicadores-gasto-2026.json` con:
  - Distribución por categoría (Bienes/Servicios/Obras): montos y % del total.
  - Distribución por tipo de procedimiento.
  - Monto por proveedor (top, con % acumulado).
  - Totales (procesos, monto total adjudicado, proveedores distintos).
- Actualización de `DATA_INVENTORY.md`: documentar la brecha de salarios investigada (3 vías, con URLs y frenos) y la fuente de indicadores.
- Opcional (si baja el costo): data preparada para la sección "Gasto" de la plataforma.

**Excluye (no en esta fase):**
- OCR de Hesakã / integración de la nómina.
- Ingeniería inversa completa del filtro de SFP.
- Cambios al pipeline de contrataciones (DNCP) existente.
- Segmentación territorial (requiere GIS).

## Decisiones

1. Los indicadores de gasto se derivan de las **contrataciones** (compras adjudicadas), no del presupuesto total de la Muni (que no se publica en abierto). El indicador se etiquetará claro: **"gasto en contrataciones adjudicadas"**, no "presupuesto".
2. `scripts/indicadores_gasto.py` con tests (TDD), siguiendo el patrón del proyecto (stdlib).
3. El JSON de indicadores es consumible por la web/lab (misma ruta `www/datos/`).
4. Brecha de salarios documentada con evidencia (URLs y frenos verificados).

## Criterios de éxito

- `scripts/indicadores_gasto.py` pasa sus tests.
- `www/datos/indicadores-gasto-2026.json` generado con datos reales (36 procesos; distribución por categoría; top proveedores).
- Las sumas por categoría coinciden con el total del dataset (validación cruzada).
- `DATA_INVENTORY.md` actualizado con la brecha de salarios (3 vías, frenos) y la fuente de indicadores.
- Sin dependencias nuevas (stdlib).