# Ficha de evaluación — DNCP: contrataciones de la Municipalidad de Asunción

> **Fecha:** 26 de agosto de 2026
> **Fase:** FASE 2 (evaluación de fuente) → paso a FASE 3 (primer pipeline)
> **Criterios:** los 7 del plan maestro (sección 18).
> **Método:** consultas reales a la DNCP (API V3 doc, catálogo `/datos/data`, descarga de CSV). Evidencia con URLs y números. Lo no verificado se marca.

---

## 1. Resumen ejecutivo

La **DNCP** es la primera fuente del proyecto. La Municipalidad de Asunción es la **convocante/comprador SICP `108`** en el Sistema de Información de Contrataciones del Estado (SICE). Sus datos de contratación pública están disponibles en tres vías compatibles y actualizables:

1. **CSV masivos por año** (`contrataciones.gov.py/images/opendata-v3/final/ocds/{AÑO}/{modulo}-masivo.zip`), descarga anónima, licencia **CC BY 4.0** — vía recomendada para el pipeline.
2. **API V3 REST (OCDS)** (`contrataciones.gov.py/datos/api/v3/doc/`), requiere OAuth (token 15 min) — para consultas puntuales/frescas.
3. **Buscadores web** filtrados por convocante — para verificación humana.

**Volumen verificado:** ~5.989 procesos (licitaciones), 2.759 contratos y 1.554 pagos de la Muni; 70 procesos solo en 2026. Cobertura activa (datos de ago-sep 2026 presentes). Estándar **OCDS internacional**, reutilizable para cualquier municipio de Paraguay.

**Decisión:** construir el primer pipeline sobre los **CSV masivos de la DNCP**, filtrando por la Muni (SICP 108), con el **`records.csv`** como fuente primaria (resumen por proceso, con `buyer/name`). Ver FASE 3.

---

## 2. Evaluación por criterios

### 2.1 Disponibilidad — ⭐ Alta (5/5)

- Acceso sin registro ni login (descarga de CSV anónima, verificada con `curl.exe`).
- API con OAuth: registro gratuito, `request_token` → `access_token` (15 min). El pipeline puede empezar sin API usando CSV.
- URL de descarga directa: `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/{AÑO}/{modulo}-masivo.zip` (años 2010–2026, verificada).
- **No verificado:** límite concreto de llamadas/min con auth; formato exacto del organismo en algunos campos de `awards.csv`.

### 2.2 Estructura — ⭐ Alta (5/5)

- Estándar **OCDS 1.1** (Open Contracting Data Standard) internacional, aplanado a CSV con OCDS Flatten Tool.
- Un `records.csv` por año (1 fila = 1 proceso) con `compiledRelease/buyer/name` → **métrica confiable para aislar a la Muni**: 70 procesos en 2026.
- Datasets disponibles: planificaciones, convocatorias, licitaciones (procesos completos `masivo.zip`), adjudicaciones (`awa-masivo.zip`), contratos (`con-masivo.zip`), proveedores, catálogo, protestas.
- **Motivo de precaución:** los CSV son OCDS anidado en columnas (`compiledRelease/...`); hay que conocer el esquema exacto antes de hardcodear nombres de columna. En `awards.csv` el campo `buyer/name` viene vacío en parte de las filas — usar `records.csv` o el ID del organismo.

### 2.3 Actualización — ⭐ Alta (5/5)

- Datos al día: registros de **ago-sep 2026** presentes (licitaciones, contratos 10-08-2026, pagos 19-08-2026).
- Frecuencia: la base de la DNCP se actualiza a diario; hay CSV por año regenerados periódicamente.
- Estimación de ritmo (Muni): ~370 procesos/año de media en 16 años; varias licitaciones y pagos al mes en 2026.

### 2.4 Calidad — Alta (5/5, con matiz)

- Licencia **CC BY 4.0** confirmada; datos derivados del SICE, "recopilación fiel e integral" declarada.
- Campos clave presentes: objeto (`nombre_licitacion`), monto (`monto_total_adjudicado`/`value/amount`), moneda, proveedor, fecha, convocante, estado, categoría.
- **Matiz:** campo de organismo a veces vacío en `awards.csv`; el string de `convocante` incluye UOC (p. ej. "MUNICIPALIDAD DE ASUNCION UOC N"); nombres con/sin tilde ("Asuncion" vs "Asunción"). Requiere normalización.
- **No verificado:** RUC del proveedor en los CSV aplanados (está en el modelo OCDS; confirmar a nivel de records/suppliers).

