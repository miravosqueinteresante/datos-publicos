# Hallazgos: indicadores de demanda, consumo y generación/abastecimiento de ANDE (Paraguay)

Fecha de investigación: 2026-08-29
Fuente de búsqueda: web_search (5 consultas en español)
Alcance: distinguishing lo que publica ANDE de lo que publican terceros.

---

## 1. Resumen ejecutivo

ANDE publica indicadores de electricidad en tres canales oficiales:

1. **Memoria Anual** (PDF): el documento oficial completo. Incluye demanda máxima de potencia, consumo de energía del SIN, factor de carga, pérdidas, energía facturada por grupo de consumo, generación/compra por central, evolución anual.
2. **Resumen Estadístico** (PDF): extracto tabulado de varios años (ej. 2020-2024).
3. **Página web `generacion.php`** (HTML): gráfico histórico "cuadro de oferta y demanda" del SIN y fichas de capacidad de Itaipú, Yacyretá y Acaray.

ANDE **no expone API ni descargas CSV** en los canales encontrados; todo es PDF o HTML. Los datos mensuales y los despachos de noticias los difunde ANDE vía notas de prensa en `ande.gov.py` y, secundariamente, medios que citan a ANDE (MarketData, ABC Color, Última Hora, OviedoPress).

El **Viceministerio de Minas y Energía (VMME/MOPC)** publica los Balances de Energía anuales (tercera fuente, no ANDE) y el BID compiló una "Breve reseña del sector de energía en Paraguay" basada en ANDE.

---

## 2. Indicadores y dónde se publican

### 2.1 Demanda máxima de potencia (SIN)

- **Qué es:** pico de potencia del Sistema Interconectado Nacional, en MW.
- **Dónde lo publica ANDE:** Memoria Anual (tabla "Demanda Máxima de Potencia del SIN", gráfico histórico) y notas de prensa al batir récords.
- **Formato:** PDF (Memoria) y HTML (notas).
- **Frecuencia:** anual en Memoria; récords comunicados puntualmente por prensa.
- **Serie histórica:** sí, en Memoria Anual y en el gráfico de `generacion.php`.

Valores verificados (fuente ANDE / citas de prensa que reproducen ANDE):

| Año | Demanda máxima (MW) | Fuente / cita |
|-----|---------------------|---------------|
| 2019 | 3.553 | Memoria Anual 2019 (ANDE) |
| 2020 | ~3.563 | BID, "Breve reseña...", Gráfico 4, nota ANDE 2020 |
| 2022 | 4.270 (9 dic, récord entonces) | ABC Color 2022-12-10, cita ANDE |
| 2024 | superó proyección; ~4.195 proyectado | UIP vía RCC 2025-04-21 |
| 2025 | **5.280** (15 dic, récord histórico) | ANDE, nota "EL CONSUMO ELÉCTRICO NACIONAL CRECIÓ 12,5 % EN 2025" (interna.php?id=14877) |

Cita oficial 2025 (ANDE, interna.php?id=14877): *"la demanda máxima histórica del Sistema Interconectado Nacional (SIN) del 2025 fue de 5.280 MW, registrado el 15 de diciembre"*.

### 2.2 Consumo total / energía demandada (SIN)

- **Qué es:** energía consumida en el SIN, en GWh (o MWh en Memorias). Incluye pérdidas según definición de ANDE ("consumo bruto = consumo final + pérdidas").
- **Dónde lo publica ANDE:** Memoria Anual (tabla "Consumo de Energía Eléctrica (MWh/año)"), Resumen Estadístico, y notas de prensa anuales de crecimiento.
- **Formato:** PDF y HTML.
- **Frecuencia:** anual (Memoria + Resumen); seguimiento mensual difundido en notas de prensa.
- **Serie histórica:** sí.

Valores verificados (ANDE / citas):

| Año | Consumo total (GWh/MWh) | Crecimiento | Fuente |
|-----|-------------------------|-------------|--------|
| 2021 | 18.583 GWh | — | ANDE vía MarketData |
| 2022 | 19.635,952 MWh (≈19.636 GWh) | +5,7% | ABC Color / Memoria 2023 |
| 2023 | 22.079.861 MWh (≈22.080 GWh) | +12,45% | Memoria 2023 (ANDE) |
| 2024 | 26.154 GWh | +18,5% | ANDE vía MarketData / UIP |
| 2025 | **29.419 GWh** | +12,5% | ANDE, interna.php?id=14877 |

