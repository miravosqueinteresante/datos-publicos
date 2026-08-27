# Datos Públicos — PIVOT: de multi-tema a "Contratación pública DNCP multi-entidad"

Fecha: 2026-08-27
Estado: DISEÑO APROBADO (brainstorming complete)

## Propósito

Reestructurar TODO el proyecto para que gire exclusivamente sobre **contratación pública de Paraguay (DNCP)**, con motor parametrizable por entidad (SICP) y año, manteniendo nombre "Datos Públicos" y dominio `datospublicos.muchotexto.net`. Se elimina todo lo de presupuesto/finanzas de la actividad del proyecto (el historial de git lo conserva).

**Regla del proyecto que se mantiene:** el documento maestro (PDF) es SOLO LOCAL, nunca versionado (AGENTS.md).

## Alcance del pivot

**Nuevo posicionamiento:** "Datos Públicos analiza y hace visible la contratación pública de Paraguay (DNCP), entidad por entidad. Municipalidad de Asunción = primer caso publicado; motor listo para cualquier entidad."

**Qué permanece (núcleo contratación):**
- `scripts/dncp_contrataciones.py` + `scripts/tests/test_dncp.py` — motor DNCP parametrizado por SICP/año.
- `scripts/generar_datos_web.py` + test — genera JSON por entidad/año.
- `scripts/indicadores_gasto.py` + test → pasa a "indicadores de contratación" (concentración, % método, categorías, tiempos de ciclo — patrones OCP).
- `scripts/publicar_sitio.py` + test — build de Pages.
- Workflows `actualizar-datos.yml` y `deploy-pages.yml`.
- Web: `demo.html`, `index.html` (Explorar), `metodologia.html` (rediseñadas a solo-DNCP).
- JSON web de contrataciones 2024/2026 + indicadores.

**Qué se elimina del repo (actividad del proyecto):**
- `scripts/presupuesto_2024.py`, `scripts/tests/test_presupuesto_2024.py`.
- `data/presupuesto_ejecucion_2024.csv`.
- `docs/presupuesto/` (FUENTES_2024.md, NOTA-tecnica-hesaka).
- `www/datos/presupuesto-ejecucion-2024.json`.
- `www/gasto.html` → se reemplaza por "Análisis" (indicadores de contratación); se elimina la parte presupuestaria.
- `www/js/gasto.js` → reemplazado por JS de análisis de contratación.
- Specs/plans de: inventario-presupuesto, presupuesto-ejecucion, integracion-ciclo-presupuesto (2026-08-27).
- `DATA_INVENTORY.md` → reescrito a foco contratación DNCP (sin dominios C/D/E).

**Qué se reescribe:**
- PDF maestro (solo local) → nueva versión enfocada en contratación DNCP multi-entidad (con backup).
- `README.md` — posicionamiento nuevo, estructura, estado.
- `AGENTS.md` — convenciones; conserva regla del plan maestro solo-local.
- `lab/` — Resumen/Pipelines/Datos a solo-DNCP.
- `www/gasto.html`+JS → página "Análisis" (indicadores OCP sobre contratos).
- `www/datos.html`, `www/metodologia.html` — a solo-DNCP.

## Estructura destino

```
datos-publicos/
├── README.md, AGENTS.md, .gitignore
├── data/                  # CSV de contratación por entidad+año
├── scripts/               # dncp_contrataciones, generar_datos_web, indicadores, publicar_sitio
├── docs/                  # (sin docs/presupuesto) superpowers + fuentes/dncp-evaluacion
├── lab/                   # estado del motor DNCP (Resumen/Pipelines/Datos)
├── www/                   # Demo, Explorar, Análisis, Datos, Metodología
└── .github/workflows/     # actualizar-datos + deploy-pages
```

## Orden de ejecución

1. Tag de respaldo del estado previo (`v0-pre-pivot`).
2. Eliminar archivos de presupuesto (git rm).
3. Rediseñar web: `gasto.html` → `analisis.html` (indicadores OCP); limpiar demo/datos/metodologia a solo-DNCP.
4. Rediseñar lab a solo-DNCP.
5. Reescribir `DATA_INVENTORY.md`, `README.md`, `AGENTS.md`.
6. Reescribir PDF maestro (local, con backup).
7. Actualizar workflow `actualizar-datos` si referenciaba presupuesto (verificar).
8. Verificación integral: tests, build `_site`, deploy, dominio.

## Criterios de éxito del pivot

- El repo no contiene: presupuesto, rendición, Hesakã, MEF, gasto por objeto, ni "ciclo presupuestario".
- Web en línea (`datospublicos.muchotexto.net`) con páginas solo-DNCP y selector de entidad/año.
- Motor multi-entidad: `dncp_contrataciones.py` corre para la Muni (108) y queda parametrizable a cualquier SICP.
- Indicadores de contratación (OCP): % método, categorías, concentración proveedores, tiempos de ciclo.
- Lab refleja el estado del motor.
- Tests pasan; deploy funciona; dominio responde.
- PDF maestro reescrito a solo-contrataciones (local).