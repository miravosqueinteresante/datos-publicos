# Datos Públicos — Restaurar buscador de contratos en el perfil Municipalidad

Fecha: 2026-08-28

## Propósito

Restaurar el **buscador de contratos** (tabla con búsqueda por objeto/proveedor + filtro por categoría) que se perdió en el refactor `d3a0ebf` (consolidación Explorar→Municipalidad). Se integra como sección "Contratos" DENTRO de `www/municipalidad.html`, alineada con el selector de año existente.

## Decisión

- Agregar sección "Procesos / Contratos" en `municipalidad.html` con: input de búsqueda, filtro de categoría, tabla (objeto, categoría, proveedor, monto, fechas, enlace).
- Reutilizar la lógica de historial (`renderTabla`, `filaTabla`, `normalizar`) en `www/js/municipalidad.js`, adaptada a cargar los contratos del año elegido (`datos/contrataciones-{año}.json`).
- El selector de año ya existente (`sel-anio-muni`) dispara la recarga de indicadores Y contratos.

## Archivos y criterios

- `www/municipalidad.html`: += sección "Contratos" (inputs + tabla tbody #tabla).
- `www/js/municipalidad.js`: += `normalizar`, `renderContratos(anio)` y llamada desde `init` + listener del selector.
- No toca datos/pipeline; tests OK; desplegado.
- Criterio: al cambiar año, la tabla muestra los contratos de ese año y permite buscar/filtrar.