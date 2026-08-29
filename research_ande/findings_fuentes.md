# Hallazgos: Fuentes y canales oficiales de datos públicos de ANDE (Paraguay)

Investigación realizada el 29/08/2026 mediante búsqueda web (5 búsquedas).
Objetivo: mapear dónde la Administración Nacional de Electricidad (ANDE) y
organismos vinculados publican datos públicos sobre electricidad en Paraguay.

---

## 1. Sitio web institucional de ANDE

**URL base:** https://www.ande.gov.py/

Portal corporativo con secciones de servicios, noticias y transparencia. No
expone una sección de "datos abiertos" como tal, pero sí publica documentos
contables y memorias.

- Sección de estados contables / Memoria y Balance:
  https://www.ande.gov.py/contables.php?cat=5
  (filtro por año 2020-2026; el listado se carga dinámicamente)
- Memoria Anual 2024 (PDF directo):
  https://www.ande.gov.py/finanzas/ANDE%20-%20Memoria%20Anual%202024.pdf
- Memoria Anual 2020 (referenciada en literatura):
  https://www.ande.gov.py/documentos_contables/746/ande_-_memoria_2020.pdf
- Compilación Estadística 1996-2016 (PDF):
  https://www.ande.gov.py/documentos_contables/532/compilacion_estadistica_1996-2016.pdf
- Compilación Estadística 2000-2020 (PDF, citada en BID):
  https://www.ande.gov.py/documentos_contables/747/ande_-_compilacion_estadistica_2000-2020.pdf
- MECIP (control interno / transparencia): https://mecip.ande.gov.py/
- Gestión y Control (sistema interno): https://gestion.ande.gov.py:8580/control/
- App "Mi ANDE" y servicios online para reclamos, facturas, aporte de lectura.

**Tipo de datos:** Memorias anuales (gestión técnica, comercial, financiera),
compilaciones estadísticas históricas del sector eléctrico, estados contables.
Formato: PDF (no hay API ni descarga de series en CSV/JSON).

**Hecho clave:** La "Compilación Estadística" es la fuente primaria de series de
demanda, generación, clientes y cobertura eléctrica de ANDE (períodos 1990-2020
y 1996-2016). La Memoria Anual contiene cuadros de energía facturada por grupo
de consumo, generación por central, e indicadores operativos.

---

## 2. Viceministerio de Minas y Energía (VMME - MOPC)

**URL base:** https://minasyenergia.mopc.gov.py/

Es el organismo rector de las estadísticas energéticas nacionales (delega la
DGEEC la elaboración del Balance Energético Nacional). Publica el **Balance
Energético Nacional (BEN)** en PDF, anual.

- Balance Energético Nacional 2024 (PDF):
  https://minasyenergia.mopc.gov.py/pdf/balance2024/BEN%202024_Paraguay.pdf
- Balance Energético Nacional 2023 (PDF analítico):
  https://minasyenergia.mopc.gov.py/pdf/balance2023/BEN%202023_Analitico%20VF.pdf

**Tipo de datos:** Oferta y consumo final de energía, balances en términos
físicos, precios de energéticos, capacidades, intensidad energética, cobertura
eléctrica. Metodología siePARAGUAY, alineada a estándares internacionales
(OLADE, IEA). Incluye datos de electricidad (ANDE, Itaipú, Yacyretá, Acaray),
biomasa, hidrocarburos, ERNC.

**Hecho clave (cita del BEN 2024):** "el presente informe [...] constituye una
reseña y resumen estadístico del Balance Energético Nacional en términos de
energía final 2024 (BEN 2024), que regularmente publica el Viceministerio de
Minas y Energía del Ministerio de Obras Públicas y Comunicaciones (VMME-MOPC)."

El Comité de Estadística Energética (CEE-SIEN) reúne a ANDE, BCP, Yacyretá,
Itaipú, INFONA, INE, PETROPAR, INTN, MADES, MIC, entre otros.

---

## 3. Instituto Nacional de Estadística (INE) - Inventario de Operaciones Estadísticas (IOE)

**URL base:** https://www.ine.gov.py/
**IOE (Inventario de Operaciones Estadísticas):** https://ioe.ine.gov.py/

