# Datos Públicos — Datasets de contratación (Municipalidad de Asunción)

Datasets de procesos de contratación de la **Municipalidad de Asunción** (Paraguay), por ejercicio. El pipeline es parametrizable por año (`python scripts/dncp_contrataciones.py <AÑO>`).

## Datasets disponibles

- `data/contrataciones_muni_2024.csv` — 28 procesos del ejercicio 2024.
- `data/contrataciones_muni_2026.csv` — 36 procesos del ejercicio 2026.

## Origen

- **Fuente:** DNCP (Dirección Nacional de Contrataciones Públicas) — Portal de Datos Abiertos.
- **URL (por año):** `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/{AÑO}/masivo.zip`
- **Fecha de obtención:** 2024 y 2026 descargados el 27 de agosto de 2026.
- **Licencia:** Creative Commons BY 4.0 (`https://creativecommons.org/licenses/by/4.0/`). Atribución requerida.
- **Proceso:** pipeline `scripts/dncp_contrataciones.py` (descarga → join por OCID de records + awards + awa_suppliers + contracts → filtro por `buyer/name = "Municipalidad de Asunción"` → limpieza → validación → consistencia SICP 108).

## Contenido

- **2024:** 28 procesos (27 con objeto, 21 con proveedor, 19 con fecha de contrato). **2026:** 36 procesos (con proveedor 16-17, según corrida).
- Columnas: `id` (OCID), `objeto`, `estado`, `categoria`, `tipo_procedimiento`, `comprador`, `proveedor`, `monto`, `moneda`, `fecha_publicacion`, `fecha_adjudicacion`, `fecha_contrato`, `url_muni`.

## Limitaciones

- Solo procesos donde el comprador declarado es exactamente la Municipalidad de Asunción (SICP 108). Procesos donde participa como cofinanciante/cogestor (no comprador) quedan fuera.
- Los procesos sin proveedor son llamados que no registraron adjudicación en el dataset del año (o aún no adjudicados).
- El ZIP descargado (`masivo.zip`, ~490 MB) queda en `data/_sin_versionar/` (no versionado) para reproceso local.

## Reproceso

```bash
python scripts/dncp_contrataciones.py 2024   # genera contrataciones_muni_2024.csv
python scripts/dncp_contrataciones.py 2026   # genera contrataciones_muni_2026.csv
```
Automatización (GitHub Actions) pendiente — manual primero (plan maestro).