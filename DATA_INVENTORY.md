# DATA_INVENTORY.md — Inventario de Datos de la Municipalidad de Asunción

> **Fecha de investigación:** 26 de agosto de 2026
> **Método:** navegación directa y fetch de fuentes oficiales (asuncion.gov.py, jma.gov.py, contrataciones.gov.py, mef.gov.py, datos.gov.py, ine.gov.py, mopc.gov.py). Estado de la investigación para FASE 1.
> **Nota de trazabilidad:** cada fuente indica su URL y su fecha de verificación. Lo marcado como **[no verificado]** no fue comprobado en esta pasada y debe validarse antes de usarse. Base heredada de la investigación de muchotexto.net (research_ordenanzas_asuncion, 11-ago-2026), re-verificada el 26-ago-2026.

---

## Resumen ejecutivo

**La Municipalidad de Asunción publica datos reales de transparencia, pero casi todo es PDF o Google Drive.** No existe una sección de datos abiertos con datasets estructurados (CSV/JSON/API) en el sitio municipal. Las fuentes estructuradas y automatizables del dominio de Asunción viven en **portales nacionales**: la nómina salarial (datos.gov.py / datos.sfp.gov.py, API DKAN), las licitaciones y contratos (DNCP, API V3 OCDS + datasets CSV) y las transferencias a municipios (MEF). La cartografía de Asunción es la fuente geoespacial más automatizable (INE Cartografía Censal 2022).

**Hallazgo clave (26-ago-2026):** la Municipalidad **sí expone servicios geoespaciales ArcGIS REST públicos** en `asuncion.gov.py/arcgis/rest/services/` — 19 servicios MapServer en `Mapa_Web/` + `Mapas/Mapa_Base`. Esto **contradice y corrige** el reporte inicial de FASE 1 que describía el catastro como "SPA no scrapeable". Los servicios REST son consultables programáticamente (JSON, con opción de geometría). Ver Dominio F. (Nota: se verificó una referencia externa que citaba una "capa Barrios ID 35" con campos `BRR_ID`/`NOMBRE`/`poblacion` — **esa capa NO existe**; la infraestructura es real pero los IDs y campos de esa referencia concretan están errados. Siempre verificar contra la fuente antes de usar.)

**Las 5 fuentes más prometedoras** (para FASE 2/3):
1. **Hesakã — salarios mensuales** (asuncion.gov.py/hesaka): 60+ PDFs 2021→jul 2026, URLs predecibles, alta automatización.
2. **DNCP — contrataciones y contratos de la Muni**: API V3 OCDS + datasets CSV (CC BY 4.0), cubre licitaciones/adjudicaciones/contratos/proveedores.
3. **datos.gov.py — Nómina de Funcionarios**: dataset estructurado con API DKAN, incluye municipios (granularidad municipal a confirmar).
4. **MEF — Transferencias a municipios** (servicios.mef.gov.py/consultas-publicas/muni.html): exportable a Excel, desde 2017.
5. **Muni — servicios ArcGIS REST** (Dominio F): capas de barrios y catastro consultables por API, base para el mapa / ficha de barrios.

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
| A10 | Catastro (visor) + servicios ArcGIS | asuncion.gov.py/catastro/ + /arcgis/rest/services/ | Visor SPA + **API REST** | Mapa + **JSON** | — | Actual | **Alta** (servicios REST públicos) | ⭐ Verificado (ver Dominio F) |
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
| D2 | **DNCP — API V3** (OCDS) ⭐ **SELECCIONADA** | contrataciones.gov.py/datos/api/v3/doc/ | **API REST** | JSON (OCDS) | Diaria | desde 2010 | **Alta** (OAuth, token 15 min) | ⭐ Verificada — ver `docs/fuentes/dncp-evaluacion.md` |
| D3 | **DNCP — datasets CSV** ⭐ **SELECCIONADA** | contrataciones.gov.py/datos/data | Catálogo de datasets | **CSV (CC BY 4.0)** | snapshots | desde 2010 | **Alta** (descarga directa) | ⭐ Verificada — ver `docs/fuentes/dncp-evaluacion.md` |
| D4 | Muni — blog Obras | asuncion.gov.py/category/obras | Noticias | HTML | Irregular | año vigente | Media (scrape WP) | Sin dataset estructurado |
| D5 | MOPC (obras en Asunción) | mopc.gov.py (transparencia, obras) | Portal web + noticias | HTML/PDF | Irregular | — | Media | Sin API |
| D6 | Mapa de Inversiones "RindiendoCuentas" | rindiendocuentas.gov.py | Dashboard nacional | Web | Periódica | — | n/d (profundidad municipal a verificar) | **[no verificado]** |
| D7 | **DNCP — perfil institucional por convocante** | contrataciones.gov.py/convocantes/municipalidad-asuncion/licitaciones/{año}.html | Perfil web paginado | HTML | Diaria | 2010→presente | Media (listado página) | ⭐ Verificado — verificación oficial del conjunto |
| D8 | **DNCP — catálogo de convocantes (CSV)** | contrataciones.gov.py/convocantes.csv | Dataset descargable | CSV | Periódica | actual | **Alta** | ⭐ Verificado — `slug=municipalidad-asuncion`, `codigo=108`, niv. Entidad |

