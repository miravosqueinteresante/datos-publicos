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

## Foco del proyecto (post-pivot)

El proyecto analiza **contratación pública (DNCP)** entidad por entidad. La fuente es la DNCP
(datos abiertos, OCDS, CC BY 4.0). No se consumen fuentes que requieran romper captchas, OCR
de PDFs corruptos o ingeniería inversa de SPA: lo que no se obtiene limpio se documenta como
brecha de la institución.

## Estructura de carpetas

- `docs/` — documentación del proyecto; specs en `docs/superpowers/specs/`, planes en `docs/superpowers/plans/`
- `data/` — datasets de contratación (por entidad+año)
- `scripts/` — pipeline DNCP y generadores (Python)
- `lab/` — web del laboratorio (GitHub Pages)
- `www/` — web de la plataforma pública (GitHub Pages)
- `.github/workflows/` — GitHub Actions (actualizar-datos, deploy-pages)

## Convenciones

- Un solo repositorio para todo el sistema (lab y plataforma son interfaces del mismo proyecto).
- Archivos Markdown en español.
- Proceso manual primero; automatizar (GitHub Actions) solo lo que ya se entiende y funciona.
- Datos siempre con trazabilidad: fuente original, URL, fecha de obtención, proceso y limitaciones.
- No prometer en la web datos que no se puedan obtener en abierto.

## Flujo de trabajo

- Feature nueva → spec → plan → implementación (TDD cuando aplique código) → revisión.
- Commits pequeños y frecuentes en español.