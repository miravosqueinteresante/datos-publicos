# FUENTES_2024.md — Inventario de fuentes del ciclo presupuestario 2024
# Municipalidad de Asunción

> **Fecha de investigación:** 27 de agosto de 2026
> **Método:** verificación directa de URLs (fetch HTTP) sobre fuentes oficiales; extracción de texto de PDFs con PyMuPDF. Sin URLs inventadas; cada fuente marcada con estado real.
> **Regla (documento maestro de contexto):** no inventar datos; las brechas se reconocen. Este inventario responde *qué existe* para reconstruir el presupuesto 2024 — **no se programó nada**.

---

## Resumen ejecutivo

El ciclo presupuestario 2024 de la Municipalidad de Asunción es **parcialmente reconstruible en abierto**, pero con dos vacíos importantes:

**DISPONIBLE (verificado):**
- **Rendición de Cuentas 2024** — única fuente municipal que publica **ejecución del gasto** (presupuesto vigente vs. obligado, agregado anual por objeto del gasto: total 2.360.168 / obligado 1.253.270 MGs ≈ 53%). Incluye ingresos recaudados 2024 (1.113.156 MGs) y obras.
- **Presupuesto aprobado 2025** (patrón documentado) y reprogramaciones 2024 (**ORD 156/24**) + base tributaria 2024 (**ORD 107/23** + modif. **ORD 128/24**).
- **Hesakã (salarios) 2024** — 12 PDFs mensuales disponibles en URL, pero **texto no extraíble** (fuente corrupta) → requiere OCR/ingeniería (documentado con evidencia).
- **DNCP contrataciones 2024** — dump OCDS disponible (~236 MB); el pipeline existente lo procesa pasando `anio="2024"`.
- **MEF transferencias a la Muni** — consultable por RUC + año 2024 (desde 2017), exporta Excel/PDF (requiere interacción/captcha).

**NO ENCONTRADO (brechas):**
- **Presupuesto aprobado 2024** (PDF detallado) — el sitio solo retiene el año vigente (2025); `/presupuesto-2024` da **404**.
- **Ordenanza que aprueba el presupuesto/gastos 2024** — no publicada en el listado municipal; requiere el buscador de la Junta Municipal (JMA, IP `:3000`, SPA no rastreable por fetch) o pedido de información.
- **Ejecución mensual / por partida 2024** — confirma el hallazgo de FASE 1: **no existe visor público**; solo la ejecución anual agregada de la Rendición.
- **Modificaciones presupuestarias 2024** — sin sección dedicada; rastreables solo caso por caso por ordenanzas.

---

## Tabla de fuentes del ciclo

| ID | Documento | Fuente | Año | Formato | Contenido | Estado |
|----|-----------|--------|-----|---------|-----------|--------|
| P01 | Presupuesto aprobado 2024 (por programa/dependencia/objeto/ingresos) | asuncion.gov.py/presupuesto | 2024 | PDF | asignación | **NO ENCONTRADO** (solo 2025; /presupuesto-2024 = 404) |
| P02 | Ordenanza de aprobación del presupuesto 2024 | JMA (`201.217.34.206:3000`) | 2024 | PDF | autorización | **NO VERIFICADO** (SPA; requiere consulta manual/pedido) |
| P03 | ORD 156/24 — Reprogramación de gastos del presupuesto 2024 | https://www.asuncion.gov.py/wp-content/uploads/2024/11/Ord_156.24.pdf | 2024 | PDF | modificaciones | ✅ Disponible |
| P04 | ORD 107/23 + ORD 128/24 — General de Tributos / base de ingresos 2024 | asuncion.gov.py/ordenanzas | 2024 | PDF | ingresos | ✅ Disponible |
| P05 | Rendición de Cuentas 2024 (ejecución del gasto) | https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf | 2024 | PDF | vigente/obligado/% | ✅ **Disponible (fuente central)** |
| P06 | Ejecución presupuestaria mensual / por partida 2024 | asuncion.gov.py | 2024 | — | obligado/pagado/mes | **NO ENCONTRADO** (brecha FASE 1) |
| P07 | Héssaka — salarios mensuales 2024 (12 PDFs) | asuncion.gov.py/hesaka | 2024 | PDF | personal | ⚠️ Disponible en URL, **texto no extraíble** (OCR/ingeniería) |
| P08 | Transferencias del Estado a la Muni (MEF, RUC+año) | servicios.mef.gov.py/consultas-publicas/muni.html | 2024 | Web→Excel/PDF | transferencias | ⚠️ Disponible (requiere RUC + captcha) |
| P09 | Contrataciones DNCP 2024 (SICP 108) | contrataciones.gov.py/.../ocds/2024/masivo.zip | 2024 | CSV/OCDS | contratos/obras | ✅ Disponible (pipeline existente) |

