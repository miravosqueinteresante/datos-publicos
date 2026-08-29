# Hallazgos de investigación: datos públicos de ANDE (Paraguay)

**Fuente investigada:** Administración Nacional de Electricidad (ANDE)
**Fecha de investigación:** 2026-08-29
**Método:** búsquedas web (`web_search`) con términos en español + verificación de URLs oficiales.
**Nota de cobertura:** las búsquedas dedicadas a "clientes" y "memoria anual" agotaron el
límite de tasa del proveedor de búsqueda (Exa). Se documentan aquí los hechos recuperados y
las fuentes oficiales donde deben publicarse los datos faltantes. Las secciones de
**Tarifas** y **Pérdidas** están bien respaldadas; **Clientes** queda parcialmente cubierta.

---

## 1. TARIFAS

### Dónde se publica
- **Sitio oficial de consulta:** `https://www.ande.gov.py/tarifas_vigentes.php`
  (página HTML con las tarifas vigentes; formato HTML, no es descarga de datos estructurados).
- **Pliego de Tarifas Nº 21 (documento base, PDF):** `https://www.ande.gov.py/docs/tarifas/PLIEGO21.pdf`
  y versiones actualizadas:
  - `https://www.ande.gov.py/docs/tarifas/Pliego%20de%20Tarifas%20Nro%2021%20Version%20Actualizada%2014-06-2023.pdf`
  - `https://www.ande.gov.py/docs/tarifas/1%20Pliego%20de%20Tarifas%20Nro%2021%20Version%20Actualizada%2028-12-2022.pdf`
- **Portal de Información Pública (espejo oficial):** `https://informacionpublica.paraguay.gov.py/public/785631-PLIEGO21pdf-PLIEGO21.pdf`
- **Resoluciones de Presidencia (PDFs, formato oficial de aprobación):** `https://www.ande.gov.py/docs/tarifas/`

### Formato y frecuencia
- **Formato:** PDF (Pliego y resoluciones) y HTML (página de tarifas vigentes). No existe API pública ni CSV.
- **Frecuencia:** Las tarifas se actualizan por **Resolución de Presidencia de la ANDE** (no hay
  calendario fijo). El marco general es el **Pliego de Tarifas Nº 21**, aprobado por
  Decreto Nº 6904/2017 y autorizado por Resolución Nº 38788 de fecha 16-03-2017. El Pliego puede
  modificarse por Resolución de Presidencia cuando lo exijan necesidades técnicas/administrativas.

### Categorías tarifarias y niveles de tensión (hechos del Pliego Nº 21)
Niveles de tensión normalizados (Pliego Nº 21, Cap. 3.3):
- Muy Alta Tensión (MAT): 220.000 V
- Alta Tensión (AT): 66.000 V
- Media Tensión (MT): 23.000 V
- Baja Tensión (BT): 380 V (trifásica) / 380/√3 V (monofásica)

Grupos de consumo y categorías (extracto verificado en el PDF del Pliego):
- **Baja Tensión (BT):**
  - 141 – Consumo Social (tarifa subsidiada, Ley Nº 3480/2008)
  - 142 – Consumo Residencial/Doméstico (Viviendas)
  - 410 – Grupo "Otros"
  - 343 – Grupo Industrial
  - 344 / 414 / 844 – categorías industriales/otros/gubernamentales en tarifa monómica por tramos (ver RP 49887)
  - Alumbrado Público
- **Media Tensión (MT, 23 kV):**
  - 371 – Binómica en Subestación (Potencia Reservada máx. 6.000 kW / mín. 2.000 kW)
  - 372 – Binómica en Línea (Potencia Reservada máx. 3.000 kW / mín. 40,1 kW)
  - 373 – Monómica en Línea (Potencia limitada 2,2 a 52,8 kW)
  - 412 – Otros en MT
  - 374 / 416 / 834 – categorías en tarifa monómica por tramos horarios (ver RP 49887)
  - 731 / 732 – Grupo de Consumo Diferencial (punta/fuera de punta)
