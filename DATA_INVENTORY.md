# DATA_INVENTORY.md — Inventario de Datos de la Municipalidad de Asunción

> **Fecha de investigación:** 26 de agosto de 2026
> **Método:** navegación directa y fetch de fuentes oficiales (asuncion.gov.py, jma.gov.py, contrataciones.gov.py, mef.gov.py, datos.gov.py, ine.gov.py, mopc.gov.py). Estado de la investigación para FASE 1.
> **Nota de trazabilidad:** cada fuente indica su URL y su fecha de verificación. Lo marcado como **[no verificado]** no fue comprobado en esta pasada y debe validarse antes de usarse. Base heredada de la investigación de muchotexto.net (research_ordenanzas_asuncion, 11-ago-2026), re-verificada el 26-ago-2026.

---

## Resumen ejecutivo

**La Municipalidad de Asunción publica datos reales de transparencia, pero casi todo es PDF o Google Drive.** No existe una sección de datos abiertos con datasets estructurados (CSV/JSON/API) en el sitio municipal. Las fuentes estructuradas y automatizables del dominio de Asunción viven en **portales nacionales**: la nómina salarial (datos.gov.py / datos.sfp.gov.py, API DKAN), las licitaciones y contratos (DNCP, API V3 OCDS + datasets CSV) y las transferencias a municipios (MEF). La cartografía de Asunción es la fuente geoespacial más automatizable (INE Cartografía Censal 2022).

**Las 5 fuentes más prometedoras** (para FASE 2/3):
1. **Hesakã — salarios mensuales** (asuncion.gov.py/hesaka): 60+ PDFs 2021→jul 2026, URLs predecibles, alta automatización.
2. **DNCP — contrataciones y contratos de la Muni**: API V3 OCDS + datasets CSV (CC BY 4.0), cubre licitaciones/adjudicaciones/contratos/proveedores.
3. **datos.gov.py — Nómina de Funcionarios**: dataset estructurado con API DKAN, incluye municipios (granularidad municipal a confirmar).
4. **MEF — Transferencias a municipios** (servicios.mef.gov.py/consultas-publicas/muni.html): exportable a Excel, desde 2017.
5. **INE — Cartografía Censal 2022 Asunción**: SHP/KML/GeoJSON en descarga directa, malla censal decenal.

**Brecha principal detectada:**
- **No existe ejecución presupuestaria mensual** pública de la comuna (solo presupuesto aprobado en PDF anual + rendición de cuentas anual).
- **No existe padrón abierto** de contribuyentes ni dataset de recaudación (SATI es transaccional con login).
- **No existe portal de obras** estructurado (las obras se comunican por noticias).
- **No existe boletín oficial municipal** ni digesto legislativo consolidado.

---

## Catálogo de fuentes

### Dominio A — Sitio municipal (asuncion.gov.py)

