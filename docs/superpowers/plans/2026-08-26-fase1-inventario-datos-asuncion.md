# Datos Públicos — FASE 1: Inventario de datos de Asunción — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Producir `DATA_INVENTORY.md` con el catálogo de fuentes de datos oficiales de la Municipalidad de Asunción.

**Architecture:** Investigación web por 5 subtópicos en paralelo (subagentes de research), con hallazgos volcados a archivos temporales en `research_inventario_asuncion/`, y síntesis final en `DATA_INVENTORY.md`.

**Tech Stack:** Búsqueda web, navegación de portales, fetch de URLs. Documentación en Markdown.

---

## Contexto

- Repo: `datos-publicos` (raíz local `C:\Users\pc\Desktop\Proyectos\Datos Publicos`), rama `main`.
- Existe investigación previa en `C:\Users\pc\Desktop\Proyectos\muchotexto.net\research_ordenanzas_asuncion\` (fecha 11-ago-2026) sobre normativa municipal. Se usa como base, PERO el inventario debe cubrir más (finanzas, contrataciones, territorial).
- Cada subagente guarda sus hallazgos en `research_inventario_asuncion/findings_<subtopic>.md`.
- `DATA_INVENTORY.md` se versiona en la raíz del repo. Los `findings_*.md` son temporales de trabajo (se pueden borrar tras sintetizar o dejarse; decisión: se borran al final para no ensuciar el repo).

## Estructura de archivos

- `research_inventario_asuncion/` — carpeta de trabajo (fuera del commit final, se elimina)
- `data/DATA_INVENTORY.md` → se versiona en la raíz como `DATA_INVENTORY.md` (según plan maestro). Ver Task 6.

---

### Task 1: Sitio oficial asuncion.gov.py

**Files:**
- Create: `research_inventario_asuncion/findings_01_sitio_municipal.md`

- [ ] **Step 1: Despachar subagente de investigación sobre asuncion.gov.py**

Petición al subagente:
- Navegar `https://www.asuncion.gov.py` y sus secciones de datos: transparencia, presupuesto, contrataciones, obras, ordenanzas, resoluciones, edictos, datos abiertos, archivo.
- Para cada sección documentar: URL exacta, tipo (web/PDF/API), formato, si hay actualización visible, cobertura temporal, calidad, accesibilidad, automatización posible, limitaciones.
- Guardar en `research_inventario_asuncion/findings_01_sitio_municipal.md`.

- [ ] **Step 2: Verificar que el archivo de hallazgos existe y no está vacío**

```bash
Get-ChildItem research_inventario_asuncion
```

Expected: `findings_01_sitio_municipal.md` presente, con >5 secciones documentadas.

---

### Task 2: Junta Municipal (jma.gov.py)

**Files:**
- Create: `research_inventario_asuncion/findings_02_junta_municipal.md`

- [ ] **Step 1: Despachar subagente de investigación sobre jma.gov.py**

Petición al subagente:
- Navegar `https://jma.gov.py`: buscador de ordenanzas, biblioteca digital, transparencia, actas, calendario de sesiones, concejales, comisiones.
- Para cada sección: URL, tipo, formato, actualización, cobertura, calidad, accesibilidad (¿HTTP sin HTTPS? ¿requiere JS?), automatización, limitaciones.
- Usar como base los hallazgos de muchotexto.net (research_ordenanzas_asuncion) si es útil verificar.
- Guardar en `research_inventario_asuncion/findings_02_junta_municipal.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_inventario_asuncion
```

Expected: `findings_02_junta_municipal.md` presente.

---

### Task 3: Presupuesto y finanzas municipales

**Files:**
- Create: `research_inventario_asuncion/findings_03_finanzas.md`

- [ ] **Step 1: Despachar subagente de investigación sobre finanzas municipales**

Petición al subagente:
- Buscar: portales de presupuesto municipal de Asunción (ej. asuncion.gov.py presupuesto, transparencia presupuestaria, SIAF Municipal, Ministerio de Hacienda), ejecución presupuestaria, salarios públicos municipales (Hesaka / datos de funcionarios), tributos municipales (patente, inmobiliario, permisos).
- Para cada fuente: URL, tipo, formato, actualización, cobertura, calidad, accesibilidad, automatización, limitaciones.
- Guardar en `research_inventario_asuncion/findings_03_finanzas.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_inventario_asuncion
```