- **Alta y Muy Alta Tensión:**
  - 640 – Alta Tensión (66 kV), subestación
  - 620 – Muy Alta Tensión (220 kV), subestación
  - 911 / 912 / 940 / 920 – Grupo de Consumo Intensivo Especial (GCIE, creado por RP 47191/2022)

### Precios (hechos, con cita)
**Residencial BT (Categoría 142), Pliego Nº 21 (precios en G/kWh, con IVA):**
- 0–50 kWh: 311,55 | 51–150 kWh: 349,89 | 151–300 kWh: 365,45
- 301–500 kWh: 403,82 | 501–1.000 kWh: 420,27 | >1.000 kWh: 435,51
(Fuente: PLIEGO21.pdf, sección 5.1.1.2)

**Consumo Social BT (Categoría 141), Ley Nº 3480/2008:** descuentos 75% (0–100 kWh),
50% (101–200 kWh), 25% (201–300 kWh) sobre la tarifa residencial.
(Fuente: PLIEGO21.pdf, sección 5.1.1.1)

**Tarifa monómica por tramos horarios (RP 49887/2024, opcional, en G/kWh):**
- Residencial BT (cat. 144): punta 669,17 / fuera de punta 263,88 (≤500 kWh);
  696,42 / 274,62 (501–1.000 kWh); 721,68 / 284,58 (>1.000 kWh)
- Industrial BT (344): 635,54 / 268,68
- Otros BT (414): 660,51 / 255,56
- Gubernamental BT (844): 589,49 / 269,16
- MT Industrial (374): 496,37 / 197,24 | MT Otros (416): 512,18 / 190,49 | MT Gub. (834): 439,36 / 211,52
(Fuente: `https://www.ande.gov.py/docs/tarifas/RP49887%20-%20Tarifas%20Monoomicas%20por%20tramos%20horarios%20-%20ID88556715_firma%20inici.._.pdf`)

**Alta/Muy Alta Tensión (binómica, Pliego Nº 21, G/kW-mes y G/kWh):**
- 66 kV (cat. 640): Potencia Reservada 34.761; Energía punta 245,8 / fuera de punta 169,5
- 220 kV (cat. 620): Potencia Reservada 31.033; Energía punta 232,4 / fuera de punta 165,4
(Fuente: PLIEGO21.pdf, sección 5.2.5)

**Grupo de Consumo Intensivo Especial (GCIE, RP 49238/2024, en USD):**
- 220 kV: energía punta 0,03725 / fuera punta 0,03105 USD/kWh; potencia reservada punta 5,27 USD/kW-mes
- 66 kV: energía punta 0,03765 / fuera 0,03132; potencia reservada punta 7,02
- 23 kV subestación: energía punta 0,03771 / fuera 0,03177; potencia reservada punta 8,00
- 23 kV línea: energía punta 0,04006 / fuera 0,03374; potencia reservada punta 10,84
(Fuente: `https://www.ande.gov.py/docs/tarifas/RP49238%20Actualizacion%20de%20las%20Tarifas%20de%20Energia%20Electrica%20GCIE-2024.pdf`)

### Resoluciones asociadas (hechos)
- **Decreto Nº 6904/2017** + **Resolución Nº 38788 (16-03-2017):** aprueban el Pliego Nº 21.
- **Ley Nº 3480/2008:** crea la Tarifa Social (subsidio residencial).
- **Ley Nº 7354/2024:** fija el horario oficial; deriva ajuste de horarios de punta/fuera de punta.
- **Resolución P/Nº 49887 (26-11-2024):** aprueba tarifas monómicas por tramos horarios en BT y MT.
- **Resolución P/Nº 49888 (2024):** modifica numerales 3.4, 3.5 y 4.11.1 e incluye 4.11.6 del Pliego Nº 21
  para adecuar horarios a la Ley 7354/2024.
- **Resolución P/Nº 47191 (05-12-2022):** crea el GCIE (data centers, minería de criptoactivos, etc.).
- **Resolución P/Nº 49238 (2024):** actualiza tarifas del GCIE; sustituye a RP 47191 y RP 47708/2023.
- **Decreto Nº 7824/2022:** medidas regulatorias temporales para consumo intensivo; vigencia hasta 2027.