**Importante:** `api.dncp.gov.py` y `datos.contrataciones.gov.py` **NO existen (no resuelven DNS)**. La API y el portal de datos viven bajo `www.contrataciones.gov.py/datos/...`.

**Perfil institucional por convocante (verificado 26-ago-2026):** la DNCP publica, para cada organismo, un perfil con sus licitaciones por año y sus responsables:
- Licitaciones de la Muni: `https://www.contrataciones.gov.py/convocantes/municipalidad-asuncion/licitaciones/{año}.html` (2010→2026, paginado).
- Responsables: `.../convocantes/municipalidad-asuncion/responsables.html`.
- Catálogo de convocantes descargable: `https://www.contrataciones.gov.py/convocantes.csv` (incluye `slug`, `codigo` SICP, nombre, tipo, nivel). La Municipalidad de Asunción: `slug=municipalidad-asuncion`, `codigo=108`, tipo Entidad.
- **Utilidad:** verificación cruzada del pipeline (mismo conjunto publicado oficialmente por la institución) y fuente de códigos SICP para escalar a otros municipios (FASE 6).

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

### Dominio F — Servicios ArcGIS REST de la Municipalidad (geoespacial)

**Raíz:** https://www.asuncion.gov.py/arcgis/rest/services?f=json
**Carpetas:** `Locator`, `Mapas`, `Mapa_Web` (19 servicios MapServer).
**Consulta:** cualquier capa responde `?f=json` con metadatos, y `/query?where=1=1&outFields=*&returnGeometry=true&outSR=4326&f=pjson` para features. Sin clave de acceso pública.

| # | Servicio | URL | Tipo | SR | Capas de interés | Estado |
|---|---------|-----|------|-----|------------------|--------|
| F1 | **Mapas/Mapa_Base** | /arcgis/rest/services/Mapas/Mapa_Base/MapServer | MapServer | **EPSG:3857** | 68 barrios (capa 30 grupo → 31 `Limites de Barrios`, 32 `Barrios`); límites municipio; río; zonas | ⭐ Verificado |
| F2 | **Mapa_Web/Mapa_General** | /arcgis/rest/services/Mapa_Web/Mapa_General/MapServer | MapServer | **EPSG:32721** (UTM 21S) | Capa 22 `catastro.sigasu.Lote`; 31 `Lotes`; 32 **`Datos Catastrales`** ⭐ (lotes + valores SATI); 33 Barrios (grupo vacío); movilidad; manzanas | ⭐ Verificado |
| F3 | Espacios Verdes | /arcgis/rest/services/Mapa_Web/Espacios_Verdes/MapServer | MapServer | — | `Espacios_Verdes_Vigente`, área silvestre protegida | Verificado |
| F4 | **Movilidad Urbana** | /arcgis/rest/services/Mapa_Web/Movilidad_Urbana/MapServer | MapServer | — | Paradas de buses, semáforos, bicisendas, refugios | Verificado |
| F5 | Centros Municipales | /arcgis/rest/services/Mapa_Web/Centros_Municipales/MapServer | MapServer | — | Ubicación y límites de centros municipales | Verificado |
| F6 | Lugares | /arcgis/rest/services/Mapa_Web/Lugares/MapServer | MapServer | — | Estaciones de servicio, clubes, supermercados, direcciones, manzanas, edificaciones | Verificado |
| F7 | Patrimonios Históricos | /arcgis/rest/services/Mapa_Web/Patrimonios_Historicos/MapServer | MapServer | — | 1.835 patrimonios históricos | Verificado |
| F8 | Edificios 10+ niveles | /arcgis/rest/services/Mapa_Web/Edificios_desde_10_Niveles_2024/MapServer | MapServer | — | Edificios altos 2024 | Verificado |
| F9 | Otros servicios | Baldios, Curvas_de_Nivel, Imagen_Satelital_2020, Medidas_Juridicas, Lotes_Calles_y_Ensanches, PlanRegulador, Asuncion_1786, Limites_Centro_Historico, ITINERARIOS, Comisarías, Koika/Caf | /arcgis/rest/services/Mapa_Web/... | MapServer | — | Ver listado completo en la raíz | Verificados (existen) |

