# MuchoTexto Data

Infraestructura de **datos verificables sobre Paraguay** que se ubica debajo del contenido
editorial de MuchoTexto: selecciona información pública relevante, la extrae, normaliza,
conserva su procedencia y la convierte en conocimiento reutilizable.

El primer conector es **ANDE** (energía) y sirve de laboratorio para la arquitectura de
conectores. Toda fuente sigue el principio de no almacenar lo que no se necesita: se consumen
API/CSV/HTML y, solo cuando la fuente es PDF, se extraen los datos necesarios conservando la
referencia exacta. Lo que no se obtiene limpio en abierto se documenta como brecha de la
institución.

## Sitio

- **Plataforma pública:** https://datospublicos.muchotexto.net
- **Página de energía:** https://datospublicos.muchotexto.net/energia.html

## Qué hace

- **Energía (ANDE)** — indicadores eléctricos estructurados y verificables: demanda, consumo,
  pérdidas, clientes, tarifas, consumo por categoría y generación/abastecimiento (Itaipú,
  Yacyretá, Acaray). Cada dato lleva fuente, URL, fecha de obtención y método de extracción.

## Arquitectura

- `connectors/ande/` — conector (fetch → extract → normalize → validate → store): extractor,
  normalizer, validators, metadata, connector y tests.
- `data/` — solo derivados: indicadores, series, metadatos y proveniencia (no descargas masivas).
- `docs/fuentes/` — fichas por fuente (`ande-data-map.md`).
- `scripts/` — pipeline genérico de conectores y generadores (Python).
- `www/` — sitio de la plataforma pública (GitHub Pages).
- `lab/` — web del laboratorio (GitHub Pages).
- `research_ande/` — investigación de fuentes y brechas del conector ANDE.

Interfaz común por conector: `fetch()` / `extract()` / `normalize()` / `validate()` / `store()`.

## Fuente

- **ANDE** — Balance Anual de Generación y Pérdidas (BAGP), Pliego tarifario, Compilación
  Estadística de Generación 2000–2020, e informes de binacionales (Itaipú, Yacyretá).

## Automatización

- `actualizar-ande` (GitHub Actions): ejecuta el conector ANDE, valida y regenera
  `www/datos/ande-indicadores.json`.
- `deploy-pages`: publica `www/` en GitHub Pages.

## Regla importante

El **documento maestro** del proyecto es interno y de distribución limitada: vive solo en local
(`MUCHOTEXTO DATA - DOCUMENTO MAESTRO.md`) y NO se versiona ni se publica en este repositorio.
