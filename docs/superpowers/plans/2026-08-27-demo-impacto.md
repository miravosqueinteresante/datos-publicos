# Datos Públicos — Página Demo de impacto — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear la página Demo (landing de demostración política) que cuenta la historia del proyecto y enlaza a las vistas reales.

**Architecture:** `www/demo.html` como landing; `www/index.html` (Explorar) se mantiene. En el `_site` publicado, `demo.html` es accesible en `/demo.html`. Como `index.html` es la raíz, en el plan se decide si la raíz apunta a demo (redirección/enlace) o se deja demo como página enlazada — decisión mínima e intrusiva.

**Tech Stack:** HTML5, CSS compartido (2026), JS vanilla mínimo (lectura del JSON de indicadores para métricas reales).

---

## Decisiones de estructura (confirmar en Task 1)

- **Opción A (recomendada):** `demo.html` = landing de demostración; `index.html` (Explorar) se mantiene como está. La landing Demo se enlaza desde el menú de todas las páginas como "Demo" y es el punto de entrada recomendado.
- **Opción B:** La raíz `index.html` se convierte en la landing demo y Explorar pasa a `explorar.html` (rompería el permalink actual y el lab que enlaza a `index.html`). NO recomendado: intrusivo.

→ Se adopta **Opción A**: Demo es una página nueva, protagonista, y queda también accesible como `https://datospublicos.muchotexto.net/demo.html`.

---

### Task 1: `www/demo.html` — landing de impacto

**Files:**
- Create: `www/demo.html`

- [ ] **Step 1: Crear la página** (estructura según spec):

- Hero con título-tesis, subtítulo y CTA a Explorar/Gasto.
- Sección "Por qué importa": 3 tarjetas (real / datos ya públicos / herramientas accesibles).
- Sección "Prueba viva": métricas reales del JSON de indicadores 2026 + ejecución 2024 (fetch mínimo de `datos/indicadores-gasto-2026.json`), con enlaces.
- Sección "Qué encontramos y qué falta": honestidad (disponible vs. bloqueado), enlaces a Metodología.
- CTA final.

- [ ] **Step 2: Commit** — `git add www/demo.html && git commit -m "feat: add impact demo landing page"`

---

### Task 2: Integrar Demo en el menú

**Files:**
- Modify: `www/index.html`, `www/datos.html`, `www/gasto.html`, `www/metodologia.html`

- [ ] **Step 1:** Añadir en el `<nav>` de cada página el ítem "Demo" como enlace (con `class="activo"` solo en demo.html). Orden sugerido: Demo · Explorar · Datos · Gasto · Metodología.

- [ ] **Step 2: Commit** — `git add ... && git commit -m "feat: add Demo to shared navigation"`

---

### Task 3: Verificación + push

- [ ] Step 1: Servir local, verificar `demo.html` + recursos.
- [ ] Step 2: `python -m unittest discover -s scripts/tests` (los tests de scripts siguen OK).
- [ ] Step 3: Commit docs (spec/plan) + `git push` (deploy automático).
- [ ] Step 4: Verificar en producción `https://datospublicos.muchotexto.net/demo.html`.

---

## Criterios de éxito
- Demo cuenta la historia, usa métricas reales, enlaza a las vistas.
- Menú coherente.
- Tests OK; desplegado.