| # | Fuente | URL | Tipo | Formato | Actualización | Cobertura | Automatización | Estado |
|---|--------|-----|------|---------|---------------|-----------|----------------|--------|
| A1 | Hesakã — Salarios mensuales | asuncion.gov.py/hesaka | Página + PDFs | PDF | Mensual | 2021→jul 2026 | **Alta** (URL predecible) | ⭐ Verificada |
| A2 | Ley 5282 Art. 8 — transparencia activa | asuncion.gov.py/ley-5282-14-articulo-8 | Página → Google Drive | Drive | Mensual (atrasada) | 2025-04→2026-03 | Media (gdown) | Atrasada |
| A3 | Presupuesto | asuncion.gov.py/presupuesto | Página + PDFs | PDF | Anual | 2025 (plurianual 25–27) | Baja (parseo PDF) | Verificada |
| A4 | Rendición de Cuentas anual | asuncion.gov.py/rendicion-de-cuentas-2025 | Página + PDF | PDF | Anual | 2025 | Baja | Verificada |
| A5 | Inventario de Bienes | asuncion.gov.py/inventario-de-bienes-municipales | Página + PDFs | PDF | **Nula** | hasta 2020 | — | Desactualizada |
| A6 | Licitaciones (enlace) | → contrataciones.gov.py (DNCP) | Redirección externa | Web | — | — | vía DNCP | Externo |
| A7 | Ordenanzas (compendio) | asuncion.gov.py/ordenanzas | Páginas + PDFs | PDF | — | 1991–presente (parcial) | Media (scrape WP) | Completo en JMA |
| A8 | Resoluciones | asuncion.gov.py/resoluciones | Página + PDFs | PDF | Nula | 2016–2024 (5 docs) | — | Mínima |
| A9 | Edictos | asuncion.gov.py/edictos | Página + PDF | PDF | Nula | 2016 (1 doc) | — | Mínima |
| A10 | Catastro (visor) | asuncion.gov.py/catastro/ | SPA JS | Mapa | — | Actual | **Baja** (no scrapeable simple) | Requiere análisis |
| A11 | Mapa descargable (capas) | asuncion.gov.py/mapa-descargable-de-la-ciudad-de-asuncion | Página → ZIP/PDF | ZIP/PDF | Puntual (02/2026) | Actual | **Alta** (descarga directa) | ⭐ Verificada |
| A12 | Plan Regulador | asuncion.gov.py/plan-regulador | Página + PDFs | PDF | Irregular | 2018–2022 | Alta (descarga) | Verificada |
| A13 | Plan Maestro Franja Costera | asuncion.gov.py/plan-maestro-de-la-franja-costera-de-asuncion | Página + PDF | PDF | Puntual | — | Media | PDF pasta 2026 verificado |
| A14 | Redundación en Línea (recaudación) | asuncion.gov.py/recaudacion-en-linea | Página (JS) | Web | Diaria/mensual (reportada) | desde 07/2025 | A confirmar (posible JSON) | **[no verificado]** |
| A15 | Otros (taxis, rodados, multas, PEI, DGRRD) | /taxis, /datos-de-rodados, /multas-usuales, /pei-2022-2025, /dgrrd-transparencia | Varía | Varía | n/d | n/d | n/d | **[no verificado]** |

### Dominio B — Junta Municipal (jma.gov.py)

| # | Fuente | URL | Tipo | Formato | Actualización | Cobertura | Automatización | Estado |
|---|--------|-----|------|---------|---------------|-----------|----------------|--------|
| B1 | Buscador de Ordenanzas | http://201.217.34.206:3000/ | SPA React | Web | n/d | n/d | Baja (sin API visible) | ⚠️ HTTP sin HTTPS |
| B2 | Biblioteca Digital — actas históricas | jma.gov.py/biblioteca-digital/ → :3001 | Imágenes escaneadas | JPEG | Estática | 1879–1998 (con huecos) | Descargable (Nextcloud) | ⚠️ HTTP sin HTTPS, sin OCR |
| B3 | Funcionarios / Hesaka JMA | jma.gov.py/funcionarios/ | Página → Google Drive | Drive/PDF | Mensual/anual | 2021–2026 | Media (gdown) | Verificada |
| B4 | Calendario de Sesiones | jma.gov.py/calendario-de-sesiones/ | Página → Drive | PDF | Semanal | 2024–2026 | **Alta** (scrape + Drive) | Verificada |
| B5 | Concejales | jma.gov.py/concejales-2022-2/ | Página | HTML/fotos | Estática | 2022–2026 | Trivial | Mínima (sin declaraciones) |
| B6 | Comisiones | jma.gov.py/elementor-8318/ | Página | HTML | — | — | n/a | **Página vacía** |
| B7 | FONAE / FONACIDE | jma.gov.py/fonacide/ | Página | Varía | n/d | n/d | n/d | **[no verificado]** |
| B8 | Campos/reservas: plan regulador, padrones, historial | jma.gov.py/plan-regulador-3/, /beneficiarios-adultos-mayores/, /datos-municipales/ | Varía | Varía | n/d | n/d | n/d | **[no verificado]** |

**Nota institucional:** jma.gov.py **no tiene un boletín oficial municipal**. El calendario de sesiones publica órdenes del día (PDF en Drive), no el texto de las ordenanzas aprobadas.

### Dominio C — Presupuesto, finanzas y salarios