Expected: `findings_03_finanzas.md` presente.

---

### Task 4: Contrataciones y obras

**Files:**
- Create: `research_inventario_asuncion/findings_04_contrataciones_obras.md`

- [ ] **Step 1: Despachar subagente de investigación sobre contrataciones y obras**

Petición al subagente:
- Buscar: contrataciones de la Municipalidad de Asunción en la DNCP (portal de contrataciones públicas de Paraguay, api.dncp.gov.py), licitaciones de la Muni, Licitación Pública, obras públicas municipales (MOPC, SEP?), infraestructura y proyectos.
- Para cada fuente: URL, tipo, formato, actualización, cobertura, calidad, accesibilidad, automatización, limitaciones.
- Guardar en `research_inventario_asuncion/findings_04_contrataciones_obras.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_inventario_asuncion
```

Expected: `findings_04_contrataciones_obras.md` presente.

---

### Task 5: Datos territoriales y técnicos

**Files:**
- Create: `research_inventario_asuncion/findings_05_territorial.md`

- [ ] **Step 1: Despachar subagente de investigación sobre datos territoriales**

Petición al subagente:
- Buscar: mapas de Asunción, GIS municipal, catastro, plan de desarrollo urbano, infraestructura (bañados, costanera), servicios, estadísticas (INE Para Asunción), censo 2022.
- Para cada fuente: URL, tipo, formato, actualización, cobertura, calidad, accesibilidad, automatización, limitaciones.
- Guardar en `research_inventario_asuncion/findings_05_territorial.md`.

- [ ] **Step 2: Verificar archivo**

```bash
Get-ChildItem research_inventario_asuncion
```

Expected: `findings_05_territorial.md` presente.

---

### Task 6: Sintetizar `DATA_INVENTORY.md`

**Files:**
- Create: `DATA_INVENTORY.md` (en la raíz del repo)

- [ ] **Step 1: Leer los 5 archivos de hallazgos**

```bash
Get-ChildItem research_inventario_asuncion
```

Leer con la herramienta Read cada `findings_*.md`.

- [ ] **Step 2: Escribir `DATA_INVENTORY.md`**

Estructura:
1. **Resumen ejecutivo** — qué se encontró, qué no existe, brechas clave.
2. **Catálogo de fuentes** — tabla por dominio:
   - Identificación, Municipio, Fuente, URL, Tipo, Formato, Actualización, Cobertura, Calidad, Accesibilidad, Automatización, Limitaciones, Reutilización.
3. **Brechas y oportunidades** — datos que no existen y productos/oportunidades que podrían construirse.
4. **Nota metodológica** — fecha, alcance, fuentes consultadas, qué fue verificado en esta fase vs. heredado de research_ordenanzas_asuncion (11-ago-2026).
5. **Trazabilidad** — cada fuente con su URL y fecha de obtención.

Escribir en español. Markdown.

- [ ] **Step 3: Limpiar la carpeta de trabajo temporal**

```bash
Remove-Item -Recurse -Force research_inventario_asuncion
```

- [ ] **Step 4: Commit**

```bash
git add DATA_INVENTORY.md
git commit -m "docs: add data inventory for Asuncion (FASE 1)"
```

Expected: commit con solo `DATA_INVENTORY.md` + spec/plan de FASE 1 si aún no commitados (en ese caso, incluir también `docs/superpowers/specs/2026-08-26-fase1-inventario-datos-asuncion.md` y `docs/superpowers/plans/2026-08-26-fase1-inventario-datos-asuncion.md`).

---

## Criterios de éxito (verificación final)

- `DATA_INVENTORY.md` en la raíz, versionado, en español.
- Cubre los 5 dominios: sitio municipal, legislativa, finanzas, contrataciones/obras, territorial.
- Cada fuente con URL, tipo, formato, frecuencia, limitaciones y pregunta que responde.
- Distingue lo verificado ahora de lo heredado de research_ordenanzas (ago 2026).
- Ningún archivo de investigación temporal quedó en el repo.