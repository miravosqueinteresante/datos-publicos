# MuchoTexto Data

Infraestructura de **datos verificables sobre Paraguay** que se ubica debajo del contenido
editorial de MuchoTexto: selecciona información pública relevante, la extrae, normaliza,
conserva su procedencia y la convierte en conocimiento reutilizable.

Cada fuente es un conector independiente con interfaz `fetch → extract → normalize → validate → store`.
Principio: no almacenar lo que no se necesita; conservar solo derivados, metadatos y trazabilidad.

## Sitio

- **Plataforma pública:** https://datospublicos.muchotexto.net
- **Energía (ANDE):** https://datospublicos.muchotexto.net/energia.html — 75 indicadores (BAGP, Pliego 21, Compilación 2000–2020)
- **Itaipú:** https://datospublicos.muchotexto.net/itaipu.html — 135 indicadores (ONS Brasil 2000–2026, horario, 27 años)
- **Yacyretá:** https://datospublicos.muchotexto.net/yacyreta.html — 14 indicadores (EBY 2016–2025, mensual+anual)
- **Grafo:** https://datospublicos.muchotexto.net/grafo.html — entidades→indicadores→artículos (Fase 11)

## Qué hace

- **ANDE** — demanda, consumo por categoría, pérdidas, clientes, tarifas, generación. PDF (`pdfplumber`), kWh→GWh, `perdidas_distribucion 20,03%` validada (`20,03+4,37=24,40`), invariantes y snapshots.
- **Itaipú** — generación total, sector 60/50 Hz, suministro PY/BR. ONS `GERACAO_ITAIPU.csv` (26+ años horario, `;`), MW·h→GWh.
- **Yacyretá** — generación total y suministro PY/AR. EBY mensual HTML + informes anuales 2016-2025 (14 regs), invariante 9+ meses.
- **Grafo** — `www/datos/grafo.json` con 3 entidades, 4 relaciones y artículos reales de `muchotexto.net`.

Cada registro lleva: `id`, `entidad`, `entidad_id`, `indicador`, `valor`, `unidad`, `fecha_inicio/fin`, `fuente`, `url`, `fecha_extraccion`, `metodo_extraccion`, `estado_verificacion`.

## Arquitectura

- `connectors/ande/` — extractor, normalizer, validators, metadata, entidad, connector, run, tests (incl. invariantes)
- `connectors/itaipu/` — extractor CSV ONS, normalizer, metadata, connector, run, tests (11)
- `connectors/yacyreta/` — extractor HTML EBY, normalizer, metadata, connector, curados, run, tests (4)
- `www/` — `energia.html`, `itaipu.html`, `yacyreta.html`, `grafo.html`, `index.html`, `sitemap.xml`, `robots.txt`, `og-image.png`, `css/style.css` (monophase dark `#212529` cian `#3bc9db`, charts canvas con tooltip)
- `www/datos/` — `ande-indicadores.json` (75), `itaipu-indicadores.json` (135), `yacyreta-indicadores.json` (14), `grafo.json`

## Entidades

Registro `connectors/ande/entidades.json` con IDs canónicos: `ande`, `itaipu`, `yacyreta`. Lookup en `entidad.py` (`get`, `nombre_a_id` con normalización NFKD).

## Fuentes

- **ANDE** — BAGP 2025, Pliego 21, Compilación 2000–2020
- **Itaipú/ONS** — https://dados.ons.org.br/dataset/geracao_itaipu (CSV horario, sin auth, diaria)
- **Yacyretá/EBY** — https://www.eby.gov.py/generacion-de-energia/ (mensual HTML) + informes anuales 2016-2025

## Automatización

- `actualizar-ande` / `actualizar-itaipu` (diario) / `actualizar-yacyreta` (mensual) — `permissions: contents: write`, cron + `workflow_dispatch`, tests → run → commit/push `www/datos/*.json`
- `deploy-pages` — `actions/deploy-pages@v4` publica `www/` (sitemap, og-image, canonical)
- `dependabot.yml` — pip + Actions mensual
- Seguridad: `esc()` en `www/*.html`, `timeout=60` en `fetch`, sin secretos expuestos

