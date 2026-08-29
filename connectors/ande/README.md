# Conector ANDE

Primer conector de MuchoTexto Data (energía). Sirve de laboratorio para la arquitectura general.

**Especificación:** [`docs/fuentes/ande-data-map.md`](../fuentes/ande-data-map.md) — inventario de
indicadores, fuentes, formatos y brechas (investigado el 2026-08-29).

**Estructura prevista** (maestro §5):
- `connector` — dónde buscar y cómo detectar actualizaciones
- `extractor` — extracción de PDF/HTML (ANDE no tiene API ni CSV)
- `normalizer` — unidades (kWh/MWh/GWh/MW/kW), períodos
- `validators` — cambios anormales, duplicados, períodos superpuestos
- `metadata` — fuente, URL, fecha de extracción, método

**Estado:** Fase 3 (Data Map) completa. Fase 4 (implementación del conector) pendiente.
