# Datos Públicos — FASE 2: Evaluación de la fuente DNCP — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Evaluar formalmente la fuente DNCP (contrataciones de la Municipalidad de Asunción) contra los 7 criterios del plan maestro, y dejar documentado el detalle técnico para el pipeline de FASE 3.

**Architecture:** Investigación dirigida sobre el portal de datos abiertos de la DNCP (contrataciones.gov.py/datos), con consultas reales (API/docs, catálogo de datasets, descargas de prueba). Resultado en una ficha de evaluación + instrucción al DATA_INVENTORY.

**Tech Stack:** Fetch de URLs, API REST de la DNCP (lectura de docs), descargas CSV de prueba. Documentación en Markdown.

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- La fuente fue seleccionada en la evaluación comparativa (spec `docs/superpowers/specs/2026-08-26-fase2-evaluacion-fuente-dncp.md`).
- Datos conocidos de FASE 1: API V3 en `www.contrataciones.gov.py/datos/api/v3/` (no `api.dncp.gov.py`), datasets CSV en `/datos/data`, licencia CC BY 4.0, filtro del sitio municipal `filtro=municipalidad+de+asuncion`.

## Estructura de archivos

- `docs/fuentes/dncp-evaluacion.md` — ficha de evaluación (entregable principal).
- `DATA_INVENTORY.md` — actualizar para marcar la fuente seleccionada.
- Carpeta temporal de trabajo `research_dncp/` (se elimina al final).

---

### Task 1: Acceso y documentación de la API V3

**Files:**
- Create: `research_dncp/findings_acceso.md`

- [ ] **Step 1: Despachar subagente para leer la documentación de la API V3**

Petición al subagente:
- Leer el Swagger de la API: `https://www.contrataciones.gov.py/datos/api/v3/doc/swagger.json`
- Identificar: endpoints de licitaciones/convocatorias/adjudicaciones/contratos, parámetros de filtro por organismo/comprador, requisitos de autenticación (OAuth, tokens), rate limits.
- Determinar si existe un parámetro para filtrar por "Municipalidad de Asunción" (nombre, RUC o ID de UOC/org).
- Guardar en `research_dncp/findings_acceso.md` con: URLs exactas, endpoints, parámetros, límites, ejemplos.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_dncp
```
Expected: `findings_acceso.md` presente, no vacío, con detalles de la API.

---

### Task 2: Catálogo de datasets CSV descargables

**Files:**
- Create: `research_dncp/findings_datasets.md`

- [ ] **Step 1: Despachar subagente para mapear el catálogo de datos**

Petición al subagente:
- Navegar `https://www.contrataciones.gov.py/datos/data` y `https://www.contrataciones.gov.py/datos/`.
- Listar los datasets disponibles (PLANIFICACIONES, CONVOCATORIAS, LICITACIONES, ADJUDICACIONES, CONTRATOS, PROVEEDORES, PAGOS, etc.), con URL de descarga CSV exacta de cada uno.
- Identificar los campos relevantes de cada dataset (objeto, monto, proveedor, fecha, UOC).
- Determinar si hay dataset filtrado por organismo o si hay que filtrar el CSV completo.
- Guardar en `research_dncp/findings_datasets.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_dncp
```
Expected: `findings_datasets.md` presente.

---

### Task 3: Volumen y cobertura de la Municipalidad de Asunción

**Files:**
- Create: `research_dncp/findings_volumen.md`

- [ ] **Step 1: Despachar subagente para medir el volumen de datos de la Muni**

Petición al subagente:
- Usar el buscador de la DNCP o la API para aislar contrataciones de la Municipalidad de Asunción.
- Candidatos a probar:
  - Buscador web filtrado: `https://www.contrataciones.gov.py/buscador/general.html?filtro=municipalidad+de+asuncion`
  - Contar resultados aproximados de licitaciones, adjudicaciones y contratos de la Muni.
- Determinar el período de cobertura visible (¿desde qué año?) y la frecuencia de actualización.
- Estimar volumen (nº de registros) y frecuencia de nuevas licitaciones (diarias/semanales).
- Guardar en `research_dncp/findings_volumen.md` con números concretos y URLs consultadas.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_dncp
```
Expected: `findings_volumen.md` presente con cifras.

---

### Task 4: Descarga de prueba de un dataset CSV

**Files:**
- Create: `research_dncp/findings_descarga.md`

- [ ] **Step 1: Probar descarga real de un dataset CSV**

Petición al subagente:
- Probar la descarga de un dataset CSV de la DNCP (ej. uno pequeño) desde la URL identificada en Task 2.
- Verificar: ¿se descarga sin auth? ¿Tamaño? ¿Formato CSV válido? ¿Algunas filas de ejemplo?
- Probar si se puede filtrar por la Municipalidad de Asunción (columna de organismo/UOC) en el CSV local con un comando básico.
- Anotar si el CSV es "foto global" (todos los organismos) o hay dataset específico de la Muni.
- Guardar resultados en `research_dncp/findings_descarga.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_dncp
```
Expected: `findings_descarga.md` presente con evidencia de la descarga.

---

### Task 5: Sintetizar la ficha de evaluación

**Files:**
- Create: `docs/fuentes/dncp-evaluacion.md`
- Modify: `DATA_INVENTORY.md`

- [ ] **Step 1: Leer los 4 archivos de findings**

```bash
Get-ChildItem research_dncp
```
Leer `findings_acceso.md`, `findings_datasets.md`, `findings_volumen.md`, `findings_descarga.md`.

- [ ] **Step 2: Escribir la ficha `docs/fuentes/dncp-evaluacion.md`**

Estructura:
1. Resumen ejecutivo (decisión).
2. Evaluación por los 7 criterios del plan maestro — cada uno con evidencia (URL, fecha, nº).
   - Disponibilidad / Estructura / Actualización / Calidad / Automatización / Utilidad / Reutilización.
3. Requisitos técnicos para el pipeline (FASE 3): cómo aislar a la Muni, datasets mínimos, volumen, frecuencia, licencia, restricciones.
4. Indicadores/descubrimientos posibles (lo que se puede construir con estos datos).
5. Cómo reusar en otro municipio (config vs código).
6. Anexo: URLs verificadas.

- [ ] **Step 3: Actualizar `DATA_INVENTORY.md`**

Marcar la fila D2/D3 con "**SELECCIONADA (FASE 2)**" y añadir referencia a la ficha `docs/fuentes/dncp-evaluacion.md`.

- [ ] **Step 4: Limpiar carpeta temporal y commit**

```bash
Remove-Item -Recurse -Force research_dncp
git add docs/fuentes/dncp-evaluacion.md DATA_INVENTORY.md docs/superpowers/specs/2026-08-26-fase2-evaluacion-fuente-dncp.md
git commit -m "docs: evaluate DNCP as first data source (FASE 2)"
```

---

## Criterios de éxito (verificación final)

- `docs/fuentes/dncp-evaluacion.md` en el repo, en español, con los 7 criterios evaluados con evidencia.
- Se sabe exactamente cómo aislar a la Municipalidad de Asunción en la DNCP (filtro/UOC).
- Están identificados los datasets mínimos y las URLs de descarga.
- Volumen y frecuencia documentados con números.
- `DATA_INVENTORY.md` marca la fuente como seleccionada.
- Sin archivos temporales de investigación en el repo.