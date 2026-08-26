# Datos Públicos — FASE 4: Primer producto útil (página en www/)

Fecha: 2026-08-26

## Propósito

Construir **una sola funcionalidad útil** (plan maestro, sección 20) que responda la pregunta pública: **"¿Qué está haciendo la Municipalidad, cuánto y con quién?"**, usando el dataset de 36 procesos de contratación 2026 (FASE 3). Es la semilla de la plataforma pública que vivirá en `datospublicos.muchotexto.net`.

## Alcance

**Incluye (mínimo útil):**
- Página estática en `www/` (HTML + CSS + JS vanilla, sin frameworks ni librerías).
- Generador CSV→JSON (`scripts/generar_datos_web.py`) que convierte `data/contrataciones_muni_2026.csv` en `www/datos/contrataciones-2026.json` (con test).
- Secciones de la página:
  1. **Cabecera** — título, pregunta que responde, fecha de datos y fuente/licencia (CC BY 4.0, DNCP).
  2. **Métricas** — nº procesos, monto total (PYG), nº proveedores distintos, categorías (goods/services/works).
  3. **Tabla de procesos** — todas las filas, con búsqueda por texto y filtro por categoría.
  4. **Top proveedores** — ranking por monto, con acumulado.
- Trazabilidad visible: URL fuente y nota metodológica.

**Excluye (no en esta fase, es FASE 5/6):**
- Dashboard del laboratorio (`lab/`).
- Automatización del pipeline (GitHub Actions).
- Configuración del dominio/subdominio.
- Múltiples años, mapas, o productos adicionales.

## Datos

- Entrada: `data/contrataciones_muni_2026.csv` (36 procesos; columnas del FASE 3).
- Salida web: `www/datos/contrataciones-2026.json` (array de objetos; montos como número, fechas ISO, `id` OCID, `url_muni`).
- El generador re-descarga nada; solo transforma el CSV ya versionado.

## Estructura de archivos

```
www/
├── index.html              # página principal
├── css/style.css           # estilos (vanilla)
├── js/app.js               # lógica (lee JSON, renderiza, filtra, ordena)
└── datos/
    └── contrataciones-2026.json   # generado (versionado)
scripts/generar_datos_web.py       # CSV→JSON (con test)
scripts/tests/test_generar_web.py  # test del generador
```

## Criterios de éxito

- `scripts/generar_datos_web.py` pasa su test.
- `www/datos/contrataciones-2026.json` generado con las 36 filas del CSV, montos numéricos.
- `www/index.html` abre en navegador sin consola de errores y muestra: métricas, tabla filtrable, top proveedores.
- La página funciona sin red de backend (solo archivos estáticos, GitHub Pages-ready).
- Responde la pregunta pública de forma directa.

## Decisiones cerradas

1. Producto = página estática single-file en `www/`, JS vanilla, sin build step.
2. Datos servidos como JSON estático generado por script (trazable y reproducible).
3. Manual primero; lo que se genere se versiona.
4. La página no depende de muchotexto.net (repos separados) y queda lista para publicarse luego en `datospublicos.muchotexto.net`.