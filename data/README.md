# Contrataciones de la Municipalidad de Asunción — 2026

Dataset de procesos de contratación de la **Municipalidad de Asunción** (Paraguay), año **2026**.

## Origen

- **Fuente:** DNCP (Dirección Nacional de Contrataciones Públicas) — Portal de Datos Abiertos.
- **URL:** `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/2026/masivo.zip`
- **Fecha de obtención:** 26 de agosto de 2026.
- **Licencia:** Creative Commons BY 4.0 (`https://creativecommons.org/licenses/by/4.0/`). Atribución requerida.
- **Proceso:** pipeline `scripts/dncp_contrataciones.py` (descarga → join por OCID de records + awards + awa_suppliers + contracts → filtro por `buyer/name = "Municipalidad de Asunción"` → limpieza → validación).

## Contenido

- **36 procesos** (un registro por licitación/proceso de la Muni con `buyer/name` exacto "Municipalidad de Asunción").
- De esos: **17 con proveedor adjudicado**, **9 con fecha de contrato**, **36 con monto**.
- Columnas: `id` (OCID), `objeto`, `estado`, `categoria` (goods/services/works), `tipo_procedimiento`, `comprador`, `proveedor`, `monto`, `moneda`, `fecha_publicacion`, `fecha_adjudicacion`, `fecha_contrato`, `url_muni`.

## Limitaciones

- Solo procesos donde el comprador declarado es exactamente la Municipalidad de Asunción (SICP 108). Procesos donde participa como cofinanciante/cogestor (no comprador) quedan fuera.
- Los procesos sin `proveedor` son llamados que no registraron adjudicación en el dataset del año (o aún no adjudicados).
- El ZIP descargado (`masivo.zip`, ~490 MB) queda en `data/_sin_versionar/` (no versionado) para reproceso local.

## Reproceso

```bash
python scripts/dncp_contrataciones.py
```
Genera `data/contrataciones_muni_2026.csv`. Automatización (GitHub Actions) pendiente — manual primero (plan maestro).