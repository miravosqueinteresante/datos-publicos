# Informe comparativo: DNCP (portal original) vs. Datos Públicos

Fecha: 2026-08-28
Método: investigación directa del portal DNCP (12 fetches verificados, docs `research_dncp_comparacion/findings_dncp.md`) + inventario real del proyecto (repo/`www`).

> Este informe es HONESTO sobre ambos: reconoce fortalezas de la DNCP (incluidas capas que el proyecto NO tiene) y define el diferencial real de Datos Públicos.

---

## 1. Qué ofrece la DNCP (verificado)

**Datos y acceso (fuerte):**
- Datos abiertos **OCDS** (CC BY 4.0): planificaciones, convocatorias, adjudicaciones, contratos, catálogo, proveedores, protestas.
- **CSV descargables por año** + **API V3** (OAuth; 10.000 registros/respuesta).
- **Buscadores especializados** con muchos filtros: licitaciones (etapa, categoría, procedimiento, convocante, fechas, flags), proveedores (RUC, categorías, tamaño), contratos, pagos, compradores, sanciones, audiencias.
- **Perfil de entidad**: procesos por año + **CSV por año** + directorio de responsables/UOC.
- **Trazabilidad declarada**: fuente SICP, URL, estándar OCDS, licencia.

**Análisis/estadística (existe, en el SIE):**
- **SIE** (Sistema de Información Estratégica): estadísticas gráficas por tema (adjudicaciones, pagos, comparativos, **ranking**, sanciones, etc.), tableros y **Red Flags**.
- **Visualizaciones**: mapa de obras (piloto, hasta 2020), burbujas de contratos por entidad/año, ciclo de licitación, calendario de ofertas.
- Reportes puntuales: historial de precios, ejecución de contratos; portal externo `quecompramos.gov.py`.

**Qué NO hace (brechas reales):**
- **No interpreta**: expone gráficos/tablas, pero no responde preguntas concretas ("quién concentra", "en qué gasta la entidad X") ni publica narrativa/conclusiones.
- **No hay dashboard por entidad individual**: el perfil de convocante es listado + CSV; el análisis agregado vive en SIE (nivel nacional), no "de la casa" por institución.
- **No hay ficha de proveedor consolidada** (cuánto, qué y a quién vendió la entidad; solo registro + datos crudos para reconstruir).
- **Fricción ciudadana**: buscador general sin filtros ni exportación; 10 registros/página; datos solo desde 2010; API con tope que obliga a paginar.
- **Doble clasificación de categorías** (antiguas 1-25 vs. nuevas 8 dígitos) sin normalizar.

---

## 2. Qué ofrece Datos Públicos (real, nuestro repo)

| Componente | Detalle |
|---|---|
| **Motor multi-entidad** | `dncp_contrataciones.py` (SICP+año), 43 tests, automatizado (GitHub Actions mensual+manual) |
| **Serie temporal por entidad** | Contrataciones de la Muni 2023-2026 (350/100/99/70) → CSV + JSON + indicadores por año |
| **Indicadores de contratación** | Distribución por categoría, % por procedimiento, concentración por proveedor, evolución anual |
| **Fichas de proveedores** | Top 10 por monto: métricas (total, contratos, años, categoría, % directo) + lista de contratos |
| **Web ciudadana** | Demo · Explorar (selector de año) · Análisis (evolución + detalle por año + fichas) · Datos · Metodología |
| **Trazabilidad** | Fuente, URL, fecha, proceso documentado en cada dataset |
| **Honestidad de brechas** | `DATA_INVENTORY.md` + Metodología documentan qué no publica la institución |
| **Publicado** | `datospublicos.muchotexto.net` + lab |

---

## 3. Comparación punto por punto

