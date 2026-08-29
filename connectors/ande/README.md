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
API ni CSV; el conector también soporta PDF.

**Formatos soportados**
- HTML: `extractor.extract(html)` → consumo total, demanda máxima, generación por central.
- PDF: `connector.run_pdf(path, url)` / `run_text(text, url)` con parsers para:
  - `consumo por categoría` (MWh → GWh)
  - `tarifas` residenciales BT por tramo (G/kWh)
  - `pérdidas` total / distribución / transmisión (%)
  - `clientes` total y nuevos

La extracción PDF usa `pdfplumber` (ver `requirements.txt`); el texto se parsea con los mismos
patrones que el HTML. Los tests usan *fixtures representativos* (`fixtures/pdf_*.txt`); la
validación contra los PDF reales de ANDE es el siguiente paso manual (criterio del maestro:
"manual primero, automatizar lo que ya funciona").
