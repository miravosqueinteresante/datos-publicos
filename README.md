# MuchoTexto Data

Infraestructura de **datos verificables sobre Paraguay** que se ubica debajo del contenido
editorial de MuchoTexto: selecciona información pública relevante, la extrae, normaliza,
conserva su procedencia y la convierte en conocimiento reutilizable.

Cada fuente es un conector independiente con interfaz `fetch → extract → normalize → validate → store`.
Principio: no almacenar lo que no se necesita; conservar solo derivados, metadatos y trazabilidad.

## Sitio

- **Plataforma pública:** https://datospublicos.muchotexto.net
- **Energía (ANDE):** https://datospublicos.muchotexto.net/energia.html — 75 indicadores (BAGP, Pliego 21, Compilación 2000–2020)
- **Itaipú:** https://datospublicos.muchotexto.net/itaipu.html — 135 indicadores (ONS Brasil 2000–2026, horario)

## Qué hace

- **ANDE** — demanda, consumo por categoría, pérdidas, clientes, tarifas, generación (Acaray + binacionales). Extracción PDF (`pdfplumber`), normalización kWh→GWh, sistema de entidades (`entidad` + `entidad_id`).
- **Itaipú** — generación total, por sector (60 Hz / 50 Hz) y suministro a Paraguay/Brasil. Fuente ONS Brasil (`GERACAO_ITAIPU.csv`, 26+ años horario, `;` delimiter), agregación anual MW·h→GWh.

Cada registro lleva: `id`, `entidad`, `entidad_id`, `indicador`, `valor`, `unidad`, `fecha_inicio/fin`, `fuente`, `url`, `fecha_extraccion`, `metodo_extraccion`, `estado_verificacion`.

## Arquitectura

- `connectors/ande/` — extractor, normalizer, validators, metadata, entidad, connector, run, tests (56 tests)
- `connectors/itaipu/` — extractor CSV ONS, normalizer, metadata, connector, run, tests (11 tests)
- `www/` — sitio público (GitHub Pages): `energia.html`, `itaipu.html`, `css/style.css` (monophase dark, cian `#3bc9db`), datos en `www/datos/*.json`
- `docs/superpowers/plans/` — planes (Data Map, entidades, Itaipú)
- `docs/fuentes/` — fichas por fuente
- `data/` — solo derivados (indicadores, series, metadatos)

## Entidades

Registro `connectors/ande/entidades.json` con IDs canónicos: `ande`, `itaipu`, `yacyreta`. Lookup en `entidad.py` (`get`, `nombre_a_id` con normalización NFKD).

## Fuentes

- **ANDE** — BAGP 2025, Pliego 21, Compilación 2000–2020, binacionales curados (Itaipú/Yacyretá prensa)
- **Itaipú/ONS** — https://dados.ons.org.br/dataset/geracao_itaipu (CSV horario, sin auth, actualización diaria)

## Automatización

- `actualizar-ande` (GitHub Actions, `permissions: contents: write`): `pdfplumber` + tests → `python connectors/ande/run.py` → commit/push `www/datos/*.json` si hay cambios
- `deploy-pages`: publica `www/` vía `actions/deploy-pages@v4` (artifact `www`)

