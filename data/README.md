# Contrataciones de la Municipalidad de Asunción — 2024 y 2026

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
- Los procesos sin `proveedor` son llamados que no registraron adjudicación en el dataset del año (o aún no adjudicados).
- El ZIP descargado (`masivo.zip`, ~490 MB) queda en `data/_sin_versionar/` (no versionado) para reproceso local.

## Reproceso

```bash
python scripts/dncp_contrataciones.py 2024   # genera contrataciones_muni_2024.csv
python scripts/dncp_contrataciones.py 2026   # genera contrataciones_muni_2026.csv
```
Automatización (GitHub Actions) pendiente — manual primero (plan maestro).

---

# Ejecución del presupuesto — Municipalidad de Asunción, 2024

Dataset de **ejecución del gasto** del ejercicio 2024 (por nivel de objeto del gasto), extraído de la Rendición de Cuentas 2024.

## Origen

- **Fuente:** Rendición de Cuentas 2024 (Municipalidad de Asunción), página 4 — "Ejecución del Presupuesto de Gastos por Niveles del Objeto del Gasto".
- **URL:** `https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf`
- **Fecha de obtención:** 27 de agosto de 2026.
- **Proceso:** pipeline `scripts/presupuesto_2024.py` (descarga PDF → extrae tabla por bloques con coordenadas → normaliza montos → valida total → escribe CSV).

## Contenido

- **7 niveles** del objeto del gasto + TOTAL (100 a 900): Servicios Personales, Servicios No Personales, Bienes de Consumo e Insumos, Inversión Física, Servicio de la Deuda Pública, Transferencias, Otros Gastos.
- Columnas: `ejercicio`, `nivel`, `denominacion`, `presupuesto_vigente`, `obligado`, `porcentaje_ejecucion`, `fuente`, `url`.
- Montos en **millones de guaraníes** (como reporta la fuente).
- **Total vigente: 2.360.168 MGs** (verificado, coincide con el PDF). Ejecución global ≈ **53%** (según la rendición); el obligado de Transferencias no se desglosa en la fuente.

## Limitaciones

- **Obligado de Transferencias (nivel 800):** la Rendición publica solo vigente (134.272) y %; el obligado separado no existe en el PDF → la suma de obligado del dataset (1.165.830) **excluye transferencias**; el total oficial obligado (1.253.270) los incluye.
- **No hay detalle por partida ni pagos mensuales** (no publicado; ver `docs/presupuesto/FUENTES_2024.md`, brechas P01/P02/P06).
- Columnas `presupuesto_inicial`, `modificacion`, `pagado` no están en esta fuente (declarado, no inventado).

## Reproceso

```bash
python scripts/presupuesto_2024.py
```
Genera `data/presupuesto_ejecucion_2024.csv`. El PDF queda en `data/_sin_versionar/` (no versionado).