---

## 2. CLIENTES

### Estado de la investigación
Las búsquedas específicas de "número de clientes / evolución histórica / clientes por categoría"
no retornaron resultados utilizables (límite de tasa del buscador). Lo documentado aquí son los
hechos parciales y las **fuentes oficiales donde este dato debe publicarse**.

### Hechos recuperados
- En 2025 se incorporaron **casi 28.000 familias** como nuevos clientes/conexiones (dato aparecido
  en nota de ANDE sobre pérdidas).
  (Fuente: `https://www.ande.gov.py/interna.php?id=15116`, oficial ANDE, 2026-03-18)
- La Memoria Anual / Balance de Gestión reporta la gestión comercial (morosidad, cambios de medidores,
  etc.) pero el número total de clientes no fue extraído en esta sesión.

### Dónde debería publicarse (fuentes oficiales identificadas)
- **Balance Anual de Gestión Pública (BAGP) ANDE 2025:** `https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf`
  (PDF oficial; contiene sección de gestión comercial con indicadores de clientes).
- **Memoria Anual de la ANDE** (publicada con rezago; citada por prensa para 2022, 2023, 2024).
- **Balance de Gestión Pública del MEF:** `https://www.mef.gov.py/sites/default/files/2024-12/25%2002%20Administraci%C3%B3n%20Nacional%20de%20Electricidad.PDF`
- **Portal de Información Pública:** `https://informacionpublica.paraguay.gov.py/` (permite buscar
  memorias y resoluciones de ANDE).

### Formato y frecuencia
- **Formato:** PDF (Memoria/BAGP). No se identificó CSV ni API de clientes.
- **Frecuencia:** anual (Memoria/BAGP), con rezago de publicación (la Memoria 2024 se conoció a fines de 2025).

### Pendiente
> Repetir la búsqueda "ANDE cantidad de clientes por año categoría" cuando el buscador esté
> disponible, y extraer del BAGP 2025 / Memoria Anual las series de total de clientes y desglose
> por categoría (residencial, industrial, gubernamental, otros).

---

## 3. PÉRDIDAS

### Dónde se publica
- **Balance Anual de Gestión Pública (BAGP) ANDE 2025:** `https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf` (oficial)
- **Plan Maestro de Reducción de Pérdidas 2025:** `https://www.ande.gov.py/documentos/plan_maestro/Plan%20de%20Reduccion%20de%20Perdidas%202025.pdf` (oficial)
- **Nota oficial ANDE (marzo 2026):** `https://www.ande.gov.py/interna.php?id=15116` (oficial)
- **MEF – Balance de Gestión:** `https://www.mef.gov.py/sites/default/files/2024-12/25%2002%20Administraci%C3%B3n%20Nacional%20de%20Electricidad.PDF` (oficial)
- **Prensa (terceros, útiles como contexto/cita secundaria):**
  - ABC Color: `https://www.abc.com.py/economia/2025/09/30/perdidas-electricas-costaron-a-la-ande-casi-us-350-millones/` (sobre Memoria 2024)
  - ABC Color: `https://www.abc.com.py/economia/2023/07/05/ande-perdio-27-mwh-por-cada-100-que-inyecto-al-sistema-electrico-nacional/` (sobre Memoria 2022)
  - La Nación: `https://www.lanacion.com.py/negocios/2026/03/19/ande-logro-una-reduccion-del-4-en-perdidas-electricas/`
  - BNamericas: `https://www.bnamericas.com/es/noticias/con-acciones-estrategicas-e-innovacion-tecnologica-ande-ha-logrado-una-importante-reduccion-de-sus-perdidas-electricas-en-los-ultimos-dos-anos`

### Formato y frecuencia
- **Formato:** PDF (BAGP, Plan Maestro) y HTML (notas de prensa). No hay CSV/API.
- **Frecuencia:** reporte **mensual y en "año móvil" (últimos 12 meses)** para el indicador de
  pérdidas; planificación y metas en documentos anuales/plurianuales.

