# Datos Públicos — Fichas de proveedores (top 10) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Producir `www/datos/proveedores.json` con el top 10 de proveedores de la Muni (por monto 2023-2026) y mostrarlo en Análisis como fichas desplegables.

**Architecture:** `scripts/generar_proveedores.py` (TDD) agrega la serie y genera el JSON; Análisis (HTML+JS) renderiza las 10 fichas con métricas y lista de contratos, desplegables.

**Tech Stack:** Python 3.10 (stdlib), JS vanilla, HTML/CSS.

---

## Contexto
- Serie: `data/contrataciones_muni_2023..2026.csv` (350/100/99/70 procesos).
- Columnas de cada contrato: objeto, estado, categoria, tipo_procedimiento, comprador, proveedor, monto, moneda, fechas, url_muni.
- Fichas: solo top 10 por monto acumulado; sin inventar RUC/rubro (fuera del dataset).

---

### Task 1: `scripts/generar_proveedores.py` (TDD)

**Files:**
- Create: `scripts/generar_proveedores.py`
- Create: `scripts/tests/test_generar_proveedores.py`

- [ ] **Step 1: Test que falla**

```python
import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from generar_proveedores import calcular_top, es_directo

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,o1,,Bienes,Licitación Pública Nacional,Muni,P1,100,PYG,,,,x
b,o2,,Bienes,Menor cuantía nacional,Muni,P1,50,PYG,,,,x
c,o3,,Servicios,Licitación Pública Nacional,Muni,P2,300,PYG,,,,x
d,o4,,Obras,Contratación Directa,Muni,P2,200,PYG,,,,x
"""

class TestProveedores(unittest.TestCase):
    def test_es_directo(self):
        self.assertTrue(es_directo("Menor cuantía nacional"))
        self.assertTrue(es_directo("Contratación Directa"))
        self.assertFalse(es_directo("Licitación Pública Nacional"))
    def test_calcular_top_agrega_y_rankea(self):
        top = calcular_top(CSV)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0]["proveedor"], "P2")  # mayor monto (500)
        self.assertEqual(top[0]["monto_total"], 500)
        self.assertEqual(top[0]["contratos"], 2)
        self.assertEqual(top[1]["proveedor"], "P1")
        self.assertEqual(top[1]["monto_total"], 150)
        self.assertEqual(top[1]["categoria_principal"], "Bienes")

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar, debe fallar** (ImportError).

- [ ] **Step 3: Implementar `generar_proveedores.py`**

```python
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
WEB_DATOS = os.path.join(ROOT, "www", "datos")
ANIOS = ["2023", "2024", "2025", "2026"]

METODOS_DIRECTOS = ("Menor", "Directa", "Excepción", "CVE", "menor cuantía", "directa")


def es_directo(tipo):
    t = (tipo or "").lower()
    return t != "licitación pública nacional" and "menor" in t or "direct" in t or "excepción" in t or "cve" in t


def calcular_top(csv_texto):
    proveedores = {}
    filas = list(csv.DictReader(csv_texto.splitlines()))
    for r in filas:
        p = (r.get("proveedor") or "").strip()
        if not p:
            continue
        try:
            monto = float(r.get("monto") or 0)
        except ValueError:
            monto = 0
        e = proveedores.setdefault(p, {
            "montos": 0.0, "contratos": 0, "anios": set(),
            "categorias": {}, "directo_monto": 0.0,
            "contratos_lista": [],
        })
        e["montos"] += monto
        e["contratos"] += 1
        e["anios"].add(r.get("fecha_adjudicacion", "")[:4] if r.get("fecha_adjudicacion") else "")
        e["categorias"][r.get("categoria") or "Sin categoría"] = \
            e["categorias"].get(r.get("categoria") or "Sin categoría", 0) + monto
        if es_directo(r.get("tipo_procedimiento")):
            e["directo_monto"] += monto
        e["contratos_lista"].append({
            "objeto": r.get("objeto", ""), "anio": r.get("fecha_adjudicacion", "")[:4],
            "categoria": r.get("categoria", ""), "monto": monto,
            "procedimiento": r.get("tipo_procedimiento", ""),
            "fecha": r.get("fecha_adjudicacion", ""), "url": r.get("url_muni", ""),
        })
    ranking = sorted(proveedores.items(), key=lambda kv: (-kv[1]["montos"], kv[0]))
    resultado = []
    for idx, (nombre, e) in enumerate(ranking[:10], start=1):
        cat_principal = max(e["categorias"], key=lambda k: e["categorias"][k]) if e["categorias"] else ""
        pct_directo = round(e["directo_monto"] / e["montos"] * 100, 1) if e["montos"] else 0
        anios = sorted(a for a in e["anios"] if a)
        resultado.append({
            "proveedor": nombre,
            "posicion": idx,
            "monto_total": round(e["montos"], 2),
            "contratos": e["contratos"],
            "anios_activos": len(anios),
            "anios": anios,
            "categoria_principal": cat_principal,
            "pct_directo": pct_directo,
            "contratos_lista": e["contratos_lista"],
        })
    return resultado


