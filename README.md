# Datos Públicos

Analiza y hace visible la **contratación pública de Paraguay** (DNCP), entidad por entidad.
Convierte los datos abiertos de contratación en información comprensible, verificable y útil:
exploración por entidad y año, indicadores de competencia y concentración, y datasets descargables.

**Primer caso publicado:** Municipalidad de Asunción (SICP 108), años 2024 y 2026.

## Sitios

- **Plataforma pública:** https://datospublicos.muchotexto.net
- **Laboratorio técnico:** https://datospublicos.muchotexto.net/lab

## Qué hace

- **Explorar** — contratos de una entidad+año, con búsqueda y filtros.
- **Análisis** — indicadores de contratación: distribución por categoría, % por método de procedimiento, concentración por proveedor (patrones Open Contracting).
- **Datos** — datasets descargables (por entidad+año).
- **Metodología** — cómo se obtienen los datos, trazabilidad y limitaciones.

## Motor

`scripts/dncp_contrataciones.py` — descarga los CSV masivos OCDS de la DNCP por año, une tablas por OCID, filtra por entidad (SICP), valida y produce datasets. Parametrizable por año; la entidad se parametriza por SICP (primera entidad: Muni de Asunción).

```
python scripts/dncp_contrataciones.py 2026   # dataset Muni 2026
python scripts/dncp_contrataciones.py 2024   # dataset Muni 2024
```

## Fuente

- **DNCP** — Portal de Datos Abiertos (`contrataciones.gov.py/datos/`), licencia CC BY 4.0.

## Automatización

- `actualizar-datos` (GitHub Actions): mensual + manual; regenera datasets y JSON web.
- `deploy-pages`: publica automáticamente en GitHub Pages.

## Estado

- FASE 0-6 del plan previo + automatización + publicación completadas (ver historial git/`docs/superpowers/`).
- **Pivot a contratación (2026-08-27):** el proyecto queda focalizado en contratación DNCP multi-entidad (se eliminó la línea de presupuesto).

## Regla importante

El **documento maestro** del proyecto es interno y de distribución limitada: vive solo en local y NO se versiona ni se publica en este repositorio.