### Hechos (con cita)
**Definición oficial:** pérdidas eléctricas = diferencia entre energía disponible para el sistema y
energía facturada; se dividen en **técnicas** y **no técnicas** (hurto/fraude).
(Fuente: Memoria ANDE vía ABC Color 2023-07-05)

**Pérdidas totales (transmisión + distribución), año móvil:**
- Diciembre 2025: **24,40%** (bajó 0,22 pp vs. 24,62% en nov-2025). Pérdida mensual dic-2025: 23,93%.
- Evolución: 28,5% en 2023 → 24,5% en 2025.
(Fuente: BAGP 2025 y `interna.php?id=15116`, oficial ANDE)

**Pérdidas en distribución (año móvil):**
- Diciembre 2025: **20,03%** (bajó 0,38 pp vs. 20,41% en nov-2025).
- Evolución: 23,4% en 2023 → 20,03% en 2025.
- Meta Plan Maestro 2025: 21,3% → se superó (20,03%).
(Fuente: BAGP 2025; Plan Maestro Pérdidas 2025; `interna.php?id=15116`)

**Pérdidas en transmisión:**
- Diciembre 2025: **4,37%** (subió 0,16 pp vs. 4,21% en nov-2025; efecto estacional/técnico Joule).
(Fuente: BAGP 2025)

**Composición técnica vs no técnica (estimación CEARE–BID, oct-2024):**
- Pérdidas Técnicas en Transmisión: **5,1%** del total.
- Pérdidas en Distribución: **23,4%** del total, estimado en **50% técnicas / 50% no técnicas**
  (≈11,7% técnicas en distribución y ≈11,7% no técnicas/comerciales).
(Fuente: Plan Maestro de Reducción de Pérdidas 2025, citando estudio CEARE–BID)

**Volúmenes absolutos (Memoria 2024, vía ABC Color 2025-09-30):**
- Energía entregada al mercado nacional: 26.153.605 MWh
- Pérdidas en transmisión: 1.207.698 MWh
- Pérdidas en distribución: 5.725.885 MWh
- Total pérdidas 2024: ≈6,93 millones MWh (≈US$ 341 millones a tarifa media 49,19 USD/MWh)
(Fuente: Memoria Anual 2024 de ANDE, citada por ABC Color — tercero, pero dato primario de ANDE)

**Metas de reducción (Plan Maestro 2025–2028):** bajar pérdidas en distribución de 23,4% a 15%
(2025: 21,3%; 2026: 19,2%; 2027: 17,1%; 2028: 15,0%).
(Fuente: Plan Maestro de Reducción de Pérdidas 2025, oficial)

---

## Resumen de fuentes oficiales vs terceros

| Tema | Fuente oficial | URL | Formato |
|------|---------------|-----|---------|
| Tarifas | ANDE – tarifas_vigentes | ande.gov.py/tarifas_vigentes.php | HTML |
| Tarifas | ANDE – Pliego Nº 21 y resoluciones | ande.gov.py/docs/tarifas/ | PDF |
| Tarifas | Portal Info. Pública | informacionpublica.paraguay.gov.py | PDF |
| Clientes | ANDE – BAGP 2025 | ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf | PDF |
| Clientes | MEF – Balance Gestión | mef.gov.py/.../Administracion%20Nacional%20de%20Electricidad.PDF | PDF |
| Pérdidas | ANDE – BAGP 2025 | ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf | PDF |
| Pérdidas | ANDE – Plan Maestro Pérdidas | ande.gov.py/documentos/plan_maestro/... | PDF |
| Pérdidas | ANDE – nota oficial | ande.gov.py/interna.php?id=15116 | HTML |
| Pérdidas (contexto) | ABC Color / La Nación / BNamericas | ver sección 3 | HTML (terceros) |

**Conclusión de trazabilidad:** Tarifas y Pérdidas tienen fuentes oficiales directas y citables
(URLs arriba). Clientes quedó sin serie numérica extraída en esta sesión por límite del buscador;
las fuentes oficiales donde debe estar (BAGP 2025, Memoria Anual, MEF) están identificadas para
una siguiente pasada.
