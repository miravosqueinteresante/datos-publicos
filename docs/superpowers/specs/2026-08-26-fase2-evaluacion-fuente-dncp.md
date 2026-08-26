# Datos Públicos — FASE 2: Evaluación formal de la fuente DNCP (contrataciones de la Muni)

Fecha: 2026-08-26

## Propósito

Evaluar formalmente la **DNCP (Dirección Nacional de Contrataciones Públicas)** como primera fuente de datos del proyecto, siguiendo los 7 criterios del plan maestro (sección 18). El resultado es la decisión documentada de construir el primer pipeline sobre esta fuente (FASE 3), con el detalle técnico necesario para planificarlo.

## Fuente seleccionada

**DNCP — Contrataciones de la Municipalidad de Asunción.**

¿Por qué? (decisión tomada en la evaluación comparativa del 26-ago-2026):
- Responde la pregunta del plan maestro: "¿Qué está haciendo la Municipalidad, dónde y cuánto?" (objeto, monto, proveedor).
- Es la más estructurada y automatizable del inventario (estándar OCDS, CSV descargables sin auth, CC BY 4.0).
- Es la más reutilizable: la DNCP cubre todos los municipios de Paraguay → un pipeline construido una vez sirve para el modelo multi-municipio del plan (motor + configuración).

## Alcance de la evaluación

### A. Criterios del plan maestro (sección 18)
Para la fuente DNCP, evaluar y documentar con EVIDENCIA verificada (consultas reales, no inferencias):

1. **Disponibilidad** — ¿podemos acceder realmente? ¿registro/OAuth necesario? ¿rate limits?
2. **Estructura** — ¿el estándar OCDS cubre lo que necesitamos? ¿qué datasets existen?
3. **Actualización** — ¿con qué frecuencia se actualizan los datos de la Muni?
4. **Calidad** — ¿datos completos y consistentes? (cobertura temporal, campos vacíos, proveedores)
5. **Automatización** — ¿descarga programática? ¿API V3 vs datasets CSV? ¿qué es lo mínimo viable?
6. **Utilidad** — ¿responde la pregunta pública? ¿Qué indicadores/fichas se pueden derivar?
7. **Reutilización** — ¿cómo se extiende a otro municipio (config vs código)?

### B. Detalle técnico imprescindible (para FASE 3)
1. **Cómo aislar a la Municipalidad de Asunción** — parámetro/filtro correcto (buscar por nombre de convocante/UOC "Municipalidad de Asunción"; RUC si aplica). Verificar en la UI del búscador y/o datasets.
2. **Datasets necesarios** — ¿PLANIFICACIONES, LICITACIONES (convocatorias), ADJUDICACIONES, CONTRATOS, PAGOS? Ruta de descarga CSV exacta.
3. **Volumen histórico** — cuántos registros aproximados de la Muni desde 2010; tamaño de los CSV.
4. **Licencia y atribución** — confirmar CC BY 4.0 y qué atribuir.
5. **Frecuencia de actualización para el pipeline** — diaria/semanal/mensual según datos reales.
6. **Restricciones** — límite de 10.000 registros por llamada API, token 15 min, etc.

## Entregables

1. `docs/` actualizado con la evaluación formal de la fuente (una ficha por criterio con evidencia: URLs consultadas, fechas, números).
2. Sección en `DATA_INVENTORY.md` marcando la fuente seleccionada y su evaluación.
3. **Decisión documentada** para pasar a FASE 3 con los requisitos técnicos del pipeline.

## Criterios de éxito

- Los 7 criterios evalúan con evidencia de consultas reales (fechas + URLs).
- Se conoce exactamente cómo aislar los datos de la Municipalidad de Asunción en la DNCP.
- Se identifican los datasets CSV/API mínimos para el primer pipeline.
- Se documenta volumen, frecuencia y licencia.
- Queda explícito qué cambiaría para reusar el pipeline en otro municipio.

## NO se hace en esta fase

- Construir el pipeline (FASE 3).
- Escribir código de descarga.
- Configurar GitHub Actions.
- Visualizaciones.