**Notas técnicas clave del Dominio F:**
- **Barrios:** la capa de barrios (F1 capa 32) devuelve 68 registros, pero con **campos mínimos** (`objectid`, `st_area(shape)`); **no tiene `BRR_ID`, `NOMBRE`, `zona`, `seccion`, `poblacion`, `ordenanza`** ni geometría en consulta pública (puede requerir credencial o el visor). Verificar si existe un servicio de barrios con atributos más ricos (revisar `Lotes`/`Datos Catastrales`, que sí tienen campo `barrio`).
- **Datos Catastrales (F2 capa 32)** es la capa más rica: une `catastro.sigasu.Lote` (numero, manzana, zona, cuenta, barrio, zona_impos, clasificación, geometría `shape`) con `Tabla_Sati_Abril_2025` (superficie, valor terreno/edificación/fiscal). **Potencial eje catastral → ficha de barrio**.
- **Sistemas de coordenadas:** `Mapa_Base` = Web Mercator (3857); `Mapa_General` = UTM 21S (32721). Para el mapa web habrá que transformar coordenadas (aprendizaje GIS/PostGIS planificado).
- **Limitación:** la capa de barrios pública actual tiene datos pobres; el dato territorial rico está en las capas catastrales (`Lotes`, `Datos Catastrales`) con el campo `barrio` a nivel de lote.

---

## Brechas y oportunidades

### Brechas (datos que no existen en formato abierto)

1. **Ejecución presupuestaria mensual** de la comuna — no hay visor público; solo presupuesto aprobado (PDF anual) y rendición de cuentas anual.
2. **Padrón / recaudación de tributos** — SATI es transaccional; no hay dataset agregado de recaudación municipal (la "Recaudación en Línea" es parcialmente verificada).
3. **Portal de obras estructurado** — las obras se publican como noticias; no hay mapeo obra→contrato→proveedor→monto sistemático.
4. **Boletín oficial / digesto legislativo** — no existe; ordenanzas dispersas entre sitio municipal (compendio) y buscador JMA en IP sin HTTPS.
5. **Actas de sesiones** públicas — solo órdenes del día; actas históricas solo en imágenes sin OCR.
6. **Datos de concejales mínimos** — sin declaraciones patrimoniales, asistencia ni votaciones.
7. **Capa de barrios con atributos ricos** — la capa pública de barrios solo expone `objectid` + área; internamente la Municipalidad gestiona más atributos (los barrios aparecen poblados en las capas catastrales), pero no hay un Feature Layer de barrios con nombres/BRR_ID consultable públicamente.
8. **Nómina / salarios de la Municipalidad (INVESTIGADA, no accesible estructurado hoy)** — se evaluaron 3 vías el 26-ago-2026:
   - **Nómina nacional** (`datos.gov.py` / `datos.hacienda.gov.py`): `datos.hacienda.gov.py` → **403 Forbidden**; la API DKAN del portal no expone un endpoint JSON consumible; la página del dataset no lista recursos descargables en HTML estático.
   - **Portal SFP** (`datos.sfp.gov.py`): se descubrió su **API REST real** — `https://datos.sfp.gov.py/api/rest` (JBoss): `/funcionarios/partitions` 200 (años/meses), `/oee/data` 200 (434 organismos), `/funcionarios/data` 200 (**43.376.600 registros**). PERO filtrar por la Municipalidad requiere replicar el payload exacto de filtros del SPA (códigos `entidad/oee/nivel`, no por nombre; el `search` de DataTables no filtra). Ingeniería inversa pendiente.
   - **Hesakã** (`asuncion.gov.py/hesaka`): 140 PDFs públicos con patrón de URL predecible (`.../wp-content/uploads/AAAA/MM/Mes_AAAA.pdf`), pero **escaneados** → 364 páginas/mes sin texto extraíble → requiere OCR (tesseract/easyocr + modelos; alto esfuerzo, riesgo en números).
   - **Conclusión:** la masa salarial exacta de la Muni no es accesible hoy en formato estructurado de bajo esfuerzo. El indicador de gasto (FASE pendiente) se construye sobre **contrataciones adjudicadas** (DNCP), no sobre la nómina.