Cita oficial 2025 (ANDE): *"Durante el año, el consumo total llegó a 29.419 GWh"*.

**Consumo mensual / acumulado 2026** (ANDE vía OviedoPress, 2026-06-24): enero-mayo 2026 = 14.587,1 GWh (+19,4% vs mismo periodo 2025); solo mayo 2026 = 2.382,8 GWh (+11,9% vs mayo 2025). Esto confirma que ANDE difunde desagregación mensual vía prensa, aunque no en un dataset descargable.

### 2.3 Consumo por categoría (grupo de consumo)

- **Qué es:** energía facturada desagregada por grupo tarifario.
- **Dónde lo publica ANDE:** Memoria Anual, sección de "Energía Facturada por Grupo de Consumo" (tablas y gráficos).
- **Formato:** PDF.
- **Frecuencia:** anual.
- **Serie histórica:** sí (por año en Memorias).
- **Nota de clasificación:** desde el Pliego de Tarifas N° 21 (2017) desapareció "Comercial" y se crearon grupos: Residencial, Otros, Diferencial, Alta Tensión, Muy Alta Tensión, Electrointensivas, Gubernamental, Alumbrado Público, Industrial.

Distribución 2020 (ANDE, Memoria/Compilación, citada por BID "Breve reseña"):
- Residencial 48%
- Otros 38%
- Alta Tensión 5%
- Industrial 3%
- Gubernamental 3%
- Alumbrado Público 2%
- Diferencial 1%
- Electrointensivas 1%
- Muy Alta Tensión 1%

Cita (BID, compilando ANDE Memoria 2019-2020): *"En 2020, el consumo de los demás clientes por grupo se desagregaba en otros 38%, y el resto se distribuye entre clientes diferenciales industriales, alta/muy alta tensión, electro intensivas; gubernamentales y alumbrado público, todos estos en total 15%."*

### 2.4 Generación / abastecimiento por central (Itaipú, Yacyretá, Acaray)

- **Dónde lo publica ANDE:**
  - `generacion.php` (HTML): fichas de capacidad de Itaipú (7.000 MW PY), Yacyretá (1.600 MW PY), Acaray (200/210 MW), térmicas del Chaco; gráfico "oferta y demanda".
  - Memoria Anual: origen de la energía (Energía Comprada Itaipú+Yacyretá vs Energía Generada Acaray+Térmicas), destino (Consumo Nacional / Exportación).
  - Notas de prensa anuales con el aporte por central al consumo.
- **Formato:** HTML y PDF.
- **Frecuencia:** anual; reporte mensual de producción y suministro de Itaipú (Dirección Técnica Margen Derecha) citado por la prensa.
- **Serie histórica:** sí (Memoria y Resumen Estadístico).

Aporte al consumo 2025 (ANDE, interna.php?id=14877):
- Itaipú Binacional: 25.768 GWh (87,6%)
- Yacyretá: 3.081 GWh (10,5%)
- Acaray: 570 GWh (1,9%)

Cita oficial: *"abastecido principalmente por las centrales hidroeléctricas, distribuidos de la siguiente manera: Itaipú Binacional: 25.768 GWh (87,6 %). Yacyretá: 3.081 GWh (10,5 %). Central Hidroeléctrica Acaray: 570 GWh (1,9 %)"*.

Generación total de Itaipú 2025 (MarketData, citando informe mensual Dirección Técnica Margen Derecha): 72.879 GWh (+8,6% vs 2024); suministro a ANDE solo en diciembre 2.610 GWh (mayor mensual histórico). Esto es generación total de la central (parte paraguaya + brasileña), no solo la porción paraguaya.

Capacidades instaladas (ANDE, `generacion.php`): Itaipú 7.000 MW para PY; Yacyretá 1.600 MW para PY; Acaray 200/210 MW (4 generadores de 50 MW); térmicas Chaco ~6,1 MW en conjunto (Bahía Negra, Fuerte Olimpo, Pedro J. Caballero, Salto del Guairá).

