# DATA_INVENTORY.md — Inventario de fuentes (foco: contratación pública)

> **Fecha de revisión tras el pivot:** 27 de agosto de 2026
> **Método:** verificación directa de URLs/fetch sobre la fuente. Estado de la investigación para el proyecto.
> El proyecto pivoteó a **contratación pública (DNCP)** como única línea de datos activa.

---

## Resumen ejecutivo

**La fuente central del proyecto es la DNCP (Dirección Nacional de Contrataciones Públicas)**, el portal paraguayo de datos abiertos de contratación:
- Publica **datos realmente abiertos**: CSV masivos por año, API V3 documentada, licencia **CC BY 4.0**.
- Cubre **todas las entidades públicas** del país (identificadas por **código SICP**), lo que hace al motor **multi-entidad** por diseño.
- Estandar: **OCDS** (Open Contracting Data Standard), internacional.

**El primer caso publicado es la Municipalidad de Asunción (SICP 108)**, con datasets de 2024 y 2026.

**Regla de alcance (decidida tras el pivot):** el proyecto solo consume fuentes que publican datos abiertos limpios, sin romper la página (sin captchas, sin OCR de PDFs corruptos, sin ingeniería inversa del SPA). Lo que no se obtiene limpio se documenta como **brecha de la institución**, no se fuerza.

---

## La fuente DNCP

| Atributo | Valor |
|---|---|
| Portal | `www.contrataciones.gov.py/datos/` |
| Datasets por año | `.../images/opendata-v3/final/ocds/{AÑO}/{modulo}-masivo.zip` |
| Módulos | records (procesos), awards (adjudicaciones), contracts (contratos), + proveedores |
| API V3 | `.../datos/api/v3/doc/` (OAuth, token 15 min; para consultas puntuales) |
| Licencia | CC BY 4.0 |
| Cobertura | desde 2010 |
| Estándar | OCDS 1.1 (aplanado a CSV) |

### Cómo aislar una entidad
- Cada entidad se identifica por su **código SICP** (ej. Municipalidad de Asunción = `108`).
- En los CSV, `buyer/id` = `DNCP-SICP-CODE-{SICP}` y `buyer/name` = nombre.
- El pipeline verifica consistencia entre ambos (nombre ↔ SICP).

### Datasets publicados por el proyecto (por entidad+año)

| Dataset | Año | Registros | Estado |
|---|---|---|---|
| `data/contrataciones_muni_2026.csv` | 2026 | 36 | ✅ |
| `data/contrataciones_muni_2024.csv` | 2024 | 28 | ✅ |

---

## Brechas (documentadas, no forzadas)

El pivot no elimina el conocimiento de estos vacíos; los hace **agenda de incidencia** en vez de carga activa:

1. **Nómina/salarios de la Muni**: `datos.hacienda.gov.py` → 403; portal SFP requiere replicar payload del SPA; PDFs de Hesakã tienen texto no extraíble (fuente corrupta). No accesible limpio.
2. **Transferencias MEF**: portal con API pero bloqueada por captcha propio (server-side). Solo descarga manual.
3. **Presupuesto aprobado detallado / ejecución mensual**: no publicado en abierto.
4. **Reclamos (Dashboard MCA)**: sistema interno sin API pública.

Estas brechas se referencian en `Metodología` (web) y quedan descritas para futuros **pedidos formales de acceso a la información (Ley 5282/14)**.

---

## Trazabilidad

Cada dataset del proyecto conserva: URL de la fuente, fecha de obtención, proceso (pipeline), validaciones y limitaciones. Ver `data/README.md` y `Metodología`.