| Capacidad | DNCP | Datos Públicos | Diferencial |
|---|---|---|---|
| Datos abiertos OCDS | Sí (bruto) | Consume el mismo (procesa) | Neutro (misma fuente) |
| Acceso masivo | CSV + API (tope 10.000) | SVG + JSON procesado por año, ya limpio | **Datos Públicos**: entrega limpio/sin fricción |
| Buscadores de registros | Sí, con filtros | Explorar con selector de año + búsqueda | DNCP más rico en filtros brutos |
| **Indicadores por entidad** | NO (solo listado+CSV; análisis en SIE nacional) | **SÍ: serie + concentración + categorías por entidad** | **DIFERENCIAL CLAVE** |
| **Ficha de proveedor consolidada** | NO (reconstruible a mano) | **SÍ: top 10 con historial** | **DIFERENCIAL CLAVE** |
| **Narrativa/interpretación** | NO (gráficos solos) | Parcial (Demo + secciones con preguntas) | Diferencial (aún leve) |
| Dashboard global (SIE) | SÍ | NO (a escala) | **DNCP gana** |
| Red Flags / alertas | SÍ (SIE) | NO | **DNCP gana** |
| Visualizaciones (mapas, burbujas) | SÍ (parcial) | NO (barras/tablas) | **DNCP gana** |
| Trazabilidad | Sí (declarada) | Sí (en cada dataset) | Empate |
| Frescura/automatización | Depende del gobierno | Automatizado mensual + deploy | Diferencial de operación |

---

## 4. Qué preguntas respondemos que la DNCP NO responde directamente

1. **¿En qué gasta la Municipalidad de Asunción a lo largo del tiempo?** → nuestra serie 2023-2026 con evolución por año (la DNCP muestra procesos por año, no el análisis agregado por entidad "de la casa").
2. **¿Quién concentra la contratación de la Muni?** → top 10 de proveedores por monto con %. La DNCP tiene ranking nacional (SIE), no por-entidad consolidado.
3. **¿Un proveedor X le vende cuánto, en qué y con qué procedimiento a la Muni?** → fichas con historial. La DNCP expone los insumos para reconstruirlo, no la ficha.
4. **¿La contratación de la Muni es competitiva o directa?** → % por procedimiento directo vs. público por año y por proveedor (pregunta de competencia; la DNCP muestra el dato por registro, no la lectura agregada por entidad).

**Veredicto:** la DNCP es la fuente perfecta y un hub; Datos Públicos agrega la capa que falta: **procesamiento + lectura por entidad + serie temporal + fichas de proveedores**, con trazabilidad y honestidad, publicada de forma accesible.

---

## 5. Puntos en contra / debilidades de Datos Públicos (honestos)

1. **Menos escala que el SIE/DNCP**: no tenemos dashboard nacional, red flags ni visualizaciones geográficas.
2. **Dependemos 100% de la DNCP como fuente** (si cambia/cierra, el proyecto se estanca).
3. **Un solo entidad publicada** (la Muni) — el motor es multi-entidad pero la web muestra una.
4. **Volumen pequeño de usuarios/user impact** todavía (proyecto ciudadano incipiente).
5. **No hay red flags / indicadores de riesgo** (la DNCP los tiene en SIE).
6. La capa de interpretación aún es **informativa, no analítica profunda** (sin reportes narrativos extensos).

---

## 6. Conclusión del diferencial

**La DNCP publica los datos y ofrece navegación/estadística; Datos Públicos convierte esa información en lectura por entidad, serie temporal y fichas de proveedores — la capa que la DNCP no construye como producto para el ciudadano.**

El diferencial NO es "acceso a datos" (fuente compartida) ni "estadística global" (la DNCP gana). Es: **síntesis por entidad + dirección de proveedores + evolución temporal + accesibilidad**, con trazabilidad y automatización propias.

**Estrategia (para no competir en lo que la DNCP gana):**
- No intentar replicar SIE/red flags/mapas → enlazar esos recursos (Metodología) como "ir a la fuente".
- Enfocar en lo que es únicamente nuestro: **fichas por entidad + proveedores + serie** → profundizar ahí.
- Posicionar la web como "la capa de lectura ciudadana de la contratación pública por entidad".