| # | Fuente | URL | Tipo | Formato | Actualización | Cobertura | Automatización | Estado |
|---|--------|-----|------|---------|---------------|-----------|----------------|--------|
| C1 | Nómina de Funcionarios Públicos (nacional) | datos.gov.py/dataset/nómina-de-funcionarios-públicos | Dataset (DKAN) | CSV/JSON + API | Periódica | serie por ejercicio | **Alta** (API DKAN) | ⭐ Verificada |
| C2 | Portal SFP de funcionarios | datos.sfp.gov.py | Portal de datos | Web/descarga | Periódica | n/d | Media-alta | Parcial (URL verificada) |
| C3 | Transferencias a municipios (MEF) | servicios.mef.gov.py/consultas-publicas/muni.html | Portal + exportación | Tabla→Excel/PDF | Continua | 2017→hoy | **Media-alta** (Excel por RUC+año) | ⭐ Verificada |
| C4 | Presupuesto Ciudadano (PGN) | mef.gov.py (consulta ciudadana) | Portal | Web/PDF | Anual | por ejercicio | Baja-media | Nacional, no desglosa comuna |
| C5 | SATI (tributos) | sati.gov.py / publicsati.asuncion.gov.py | Portal transaccional | Web (login) | En línea | — | **Baja** (login, sin recaudación agregada) | Verificada |
| C6 | Portal Unificado Ley 5282 | informacionpublica.paraguay.gov.py | Portal de solicitudes | Web | — | — | n/a | Apoyo institucional |

### Dominio D — Contrataciones y obras

| # | Fuente | URL | Tipo | Formato | Actualización | Cobertura | Automatización | Estado |
|---|--------|-----|------|---------|---------------|-----------|----------------|--------|
| D1 | DNCP — buscador Muni | contrataciones.gov.py/buscador/general.html?filtro=municipalidad+de+asuncion | Portal web (JS) | HTML | Diaria | desde 2010 | Media (headless) | Verificada |
| D2 | **DNCP — API V3** (OCDS) | contrataciones.gov.py/datos/api/v3/doc/ | **API REST** | JSON (OCDS) | Diaria | desde 2010 | **Alta** (OAuth, token 15 min) | ⭐ Verificada |
| D3 | **DNCP — datasets CSV** | contrataciones.gov.py/datos/data | Catálogo de datasets | **CSV (CC BY 4.0)** | snapshots | desde 2010 | **Alta** (descarga directa) | ⭐ Verificada |
| D4 | Muni — blog Obras | asuncion.gov.py/category/obras | Noticias | HTML | Irregular | año vigente | Media (scrape WP) | Sin dataset estructurado |
| D5 | MOPC (obras en Asunción) | mopc.gov.py (transparencia, obras) | Portal web + noticias | HTML/PDF | Irregular | — | Media | Sin API |
| D6 | Mapa de Inversiones "RindiendoCuentas" | rindiendocuentas.gov.py | Dashboard nacional | Web | Periódica | — | n/d (profundidad municipal a verificar) | **[no verificado]** |

**Importante:** `api.dncp.gov.py` y `datos.contrataciones.gov.py` **NO existen (no resuelven DNS)**. La API y el portal de datos viven bajo `www.contrataciones.gov.py/datos/...`.

### Dominio E — Datos territoriales y técnicos