El INE consolida las operaciones estadísticas de los organismos públicos del
SISEN, incluida la ANDE. Permite localizar qué estadísticas produce ANDE y bajo
qué responsabilidad.

**Hecho clave (cita INE, noticia 23-12-2024):** "El IOE 2023 recolectó 220
Operaciones Estadísticas a diciembre de 2024 [...] Entre los organismos que
respondieron figura la Administración Nacional de Electricidad (ANDE)."

**Tipo de datos:** Catálogo/índice de metadatos de operaciones estadísticas
(incluye las de ANDE), no las series en sí.

---

## 4. Portales nacionales de transparencia y datos abiertos (Paraguay)

- Portal Único de Información Pública:
  http://informacionpublica.paraguay.gov.py/portal/#!/buscar_informacion
- Portal nacional de Datos Abiertos: https://www.datos.gov.py/
- Rindiendo Cuentas: https://www.rindiendocuentas.gov.py/

**Tipo de datos:** Transparencia y solicitudes de información pública. ANDE
publica guías internas y documentos en el portal de información pública, por
ejemplo:
https://informacionpublica.paraguay.gov.py/public/6767220-GUIAINTERNAMAYO2021pdf-GUIAINTERNAMAYO2021.pdf

Nota: no se encontró un portal de "datos abiertos" dedicado exclusivamente a
energía/ANDE; los datos energéticos centralizados están en el VMME (BEN).

---

## 5. Fuentes secundarias / de contexto (NO primarias, útiles como citas)

- **BID - Breve reseña del sector de energía en Paraguay (2022):**
  https://publications.iadb.org/publications/spanish/document/Breve-resena-del-sector-de-energia-en-Paraguay.pdf
  Citas útiles: "ANDE divide el SIN por regiones en seis subsistemas:
  metropolitano, central, sur, norte, este y oeste"; "la ANDE tiene un cuasi
  monopolio del mercado eléctrico". Gráficos basados en Compilación Estadística
  y Memoria Anual de ANDE.
- **Noticias de demanda/récords (datos coyunturales):** El Nacional
  (https://elnacional.com.py/economia/ande-registro-nuevo-record-historico-consumo-sistema-electrico-paraguayo-n99876),
  La Nación (https://www.lanacion.com.py/negocios_edicion_impresa/2026/04/11/ande-registra-aumento-sostenido-del-consumo-electrico),
  MarketData (https://marketdata.com.py/noticias/paraguay-alcanza-nuevo-record-de-demanda-y-suministro-de-energia-149167).
  Reportan demanda de potencia instantánea del SIN (p. ej. récord de 5.752 MW
  el 27/01/2026), aportes de Itaipú/Yacyretá/Acaray, consumo en MWh.

---

## Resumen de canales por tipo de dato

| Tipo de dato | Fuente principal | Formato | URL |
|---|---|---|---|
| Memoria anual / estados contables | ANDE (contables.php) | PDF | https://www.ande.gov.py/contables.php?cat=5 |
| Series históricas sector eléctrico (demanda, generación, clientes, cobertura) | ANDE - Compilación Estadística | PDF | ande.gov.py/documentos_contables |
| Balance energético nacional (oferta/consumo, precios, ERNC) | VMME-MOPC | PDF | minasyenergia.mopc.gov.py/pdf/balance2024 |
| Catálogo de operaciones estadísticas (metadatos) | INE - IOE | Web | https://ioe.ine.gov.py/ |
| Transparencia / solicitud de información | Portal Info. Pública / datos.gov.py | Web | informacionpublica.paraguay.gov.py |

---

## Brechas detectadas (para el conector ANDE)

- No existe API pública de ANDE ni del VMME (datos solo en PDF).
- Las compilaciones estadísticas y memorias son PDF (requieren extracción;
  ver principio del proyecto: extraer solo lo necesario conservando referencia).
- El BEN es anual y se publica con retraso (BEN 2024 cerró al 31/07/2025).
- No hay series de demanda en tiempo real abiertas; los récords de potencia
  solo se publican vía notas de prensa/ANDE.
- ANDE no aparece con portal de datos abiertos propio; su presencia en
  datos.gov.py / IOE es a nivel de metadatos, no de descarga de series.
