# AGENTS.md — Datos Públicos

Guía para agentes de IA y colaboradores al trabajar en este repositorio.

## Regla crítica: el plan maestro es SOLO LOCAL

El documento `DATOS PÚBLICOS - DOCUMENTO MAESTRO DEL PROYECTO.pdf` es interno y de
distribución limitada.

- NO lo añadas al repositorio.
- NO lo transcribas a `docs/` ni a ningún archivo versionado.
- NO subas ninguna copia a GitHub.
- Vive únicamente en la carpeta local del proyecto (fuera del área de Git).

Si un agente lo necesita como referencia, puede leerlo desde el disco local, pero nunca
persistirlo en un archivo del repo.

## Foco del proyecto

MuchoTexto Data es una **infraestructura de datos verificables sobre Paraguay** que se ubica debajo
del contenido editorial de MuchoTexto: selecciona información pública relevante, la extrae, normaliza,
conserva su procedencia y la convierte en conocimiento reutilizable. El primer conector es **ANDE**
(energía) y sirve de laboratorio para la arquitectura de conectores. Toda fuente sigue el principio de
no almacenar lo que no se necesita: se consumen APIs/CSV/HTML y, solo cuando la fuente es PDF, se extraen
los datos necesarios conservando la referencia exacta. No se consumen fuentes que requieran romper
captchas, OCR de PDFs corruptos o ingeniería inversa de SPA: lo que no se obtiene limpio se documenta
como brecha de la institución. El documento maestro local (`MUCHOTEXTO DATA - DOCUMENTO MAESTRO.md`)
y el plan de migración (`docs/superpowers/plans/`) describen la arquitectura completa.

## Estructura de carpetas

- `docs/` — documentación del proyecto; specs en `docs/superpowers/specs/`, planes en `docs/superpowers/plans/`, fichas de fuente en `docs/fuentes/`
- `data/` — solo derivados: indicadores, series, metadatos y proveniencia (no descargas masivas)
- `connectors/` — un conector por fuente (`connectors/ande/`: connector, extractor, normalizer, validators, metadata)
- `scripts/` — pipeline genérico de conectores y generadores (Python)
- `lab/` — web del laboratorio (GitHub Pages)
- `www/` — web de la plataforma pública (GitHub Pages)
- `.github/workflows/` — GitHub Actions (deploy-pages; el pipeline de conectores se añade en Fase 6)

## Convenciones

- Un solo repositorio para todo el sistema (lab y plataforma son interfaces del mismo proyecto).
- Archivos Markdown en español.
- Proceso manual primero; automatizar (GitHub Actions) solo lo que ya se entiende y funciona.
- Datos siempre con trazabilidad: fuente original, URL, fecha de obtención, proceso y limitaciones.
- No prometer en la web datos que no se puedan obtener en abierto.

## Flujo de trabajo

- Feature nueva → spec → plan → implementación (TDD cuando aplique código) → revisión.
- Commits pequeños y frecuentes en español.