# Datos Públicos — Inventario presupuestario 2024 — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Producir `docs/presupuesto/FUENTES_2024.md`: inventario documental del ciclo presupuestario 2024 de la Municipalidad de Asunción, con trazabilidad y sin programar.

**Architecture:** Investigación dirigida sobre fuentes oficiales (asuncion.gov.py, jma.gov.py, MEF, DNCP), verificando la disponibilidad específica del ejercicio 2024. Resultado en un Markdown con tablas y evidencia. Sin código.

**Tech Stack:** Fetch de URLs, navegación de portales. Documentación en Markdown.

---

## Contexto
- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`.
- Inventario global previo en `DATA_INVENTORY.md` (FASE 1) sirve de punto de partida, PERO no verifica la disponibilidad 2024 específica.
- Fuentes del ciclo: ordenanza, presupuesto (programa/dependencia/objeto/ingresos), modificaciones, ejecución, rendición, salarios (Hesakã), transferencias MEF, contrataciones DNCP.
- Carpetas a crear: `docs/presupuesto/`.

---

### Task 1: Presupuesto aprobado y ordenanza 2024 (asuncion.gov.py)

**Files:**
- Create: `docs/presupuesto/FUENTES_2024.md` (se irá completando en tasks)

- [ ] **Step 1: Verificar qué publica el sitio municipal sobre presupuesto 2024**

Petición al subagente (navegación):
- URL candidatas a revisar: `https://www.asuncion.gov.py/presupuesto`, `/presupuesto-2025`, `/presupuesto-2024`, sección Transparencia.
- ¿Existe el presupuesto aprobado 2024? ¿En qué formato (PDF/XLS)? ¿Por programa/dependencia/objeto/ingresos?
- ¿Existe la **Ordenanza de presupuesto 2024** y dónde?
- Documentar URL exacta, formato, contenido, estado (verificado/no verificado).

Resultado en el Markdown (sección "Presupuesto aprobado").

- [ ] **Step 2: Registro en tablas con estado.**

---

### Task 2: Ejecución, modificaciones y rendición de cuentas 2024

**Files:**
- Modify: `docs/presupuesto/FUENTES_2024.md`

- [ ] **Step 1: Verificar ejecución/rendición 2024**

- Revisar `https://www.asuncion.gov.py/rendicion-de-cuentas-2024` (y variantes), `/rendicion-de-cuentas-2025` (para patrón), y buscar ejecución presupuestaria.
- ¿Publican ejecución mensual? (FASE 1 indicó que NO existe visor público; confirmar para 2024).
- ¿Existen modificaciones presupuestarias 2024 en el sitio o la Junta Municipal?

Resultado en el Markdown (sección "Ejecución y modificaciones").

---

### Task 3: Salarios (Hesakã) y transferencias MEF 2024

**Files:**
- Modify: `docs/presupuesto/FUENTES_2024.md`

- [ ] **Step 1: Verificar salarios y transferencias 2024**

- Hesakã: `https://www.asuncion.gov.py/hesaka` — confirmar que existen PDFs de **2024** (patrón `/uploads/AAAA/MM/`), formato (escaneado → OCR).
- MEF: `https://servicios.mef.gov.py/consultas-publicas/muni.html` — verificar consulta por RUC de la Muni + año 2024 (datos desde 2017).

Resultado en el Markdown (sección "Salarios y transferencias").

---

### Task 4: Contrataciones DNCP 2024

**Files:**
- Modify: `docs/presupuesto/FUENTES_2024.md`

- [ ] **Step 1: Confirmar disponibilidad DNCP 2024**

- El pipeline ya procesa la DNCP por año (2026 probado). Confirmar que `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/2024/masivo.zip` existe (verificación de URL sin descargar todo — HEAD o rango).
- En el inventario: indicar que el pipeline existente se puede ejecutar para 2024 (es la fuente más automatizable del ciclo).

---

### Task 5: Análisis del ciclo y redacción final

**Files:**
- Modify: `docs/presupuesto/FUENTES_2024.md`

- [ ] **Step 1: Sintetizar el mapa del ciclo**

- Mapa Aprobado → Modificaciones → Vigente → Ejecución → Pagos con las fuentes encontradas.
- Brechas explícitas (qué falta, qué requiere OCR/pedido). Marco el paso a "modelo de datos" del documento de ideas como siguiente etapa.

- [ ] **Step 2: Commit**

```bash
git add docs/presupuesto/
git commit -m "docs: add budget cycle 2024 sources inventory (FUENTES_2024)"
```

- [ ] **Step 3: Commit docs de spec/plan + push**

---

## Criterios de éxito
- `FUENTES_2024.md` con tablas y evidencia (URL + fecha + estado).
- Fuentes del ciclo documentadas con su disponibilidad 2024 real.
- Brechas explícitas; sin inventar.
- Nada programado.
- Pusheado.