# Datos Públicos — FASE 5b: Navegación multi-sección del laboratorio (lab/)

Fecha: 2026-08-26

## Propósito

Preparar el laboratorio (`lab/`) para crecer, dándole la misma navegación multi-sección que el www, pero con **solo secciones reales** (sin tabs vacíos, respetando la sección 21 del plan: no inflar el dashboard).

## Alcance

**Incluye (3 secciones reales):**
- `lab/index.html` — **Resumen**: métricas del dataset + estado del pipeline (contenido actual + menú).
- `lab/pipelines.html` — **Pipelines**: detalle del pipeline individual (DNCP): pasos, verificación SICP, id de convocante, datos.
- `lab/datos.html` — **Datos**: datasets disponibles orientado al estado interno (mismo contenido de www/datos.html pero con foco técnico: pipeline, formato, fuente).

- Menú sticky compartido (Explorar/Resumen · Pipelines · Datos) con el mismo CSS de `www/css/style.css`.
- Coherencia visual con el www (mismo sistema 2026).

**Excluye (no en esta fase):**
- Tabs futuros (Fuentes, Errores, Logs, Ejecuciones) — se agregan cuando exista algo que mostrar.
- Cambios en el pipeline o generadores.
- Datos nuevos.

## Estructura de archivos

```
lab/
├── index.html        # Resumen (métricas + estado + menú)
├── pipelines.html    # Pipelines (detalle del pipeline DNCP)
└── datos.html        # Datos (datasets, orientado al estado interno)
```

## Criterios de éxito

- Las 3 páginas del lab abren sin errores y comparten el menú.
- Reutilizan `../www/css/style.css` (CSS y JS sin duplicación de estilos).
- Contenido real en cada sección (nada vacío).
- Coherente con el diseño 2026 del www.
- Todo versionado y pusheado.