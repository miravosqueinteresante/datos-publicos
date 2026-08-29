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

**Estado:** implementado (Fase 4) y con automatización (Fase 6).

**Ejecutar manualmente:**
```
python -m connectors.ande.run
```
Genera `www/datos/ande-indicadores.json` desde la fuente ANDE.

**Automatización:** `.github/workflows/actualizar-ande.yml` corre el conector mensualmente
(workflow_dispatch + cron) y commitea el dataset si cambió; el deploy existente reconstruye el sitio.

**Nota de robustez:** la fuente actual es la nota `interna.php?id=14877` (HTML). ANDE no expone
API ni CSV; ampliar a PDF (consumo por categoría, tarifas, pérdidas) es la siguiente iteración.
