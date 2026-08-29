# Plan de migración: Datos Públicos (DNCP/Municipalidad) → MuchoTexto Data

**Fecha:** 2026-08-29
**Estado:** Aprobado (diseño)
**Documento maestro:** `MUCHOTEXTO DATA - DOCUMENTO MAESTRO.md` (local, no versionado)
**Alcance de esta sesión:** solo documento maestro + este plan. El código y el sitio se migran en fases posteriores.

---

## Contexto del pivot

El proyecto nació como análisis de contratación pública (DNCP) entidad por entidad, con foco en la
Municipalidad. Se abandona ese concepto. MuchoTexto Data es ahora una **infraestructura de datos
verificables sobre Paraguay** que se ubica debajo del contenido editorial de MuchoTexto: estructura,
normaliza y demuestra con evidencia oficial. El primer conector es **ANDE** (energía), usado como
laboratorio para diseñar la arquitectura de conectores.

**Decisiones ya tomadas:**
- **Repo:** se conserva el nombre `Datos Publicos`. El borrador define "Proyecto de datos: Datos Públicos / capa de datos de MuchoTexto".
- **Dominio:** se conserva `https://datospublicos.muchotexto.net` (fijado en `www/CNAME` y usado por `deploy-pages.yml`).
- **Documento maestro:** sigue siendo SOLO LOCAL, fuera de Git (regla de `AGENTS.md`).

---

## Fase 0 — Documento maestro y plan (esta sesión)
- [x] Eliminar `DATOS PÚBLICOS - DOCUMENTO MAESTRO DEL PROYECTO.pdf`.
- [x] Crear `MUCHOTEXTO DATA - DOCUMENTO MAESTRO.md` (local, no versionado) a partir del borrador, con nota de pivot.
- [x] Crear y commitear este plan en `docs/superpowers/plans/2026-08-29-muchotexto-data-migracion.md`.
- [ ] Añadir `MUCHOTEXTO DATA - DOCUMENTO MAESTRO.md` a `.gitignore` para evitar commitearlo por error.

## Fase 1 — Borrar la identidad Municipalidad/DNCP
**Sitio (`www/`):** `municipalidad.html`, `js/municipalidad.js`, `proveedores.html`, `js/proveedores.js`.
**Datos:** `data/contrataciones_muni_*.csv`, `data/metadata_*.json`, `www/datos/contrataciones-*.json`,
`www/datos/indicadores-gasto-*.json`, `www/datos/proveedores.json`, `www/datos/metadata-*.json`,
`data/_sin_versionar/*` (masivos + rendición de cuentas PDF → mover a archivo muerto o borrar).
**Scripts:** `dncp_contrataciones.py`, `generar_proveedores.py`, `indicadores_gasto.py`,
`generar_datos_web.py`, `publicar_sitio.py` y sus tests en `scripts/tests/`.
Conservar `actualizar_datos.py` solo como esqueleto reutilizable si aplica.
**Docs:** `docs/comparacion-dncp-vs-datos-publicos.md`, `docs/fuentes/dncp-evaluacion.md`, `DATA_INVENTORY.md`
→ reescribir para el nuevo enfoque o retirar.
**Reglamento:** actualizar `AGENTS.md` (hoy dice "el proyecto analiza contratación pública (DNCP)") para
reflejar MuchoTexto Data.

## Fase 2 — Nueva arquitectura de carpetas
```
connectors/
  ande/            # connector, extractor, normalizer, validators, metadata
data/              # solo derivados: indicadores, series, metadatos, proveniencia
docs/fuentes/      # fichas por fuente (ande.md, ...)
scripts/           # pipeline genérico + tests
www/               # sitio MuchoTexto Data (Energía como primer producto)
```
Interfaz común por conector: `fetch() / extract() / normalize() / validate() / store()`.

## Fase 3 — ANDE Data Map (primer entregable técnico del conector)
Inventario indicador por indicador con columnas: indicador, fuente ANDE, formato (HTML/PDF/CSV/API),
frecuencia, histórico, método de extracción, prioridad. Cobertura inicial: demanda, consumo, pérdidas,
tarifas, clientes, consumidores intensivos, generación/abastecimiento. De este mapa salen el extractor
real y el esquema de la base.

## Fase 4 — Conector ANDE MVP
~10–15 indicadores iniciales: extracción → normalización → validación (cambios anormales, unidades
kWh/MWh/GWh/MW/kW, duplicados, períodos superpuestos) → base con el modelo de datos del maestro (§9) y
estados de verificación (§11). Separación estricta dato / cálculo / interpretación (§13).

## Fase 5 — Nuevo sitio (`www`): "MuchoTexto Data — Energía"
Indicadores principales + series históricas + fuente visible + metodología + entidades relacionadas
(ANDE, Itaipú, Yacyretá) + artículos MuchoTexto. Flujo editorial → datos → fuente original.

## Fase 6 — Automatización (GitHub Actions)
Workflow que ejecuta el conector ANDE, busca actualizaciones, valida, guarda, regenera indicadores y
actualiza el sitio, con registro de cambios (§20). Frecuencia según la fuente (mensual para ANDE).

## Fases futuras (incrementales, por pregunta → fuente)
- Fase 7: Energía (Itaipú, Yacyretá, Viceministerio de Minas y Energía).
- Fase 8: Economía (BCP, MEF).
- Fase 9: Población/territorio (INE).
- Fase 10: Tecnología/regulación (MITIC, fuentes jurídicas).
- Fase 11: grafo de conocimiento (entidades + indicadores + artículos + fuentes).

---

## Criterios de éxito del MVP (§24 del maestro)
Exactitud, trazabilidad, reproducibilidad, automatización, facilidad de actualización y reutilización
editorial. No se mide por cantidad de datos.