---

## Ficha de evidencia por fuente

### P01 · Presupuesto aprobado 2024 — NO ENCONTRADO
- **URL verificada:** `https://www.asuncion.gov.py/presupuesto` → solo publica el **presupuesto 2025** (plurianual 2025-2027, por Dependencia, de Ingresos, por Programa — PDFs bajo `/wp-content/uploads/2025/08/`).
- `https://www.asuncion.gov.py/presupuesto-2024` → **HTTP 404**.
- El patrón confirma que el sitio retiene **solo el año vigente**. No hay histórico del presupuesto aprobado 2024.
- **Vía posible:** pedido de acceso a información pública (Ley 5282/14), archivo municipal, o Wayback Machine.

### P02 · Ordenanza de aprobación del presupuesto 2024 — NO VERIFICADO
- El listado municipal de ordenanzas (periodo 2021-2026) **no publica** la ordenanza que aprueba los gastos del presupuesto 2024.
- El buscador oficial de la Junta Municipal (`http://201.217.34.206:3000/`) es la vía esperada, pero es **SPA sin HTML estático** → no verificable por fetch. Requiere consulta manual o pedido formal.

### P03 · ORD 156/24 (reprogramación) — DISPONIBLE
- URL: `https://www.asuncion.gov.py/wp-content/uploads/2024/11/Ord_156.24.pdf`
- Confirma que el presupuesto 2024 **fue modificado** en el propio ejercicio (reprogramación de gastos).

### P04 · Base de ingresos 2024 — DISPONIBLE
- ORD 107/23 (General de Tributos 2024) + ORD 128/24 (la modifica). Definen la previsión de ingresos del ejercicio.