| # | Fuente | URL | Tipo | Formato | Actualización | Cobertura | Automatización | Estado |
|---|--------|-----|------|---------|---------------|-----------|----------------|--------|
| E1 | **INE Cartografía Censal 2022 Asunción** | ine.gov.py/microdatos/cartografia-digital-2022.php | Dataset geográfico | **SHP/KML/GeoJSON** (RAR) | Decenal | malla censal 2022 | **Alta** (descarga directa) | ⭐ Verificada |
| E2 | Mapa en capas (Municipalidad) | asuncion.gov.py → MAPA-EN-CAPAS.zip | Dataset geográfico | ZIP (SHP/GeoJSON probable) | Puntual (02/2026) | Actual | **Alta** (descarga) | URL verificada, contenido pendiente |
| E3 | Mapa catastral PDF | asuncion.gov.py/.../CIUDAD_DE_ASUNCION_CATASTRAL_A0...pdf | Plano | PDF (A0) | Puntual | 02/2026 | Alta (descarga, solo PDF) | Verificada |
| E4 | Portal Geoestadístico INE | portalgeoestad.ine.gov.py | Visor de mapas | Web | Censo 2022 | Nacional/distrital | Media (headless) | Verificada |
| E5 | IDE nacional (SISGEPAH/SNIT) | sisgepah.mopc.gov.py, snit.gov.py | Geoportal | Varía | — | Nacional | n/d | **NO VERIFICADO** (dominios sin respuesta) |
| E6 | Códigos Geográficos 2022 | ine.gov.py/microdatos/codigo-geografico-2022.php | Diccionario | Web/tabla | Decenal | 2022 | Alta | Útil para cruzar |
| E7 | Datos censales distritales | ine.gov.py/censo2022/ | Tablas/PDF/XLSX | Estadística | Decenal | distrito Asunción | Media | Verificada |
| E8 | ESSAP (saneamiento) | essap.com.py | Portal | Varía | n/d | n/d | n/d | **[no verificado]** |

---

## Brechas y oportunidades

### Brechas (datos que no existen en formato abierto)

1. **Ejecución presupuestaria mensual** de la comuna — no hay visor público; solo presupuesto aprobado (PDF anual) y rendición de cuentas anual.
2. **Padrón / recaudación de tributos** — SATI es transaccional; no hay dataset agregado de recaudación municipal (la "Recaudación en Línea" es parcialmente verificada).
3. **Portal de obras estructurado** — las obras se publican como noticias; no hay mapeo obra→contrato→proveedor→monto sistemático.
4. **Boletín oficial / digesto legislativo** — no existe; ordenanzas dispersas entre sitio municipal (compendio) y buscador JMA en IP sin HTTPS.
5. **Actas de sesiones** públicas — solo órdenes del día; actas históricas solo en imágenes sin OCR.
6. **Datos de concejales mínimos** — sin declaraciones patrimoniales, asistencia ni votaciones.

### Oportunidades (productos posibles)

1. **Pipeline salarial (Hesakã)**: consolidar 60+ PDFs a CSV mensual, actualizable — producto "nómina municipal en datos estructurados".
2. **Contrataciones de la Muni en dataset**: consumir API V3 OCDS filtrada por "Municipalidad de Asunción" → responder "¿quién le vende a la Municipalidad, cuánto y por qué?".
3. **Presupuesto abierto**: combinar presupuesto aprobado (PDF) + transferencias MEF + ejecución vía rendición anual — primer acercamiento a "¿qué está haciendo la Municipalidad, dónde y cuánto?".
4. **Mapa cívico**: cartografía censal INE + capas municipales → mapas de obras, servicios y territorio.
5. **Corrector de transparencia**: monitoreo mensual del cumplimiento de Ley 5282 Art. 8 (carpetas Drive atrasadas desde abril 2026).

---

## Nota metodológica

- **Fecha:** 26 de agosto de 2026.
- **Alcance:** fuentes oficiales de Asunción (municipal + junta + nacionales que publican datos de la comuna). Se excluyen prensa y terceros.
- **Base heredada:** investigación de muchotexto.net `research_ordenanzas_asuncion/` (11-ago-2026), re-verificada el 26-ago-2026 (estado confirmado: buscador JMA en `:3000` sin HTTPS, actas sin OCR, sin boletín oficial).
- **Método:** navegación y fetch directos. **Todo lo marcado **[no verificado]** se debe confirmar en FASE 2** antes de usarse.
- **Licencias:** los portales municipales no declaran licencia; los datasets nacionales usan la **Licencia de Uso de la Información Pública del Gobierno Paraguayo** (datos.gov.py) y la DNCP **CC BY 4.0**.

## Siguiente fase

Con este inventario, la **FASE 2 (Evaluación de fuentes)** debe evaluar Disponibilidad, Estructura, Actualización, Calidad, Automatización, Utilidad y Reutilización (criterios del plan maestro, sección 18) sobre las fuentes ⭐ para seleccionar **una primera fuente** para el primer pipeline.