### 2.5 Evolución mensual y anual

- **Anual:** Memoria Anual, Resumen Estadístico y gráfico de `generacion.php` (serie histórica oferta/demanda).
- **Mensual:** ANDE difunde variaciones mensuales y acumulados por prensa (ej. OviedoPress enero-mayo 2026). El "informe mensual de producción y suministro de energía" de la Dirección Técnica Margen Derecha de Itaipú es la fuente primaria citada de los desgloses mensuales de generación, pero no está en un repositorio CSV/API abierto visible.
- **No se encontró** un endpoint de datos abiertos (API/CSV) de ANDE para series mensuales; los datos mensuales circulan como cifras en notas de prensa.

---

## 3. URLs clave (ANDE oficial)

- Nota de prensa 2025 (consumo + demanda máxima + abastecimiento por central):
  https://www.ande.gov.py/interna.php?id=14877
- Página Generación (oferta/demanda histórica + fichas de centrales):
  https://www.ande.gov.py/generacion.php
- Resumen Estadístico 2020-2024 (PDF):
  https://www.ande.gov.py/finanzas/ANDE%20-%20Resumen%20Estad%C3%ADstico%202020%20-%202024.pdf
- Memoria Anual 2019 (PDF, con tablas de demanda máxima, consumo, grupos de consumo, pérdidas):
  https://www.ande.gov.py/documentos_contables/705/ande_-_memoria_anual_2019.pdf
- Memoria Anual 2020 (PDF):
  https://www.ande.gov.py/documentos_contables/746/ande_-_memoria_2020.pdf
- Compilación Estadística 2000-2020 (PDF, serie larga):
  https://www.ande.gov.py/documentos_contables/747/ande_-_compilacion_estadistica_2000-2020.pdf

---

## 4. Fuentes de terceros (NO ANDE) — para contextualizar, no como fuente primaria

- **Viceministerio de Minas y Energías (VMME/MOPC)** — Balances de Energía anuales (estadísticas energéticas del país); página "Electricidad - Generación":
  https://minasyenergia.mopc.gov.py/index.php?Itemid=603&id=1216&option=com_content&view=article
  Anexo de proyección de demanda ANDE 2019-2030:
  https://minasyenergia.mopc.gov.py/pdf/actualizacionenergeticos/2021/Estudio%20de%20Demanda%20VMME%20ANDE/Anexo-ANDE-MercElecNac-Proy2019-2030.pdf
- **BID** — "Breve reseña del sector de energía en Paraguay" (2022), compila Memorias y Compilación Estadística de ANDE:
  https://publications.iadb.org/publications/spanish/document/Breve-resena-del-sector-de-energia-en-Paraguay.pdf
- **Prensa que cita a ANDE** (usar solo como confirmación de cifras oficiales): MarketData (marketdata.com.py), ABC Color (abc.com.py), Última Hora (ultimahora.com), OviedoPress (oviedopress.com).

---

## 5. Brechas / limitaciones de la fuente

- ANDE no ofrece API ni CSV descargable de ninguno de estos indicadores en los canales revisados; los datos deben extraerse de PDF (Memoria/Resumen) o HTML (notas, gráfico).
- El gráfico "oferta y demanda" de `generacion.php` es una imagen/gráfico interactivo sin descarga de datos crudos evidente.
- La desagregación mensual solo aparece como cifras sueltas en notas de prensa, no como serie estructurada.
- No se verificó acceso directo al "informe mensual de producción y suministro de energía" de Itaipú (fuente citada por MarketData); queda como brecha de trazabilidad para la frecuencia mensual.

---

## 6. Conclusión para el conector ANDE

Los indicadores solicitados (demanda máxima, energía demandada/consumo total, consumo por categoría, generación Itaipú/Yacyretá/Acaray, evolución mensual y anual) **sí los publica ANDE**, principalmente en PDF anual (Memoria y Resumen Estadístico) y en HTML (notas de prensa y página de generación). La serie histórica existe pero está fragmentada en PDFs por año; no hay API/CSV. El conector debe extraer de PDF/HTML conservando la procedencia (URL + fecha de obtención), siguiendo la regla del proyecto de trazabilidad.