### P05 · Rendición de Cuentas 2024 — DISPONIBLE (fuente central de ejecución)
- **URL completa:** `https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf` (también versión comprimida).
- **Contenido verificado (18 págs. comprimidas):**
  - Tabla "EJECUCIÓN DEL PRESUPUESTO DE GASTOS — Por Niveles del Objeto del Gasto": **PRESUPUESTO VIGENTE vs OBLIGADO ENE-DIC vs % EJEC**:
    - Servicios Personales: 788.089 / 727.234 /* — 92%
    - Servicios No Personales: 232.517 / 114.346 /* — 49%
    - Bienes de Consumo e Insumos: 205.890 / 79.754 /* — 39%
    - Inversión Física: 840.990 / 104.964 /* — 12%
    - Servicio de la Deuda Pública: 134.231 / 134.231 /* — 100%
    - Otros Gastos: 24.179 / 5.301 /* — 22%
    - **TOTAL GENERAL: 2.360.168 / 1.253.270 — 53%**
  - Ingresos recaudados 2024: TOTAL GENERAL **1.113.156** MGs.
  - Incluye sección de obras (inversión física).
- **No incluye:** pagado, ni desglose mensual, ni por partida.
- Respaldada por audiencia pública (Res. 185/2025, 01-ago-2025).

### P06 · Ejecución mensual/por partida 2024 — NO ENCONTRADO
- Confirma FASE 1: no hay visor público de ejecución del gasto. `/presupuesto` solo muestra el aprobado vigente. La única ejecución pública 2024 es la **anual agregada** de la Rendición (P05).

### P07 · Hesakã 2024 — DISPONIBLE EN URL, PERO TEXTO NO EXTRAÍBLE (requiere OCR/ingeniería)
- 12 PDFs mensuales enero-diciembre 2024 en `/hesaka`:
  - `Enero_2024.pdf`, `Febrero_2024-1.pdf`, `Marzo_2024.pdf`, `Abril_2024.pdf`, `Mayo_2024-1.pdf`, `Junio_2024.pdf`, `Julio_2024.pdf`, `Agosto_2024.pdf`, `Setiembre_2024.pdf`, `Octubre_2024.pdf`, `Noviembre_2024.pdf`, `Diciembre_2024.pdf`.
- Patrón de URL: `/wp-content/uploads/AAAA/MM/<Mes>_AAAA.pdf` (variaciones de nombre, sufijos `-1`).
- **BARRERA VERIFICADA (27-08-2026):** el PDF de Hesakã (muestra Enero_2024, 402 págs) tiene **texto no extraíble real** — `get_text()` devuelve ~8.000 caracteres/página pero **0 alfanuméricos** (fuente TrueType con byte-map corrupto `EPRQUE+TimesNewRoman...Set2`; **0 imágenes**, no es escaneado). Extraer salarios requiere **instalar tesseract + OCR** (~4.800 páginas/año) o reconstruir el CMap. Ver `docs/presupuesto/NOTA-tecnica-hesaka-texto-no-extraible.md`. Se corrige una afirmación previa de "texto extraíble" (falsa).
- **Alternativa:** la partida 100 Servicios Personales de la ejecución 2024 (P05) da el **monto agregado de personal** (788.089 vigente / 727.234 obligado / 92%) sin necesidad de Hesakã.

### P08 · MEF transferencias 2024 — DISPONIBLE CON LIMITACIÓN
- URL: `https://servicios.mef.gov.py/consultas-publicas/muni.html`
- Consulta por **RUC + Año** (2024 cubierto; datos desde 2017), resultados con exportación **Excel/PDF**.
- Limitaciones: el RUC de la Muni no aparece en la página de entrada (referencia conocida: **80011871-6**, a confirmar en el panel); hay captcha de refresco → la extracción requiere interacción (no es descarga directa).

### P09 · Contrataciones DNCP 2024 — DISPONIBLE (pipeline existente)
- `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/2024/masivo.zip` → **200 OK, ~236 MB**.
- `awa-masivo.zip` (~75 MB) y `con-masivo.zip` (~38 MB) también disponibles.
- El pipeline `dncp_contrataciones.py` procesa este año sin cambios: solo pasar `anio="2024"` (filtro SICP 108 / nombre ya implementado).

---

## Mapa del ciclo con las fuentes

```
PRESUPUESTO APROBADO 2024  →  (P01 NO encontrado / P02 no verificado)
        ↓
MODIFICACIONES             →  (P03 ORD 156/24 parcial; sin sección dedicada)
        ↓
PRESUPUESTO VIGENTE        →  (Solo está el total en P05 Rendición: 2.360.168 MGs)
        ↓
EJECUCIÓN (obligado)      →  (P05 Rendición: total obligado 1.253.270 MGs, por objeto)
        ↓
PAGOS / detalle mensual   →  (P06 NO existe en abierto)
        ↓
DESTINO                   →  Objeto del gasto (P05) + salarios (P07) + contratos (P09)
```

**Veredicto del ciclo:** reconstruible en sus **extremos** — presupuesto vigente y obligado **agregados** (P05), distribución por objeto del gasto (P05), personal (P07), contratos adquiridos (P09), transferencias recibidas (P08), modificaciones puntuales (P03). **No reconstruible:** el detalle por partida ni pagos mensuales (P01/P02/P06).

---

## Brechas y próximos pasos

### Brechas definitivas (sin inventar)
1. Presupuesto aprobado 2024 detallado (PDF) — no publicado; requiere archivo/pedido/Wayback.
2. Ordenanza de aprobación 2024 — requiere consulta manual JMA o pedido formal.
3. Ejecución mensual y por partida — no existe visor público.
4. Modificaciones 2024 — solo las rastreables por ordenanzas (P03 como muestra).

### Próximos pasos del módulo (según documento de contexto)
1. **Este inventario** sirve de mapa.
2. **Modelo de datos** (documento secciones 17-18): definir tabla `ejercicio, nivel, codigo, denominacion, presupuesto_inicial, modificacion, vigente, obligado, pagado, saldo, %ejecución, fuente`.
3. **Escala realista:** partir del que SÍ está disponible — **P05 Rendición 2024** (ejecución por objeto del gasto) + **P07 Hesakã 2024** (personal, sin OCR) + **P09 DNCP 2024** (contratos). Eso ya permite responder "¿qué se presupuestó/obligó y en qué?" a nivel agregado.
4. P08 (transferencias) requiere resolver RUC + interacción; P01/P02/P06 exigirían acceso a información o archivo.

> **Siguiente paso exacto del documento maestro:** con este inventario, definir el **modelo de datos del módulo presupuesto** y luego el pipeline por capas (manual primero).