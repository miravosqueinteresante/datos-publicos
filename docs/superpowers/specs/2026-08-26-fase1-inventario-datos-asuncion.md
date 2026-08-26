# Datos Públicos — FASE 1: Inventario de datos de la Municipalidad de Asunción

Fecha: 2026-08-26

## Propósito

Responder «¿qué información pública tenemos realmente disponible?» sobre la Municipalidad de Asunción, y registrarlo en `DATA_INVENTORY.md` versionado en el repo. Es la base de las fases siguientes (evaluación de fuentes, selección de primera fuente, primer pipeline).

## Alcance

**Incluye:** fuentes oficiales de la Municipalidad de Asunción (asuncion.gov.py, jma.gov.py) y portales nacionales que publican datos de la municipalidad (DNCP contrataciones, datos.gov.py, INE, Hesaka).

**Excluye:** fuentes no oficiales (prensa, blogs, terceros), y la evaluación formal / selección de la primera fuente (eso es FASE 2 y 3).

## Metodología

Cada fuente se documenta siguiendo los criterios del plan maestro (secciones 17 y 18):

- Fuente / URL
- Tipo (sitio web, dataset, API, PDF, documento, mapa, archivo descargable)
- Formato (HTML, PDF, CSV, JSON, GeoJSON, etc.)
- Frecuencia de actualización
- Cobertura temporal
- Calidad / consistencia observada
- Accesibilidad (¿se puede acceder real? ¿requiere JS? ¿HTTP sin HTTPS?)
- Posibilidad de automatización
- Limitaciones
- Condiciones de reutilización
- Pregunta pública que podría responder

## Subtópicos de investigación

1. **Sitio oficial asuncion.gov.py** — transparencia, presupuesto, contrataciones, obras, ordenanzas, resoluciones, edictos, datos abiertos, archivo.
2. **Junta Municipal (jma.gov.py)** — buscador de ordenanzas, biblioteca digital, transparencia, actas, calendario de sesiones, concejales.
3. **Presupuesto y finanzas municipales** — ejecución presupuestaria, salarios (Hesaka), tributos, presupuesto participativo.
4. **Contrataciones y obras** — DNCP (licitaciones de la Muni), obras públicas, infraestructura.
5. **Datos territoriales y técnicos** — mapas, GIS, catastro, servicios, estadísticas, plan de desarrollo.

## Resultado esperado

`DATA_INVENTORY.md` en la raíz del repo (versionado), con:

- Resumen de hallazgos.
- Tabla o catálogo de fuentes, cada una con su ficha de trazabilidad.
- Sección de brechas y oportunidades (qué no existe pero podría construirse).
- Nota metodológica (fecha de investigación, fuentes consultadas).
- Referencia a la investigación previa de muchotexto.net que sirvió de base.

## Criterios de éxito

- `DATA_INVENTORY.md` existe, versionado, en español.
- Cada fuente con URL, formato, frecuencia, limitaciones y trazabilidad.
- Cubre los 5 subtópicos (municipal, legislativa, finanzas, contrataciones/obras, territorial).
- Se distingue claramente lo verificado en esta fase de lo heredado de research_ordenanzas (ago 2026).
- No incluye ninguna copia del plan maestro.