### Oportunidades (productos posibles)

1. **Pipeline de indicadores de gasto (DNCP)** — **IMPLEMENTADO** (`scripts/indicadores_gasto.py`, salida `www/datos/indicadores-gasto-2026.json`): distribución del gasto en contrataciones por categoría (Bienes/Obras/Servicios) y por proveedor. Es **"gasto en contrataciones adjudicadas"**, no presupuesto total (etiquetado como tal).
2. **Pipeline salarial (Hesakã o nómina SFP)**: pendiente — requiere OCR (Hesakã, escaneado) o ingeniería inversa del filtro del API SFP. Bloqueado como "pequeño y confiable" hoy; documentado en Brecha 8.
2. **Contrataciones de la Muni en dataset**: consumir API V3 OCDS filtrada por "Municipalidad de Asunción" → responder "¿quién le vende a la Municipalidad, cuánto y por qué?".
3. **Presupuesto abierto**: combinar presupuesto aprobado (PDF) + transferencias MEF + ejecución vía rendición anual — primer acercamiento a "¿qué está haciendo la Municipalidad, dónde y cuánto?".
4. **Mapa cívico / ficha de barrio**: usar los servicios ArcGIS REST (Dominio F) + cartografía censal INE + capas de servicios (movilidad, espacios verdes, centros, patrimonios) como base geoespacial del producto. La clave territorial es el **barrio** (campo `barrio` en `Lotes`/`Datos Catastrales`) o el **lote/cuenta catastral** (campo `cuenta` / `CTA_SIG_TXT`).
5. **Datos Catastrales + SATI**: unir `Datos Catastrales` (F2) para obtener valor fiscal de inmuebles por barrio → indicadores de valor de terreno por zona (requiere validar acceso/geometría y consideraciones de datos personales).
6. **Corrector de transparencia**: monitoreo mensual del cumplimiento de Ley 5282 Art. 8 (carpetas Drive atrasadas desde abril 2026).

---

## Nota metodológica

- **Fecha:** 26 de agosto de 2026.
- **Alcance:** fuentes oficiales de Asunción (municipal + junta + nacionales que publican datos de la comuna). Se excluyen prensa y terceros.
- **Base heredada:** investigación de muchotexto.net `research_ordenanzas_asuncion/` (11-ago-2026), re-verificada el 26-ago-2026 (estado confirmado: buscador JMA en `:3000` sin HTTPS, actas sin OCR, sin boletín oficial).
- **Método:** navegación y fetch directos. **Todo lo marcado **[no verificado]** se debe confirmar en FASE 2** antes de usarse.
- **Verificación ArcGIS (26-ago-2026):** se consultaron la raíz de servicios REST, los metadatos de los 19 servicios `Mapa_Web` + `Mapas/Mapa_Base`, y queries reales a las capas de barrios y catastrales. Resultado: infraestructura ArcGIS pública confirmada; **la capa "Barrios ID 35" citada por una referencia externa no existe** (error 500) y las capas de barrios públicas solo tienen `objectid` + área. La información de atributos ricos proviene de `Lotes`/`Datos Catastrales`. Se documenta esta discrepancia para evitar depender de referencias no verificadas.
- **Licencias:** los portales municipales no declaran licencia; los datasets nacionales usan la **Licencia de Uso de la Información Pública del Gobierno Paraguayo** (datos.gov.py) y la DNCP **CC BY 4.0**. Los servicios ArcGIS no muestran condiciones de uso explícitas (dato: dominio público municipal por Ley 5282/14, no declarado formalmente).

## Siguiente fase

**FASE 2 completada (26-ago-2026):** fuente seleccionada → **DNCP** (contrataciones de la Muni). Evaluación formal en `docs/fuentes/dncp-evaluacion.md`. Datos clave: Muni = convocante SICP `108`; ~5.989 procesos, 2.759 contratos; 70 procesos en 2026; CSV por año en `.../ocds/{AÑO}/{modulo}-masivo.zip` (CC BY 4.0).

La **FASE 3 (primer pipeline)** debe construir un flujo pequeño y completo: descargar los CSV de la DNCP → filtrar por la Muni (SICP 108) → limpiar/estructurar → validar → dataset propio en `data/` → subir a GitHub. Según el plan maestro: comprender y hacer funcionar manualmente primero, automatizar (GitHub Actions) después.