# Datos Públicos — FASE 5: Dashboard del laboratorio (lab/)

Fecha: 2026-08-26

## Propósito

Crear el inicio del laboratorio (`lab/`), la interfaz que muestra **cómo funciona el sistema** (plan maestro, sección 6.1). Siguiendo la sección 21: *"no construir un dashboard enorme antes de tener algo que monitorizar"*. Hoy hay **un** pipeline real monitorizable → el lab empieza con una página que lo refleja, sin inventar secciones vacías.

## Alcance

**Incluye (mínimo real):**
- `lab/index.html` — página estática (HTML + JS vanilla).
- Muestra métricas reales del dataset leyendo el JSON existente del www (`../www/datos/contrataciones-2026.json`): procesos, monto total, proveedores distintos, categorías.
- Sección "Estado del pipeline": fuente (DNCP, CC BY 4.0), última actualización del dataset, estado de la última ejecución del workflow (success).
- Vínculo a la plataforma pública (`../www/index.html`).
- Reutiliza `www/css/style.css` (sin duplicar CSS).

**Excluye (no en esta fase):**
- Tabs del plan (Fuentes, Datasets, Pipelines, Errores, Actualizaciones) — la mayoría vaciaría hoy (1 pipeline).
- Historial de ejecuciones en vivo vía API de GitHub (dependencia frágil).
- Nuevo generador de JSON de estado (el JSON del www es suficiente).
- Automatización de la sección de ejecución (manual por ahora; se automatizará al escalar — YAGNI).

## Estructura de archivos

- `lab/index.html` — página única.
- (reusa) `www/css/style.css`, `www/js/app.js` (no: app.js es del www; el lab renderiza su propia lógica mínima inline o en `lab/js` — decidir en plan: reusar funciones o inline simple).

## Contenido de la página

1. **Cabecera:** "DATOS PÚBLICOS — LAB" · subtitulo "cómo funciona el sistema".
2. **Métricas del dataset** (leídas del JSON): Procesos 2026 · Monto adjudicado · Proveedores distintos · Categorías.
3. **Estado del pipeline:**
   - Fuente: DNCP (enlace), licencia CC BY 4.0.
   - Última actualización del dataset: fecha del commit del CSV (estado documentado).
   - Última ejecución del workflow: success (26-ago-2026).
4. **Vínculo:** "Ver plataforma pública".

## Criterios de éxito

- `lab/index.html` abre sin errores de consola y muestra las métricas del JSON real.
- Reutiliza el CSS del www (sin copiar estilos).
- No duplica generadores de datos.
- Cumple el principio del plan: muestra algo real y monitorizable, sin inflar.
- Todo versionado y pusheado.