def main():
    todos = []
    for a in ANIOS:
        path = os.path.join(DATA_DIR, f"contrataciones_muni_{a}.csv")
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                todos.append(f.read())
    top = calcular_top("\n".join(todos))
    os.makedirs(WEB_DATOS, exist_ok=True)
    with open(os.path.join(WEB_DATOS, "proveedores.json"), "w", encoding="utf-8") as f:
        json.dump(top, f, ensure_ascii=False, indent=2)
    print(f"Top {len(top)} proveedores → www/datos/proveedores.json")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Tests pasan** (ajustar `es_directo` si la lógica no cuadra con el expected del test; la expresión es frágil — usar una función simple por substring/!=).

- [ ] **Step 5: Commit** — `git add scripts/generar_proveedores.py scripts/tests/test_generar_proveedores.py && git commit -m "feat: supplier top-10 generator (TDD)"`

---

### Task 2: Generar `proveedores.json` real + verificar

- [ ] **Step 1: Ejecutar**

```bash
python scripts/generar_proveedores.py
```

- [ ] **Step 2: Verificar el JSON** (top 10, montos, contratos)

```python
import json; d=json.load(open('www/datos/proveedores.json',encoding='utf-8'))
print(len(d)); [print(p['posicion'], p['proveedor'], p['monto_total'], p['contratos'], p['anios_activos']) for p in d]
```
Expected: 10 proveedores; PETROLEOS DEL SUR S.A. primero (~108M); BERNARDA GONZALEZ con 9 contratos / 4 años.

- [ ] **Step 3: Commit** — `git add www/datos/proveedores.json && git commit -m "data: add supplier top-10 fichas JSON"`

---

### Task 3: Sección "Proveedores" en Análisis (HTML + JS)

**Files:**
- Modify: `www/analisis.html`
- Modify: `www/js/analisis.js`

- [ ] **Step 1: Añadir sección en `analisis.html`** (tras "Detalle por año", antes de la nota):

```html
<section class="ind-bloque">
  <header class="ind-bloque-head">
    <h2>Principales proveedores de la Muni</h2>
    <p>Top 10 por monto acumulado 2023-2026 · clic para detalle</p>
  </header>
  <div class="ind-bloque-cuerpo" id="fichas-proveedores"></div>
</section>
```

- [ ] **Step 2: En `analisis.js`, añadir carga y render de las fichas**:

```javascript
function renderFichas(lista) {
  const el = document.getElementById("fichas-proveedores");
  el.innerHTML = `<div class="fichas-grid">${lista.map(p => `
    <details class="ficha" data-proveedor="${p.proveedor}">
      <summary>
        <span class="rank">${p.posicion}</span> <strong>${p.proveedor}</strong>
        <span class="ficha-resumen">${FMT.format(p.monto_total)} PYG · ${p.contratos} contratos</span>
      </summary>
      <div class="ficha-detalle">
        <div class="metricas">
          <div class="metrica"><div class="valor">${FMT.format(p.monto_total)}</div><div class="etiqueta">Monto total</div></div>
          <div class="metrica"><div class="valor">${p.contratos}</div><div class="etiqueta">Contratos</div></div>
          <div class="metrica"><div class="valor">${p.anios_activos}</div><div class="etiqueta">Años activos</div></div>
          <div class="metrica"><div class="valor">${p.categoria_principal || "—"}</div><div class="etiqueta">Categoría pral.</div></div>
          <div class="metrica"><div class="valor">${FMT2.format(p.pct_directo)}%</div><div class="etiqueta">Por vía directa</div></div>
        </div>
        <h4>Contratos</h4>
        <div class="tabla-envolvente"><table>
          <thead><tr><th>Objeto</th><th>Año</th><th>Monto</th><th>Procedimiento</th><th>Enlace</th></tr></thead>
          <tbody>${p.contratos_lista.map(c => `<tr>
            <td>${c.objeto}</td><td>${c.anio}</td><td class="monto">${FMT.format(c.monto)}</td>
            <td>${c.procedimiento}</td>
            <td>${c.url ? `<a href="${c.url}" target="_blank" rel="noopener">ver</a>` : "—"}</td>
          </tr>`).join("")}</tbody>
        </table></div>
      </div>
    </details>`).join("")}</div>`;
}
```

En `init()` (tras cargar indicadores), cargar `proveedores.json`:

```javascript
try {
  const prov = await (await fetch("datos/proveedores.json")).json();
  renderFichas(prov);
} catch {}
```

- [ ] **Step 3: CSS** (en `style.css`): `.fichas-grid`, `.ficha`, `summary` (con cursor, padding), `.ficha-detalle`, `.ficha-resumen`.

- [ ] **Step 4: Commit** — `git add www/analisis.html www/js/analisis.js www/css/style.css && git commit -m "feat: supplier fichas section in Analisis"`

---

### Task 4: Verificación + push

- [ ] Step 1: `python -B -m unittest discover -s scripts/tests` (todos OK).
- [ ] Step 2: Servir local → verificar: proveedores.json 200, analisis.html renderiza las 10 fichas desplegables, métricas correctas.
- [ ] Step 3: Commit docs (spec/plan) + `git push` (deploy automático).
- [ ] Step 4: Verificar producción (`/analisis.html` + `/datos/proveedores.json`).

---

## Criterios de éxito
- `proveedores.json` top 10 por monto con métricas y contratos.
- Análisis muestra "Principales proveedores" (10 fichas desplegables).
- Tests OK; sin inventar RUC/rubro.