### 2.5 Automatización — ⭐ Alta (5/5)

- Descarga directa anónima por URL construida (año + módulo) → cubre un pipeline simple sin API keys.
- API V3 para frescura: `search/processes?parties.identifier.id=108`, `visualizations/minimal/contract/buyer/108/year/{año}` (verificadas).
- Limitación de la API: 10.000 registros/llamada y token de 15 min → no usar para descarga masiva.
- El pipeline mínimo viable: descargar `records.csv`/`con-masivo.zip` del año vigente → filtrar por SICP 108 o `buyer/name` → limpiar → CSV estructurado propio.

### 2.6 Utilidad pública — ⭐ Alta (5/5)

Responde la pregunta del plan maestro: **"¿Qué está haciendo la Municipalidad, dónde y cuánto?"**

- ¿Qué hace? → objeto/nombre de la licitación.
- ¿Cuánto? → montos (referencial, adjudicado, contratado) por categoría/año.
- ¿Con quién? → proveedores adjudicados.
- ¿Cuándo? → fechas de publicación, adjudicación, firma, pago.

Indicadores derivados posibles (para la plataforma): top proveedores de la Muni, monto adjudicado por año, distribución por categoría (bienes/servicios/obras), contratos sin proceso, pagos por proveedor.

### 2.7 Reutilización — ⭐ Alta (5/5)

- La DNCP cubre **todos** los organismos y municipios de Paraguay → el pipeline se parametriza por **ID SICP** (configuración) sin tocar el motor (código).
- Modelo previsto: `motor + configuración del municipio + fuentes` del plan maestro. Cambiar de municipio = cambiar el ID de convocante y el nombre.
- El estándar OCDS es internacional → posible comparación con otros países de la región (reutilización conceptual).

---

## 3. Requisitos técnicos para el pipeline (FASE 3)

| Ítem | Definición |
|---|---|
| **Fuente primaria** | CSV `records.csv` (resumen por proceso) + `con-masivo.zip` (contratos) de la DNCP |
| **Identificación de la Muni** | SICP **108** (filtro por `parties.identifier.id=108` en API; `buyer/name` contiene "Municipalidad de Asunción" en CSV) |
| **Vía de descarga** | `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/{AÑO}/{modulo}-masivo.zip` (anónima, CC BY 4.0) |
| **Período base** | 2010–2026 (17 años); el pipeline puede arrancar con 1–3 años y ampliar |
| **Frecuencia del pipeline** | Semanal o mensual (datos estables; es un snapshot por año) — decidir en FASE 3 |
| **Licencia** | CC BY 4.0 — requerir atribución |
| **Restricciones** | API: 10.000 reg/llamada, token 15 min, rate limit con auth sin documentar — evitar API para volumen; CSV anónimo OK |
| **Normalización necesaria** | Nombre del convocante (mayúsculas/tildes/UOC), montos (string→número, moneda), fechas (dd/mm/yyyy→ISO) |

## 4. Cómo se reutiliza en otro municipio

En la configuración del pipeline (no en el código):
- `municipio = { id_sicp: 108, nombre: "Municipalidad de Asunción" }` → cambiar a otro municipio = cambiar `id_sicp` + `nombre`.
- El código (descarga, filtro, limpieza, validación) permanece igual.

## 5. Anexo — URLs verificadas (26-ago-2026)

- Descarga CSV: `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/2026/awa-masivo.zip` (49 MB; `awards.csv` 36.627 filas, `records.csv` 5.951 filas, 70 procesos Muni)
- API V3 (spec): `https://www.contrataciones.gov.py/datos/api/v3/doc/swagger.json`
- API V3 (docs): `https://www.contrataciones.gov.py/datos/api/v3/doc/`
- Ejemplo procesos Muni (API): `https://www.contrataciones.gov.py/datos/api/v3/doc/search/processes?parties.identifier.id=108`
- Búsqueda convocante: `https://www.contrataciones.gov.py/datos/api/v3/doc/search/procuringEntities`
- Contratos por año: `https://www.contrataciones.gov.py/datos/api/v3/doc/visualizations/minimal/contract/buyer/108/year/2024`
- Buscador web Muni: `https://www.contrataciones.gov.py/buscador/general.html?filtro=municipalidad+de+asuncion`
- Catálogo de datasets: `https://www.contrataciones.gov.py/datos/data`
- Licencia: `https://creativecommons.org/licenses/by/4.0/`