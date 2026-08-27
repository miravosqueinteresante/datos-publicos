# Datos Públicos — Indicadores de gasto (DNCP) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear un pipeline que derive indicadores de gasto de las contrataciones de la Muni (DNCP) en un JSON consumible, y documentar la brecha de salarios investigada.

**Architecture:** `scripts/indicadores_gasto.py` (stdlib) lee el CSV de contrataciones, agrega por categoría/proveedor/tipo de procedimiento, produce `www/datos/indicadores-gasto-2026.json`. TDD con unittest.

**Tech Stack:** Python 3.10 (stdlib), unittest, CSV/JSON.

---

## Contexto
- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`.
- Dataset fuente: `data/contrataciones_muni_2026.csv` (36 procesos; columnas id, objeto, estado, categoria, tipo_procedimiento, comprador, proveedor, monto, moneda, fechas, url).
- `www/datos/` ya tiene `contrataciones-2026.json`.

---

### Task 1: `scripts/indicadores_gasto.py` (TDD)

**Files:**
- Create: `scripts/indicadores_gasto.py`
- Create: `scripts/tests/test_indicadores_gasto.py`

- [ ] **Step 1: Test que falla**

```python
import unittest, os, json
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from indicadores_gasto import calcular_indicadores

CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,proveedor,monto,moneda,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,obra1,complete,Obras,open,Municipalidad de Asunción,C1,1000,PYG,,,,x
b,obra2,complete,Obras,open,Municipalidad de Asunción,C1,2000,PYG,,,,x
c,bien1,complete,Bienes,open,Municipalidad de Asunción,C2,500,PYG,,,,x
d,serv1,complete,Servicios,open,Municipalidad de Asunción,C3,300,PYG,,,,x
e,serv2,,Servicios,open,Municipalidad de Asunción,,,PYG,,,,x
"""

class TestIndicadores(unittest.TestCase):
    def test_distribucion_por_categoria(self):
        ind = calcular_indicadores(CSV)
        por_cat = {c["categoria"]: c["monto"] for c in ind["por_categoria"]}
        self.assertEqual(por_cat["Obras"], 3000)
        self.assertEqual(por_cat["Bienes"], 500)
        self.assertEqual(por_cat["Servicios"], 300)
    def test_totales(self):
        ind = calcular_indicadores(CSV)
        # monto total de filas con monto
        self.assertEqual(ind["monto_total"], 3800)
        self.assertEqual(ind["procesos"], 5)
        self.assertEqual(ind["proveedores_distintos"], 3)
    def test_top_proveedores_sin_proveedor_debajo(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["top_proveedores"][0]["proveedor"], "C1")
        self.assertEqual(ind["top_proveedores"][0]["monto"], 3000)
        # filas sin proveedor se cuentan como procesos pero no suman monto
        self.assertEqual(ind["procesos_sin_proveedor"], 1)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar, debe fallar** (ImportError).

- [ ] **Step 3: Implementar**

```python
import csv
import json
import os

RUTA_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "contrataciones_muni_2026.csv")
RUTA_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "www", "datos", "indicadores-gasto-2026.json")


def calcular_indicadores(csv_texto):
    filas = list(csv.DictReader(csv_texto.splitlines()))
    por_categoria = {}
    por_proveedor = {}
    por_tipo = {}
    monto_total = 0
    sin_proveedor = 0
    for f in filas:
        monto = f.get("monto") or "0"
        try:
            monto = float(monto)
        except ValueError:
            monto = 0
        cat = f.get("categoria") or "Sin categoría"
        por_categoria[cat] = por_categoria.get(cat, 0) + monto
        prov = f.get("proveedor") or ""
        if prov:
            por_proveedor[prov] = por_proveedor.get(prov, 0) + monto
        else:
            sin_proveedor += 1
        tipo = f.get("tipo_procedimiento") or "Sin tipo"
        por_tipo[tipo] = por_tipo.get(tipo, 0) + monto
        monto_total += monto
    top_prov = sorted(por_proveedor.items(), key=lambda x: -x[1])[:10]
    return {
        "procesos": len(filas),
        "monto_total": monto_total,
        "proveedores_distintos": len(por_proveedor),
        "procesos_sin_proveedor": sin_proveedor,
        "por_categoria": [{"categoria": c, "monto": m} for c, m in
                          sorted(por_categoria.items(), key=lambda x: -x[1])],
        "por_tipo_procedimiento": [{"tipo": t, "monto": m} for t, m in
                                   sorted(por_tipo.items(), key=lambda x: -x[1])],
        "top_proveedores": [{"proveedor": p, "monto": m} for p, m in top_prov],
    }


def main():
    with open(RUTA_CSV, encoding="utf-8") as f:
        ind = calcular_indicadores(f.read())
    os.makedirs(os.path.dirname(RUTA_JSON), exist_ok=True)
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(ind, f, ensure_ascii=False, indent=2)
    print(f"Indicadores generados: {ind['procesos']} procesos, "
          f"{ind['monto_total']:.0f} PYG total")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Tests pasan.** `python -m unittest discover -s scripts/tests`

- [ ] **Step 5: Commit.** `git add scripts/indicadores_gasto.py scripts/tests/test_indicadores_gasto.py && git commit -m "feat: add spend indicators pipeline from DNCP contracts (TDD)"`

---

### Task 2: Generar el JSON de indicadores real

- [ ] Step 1: `python scripts/indicadores_gasto.py` → `www/datos/indicadores-gasto-2026.json`.
- [ ] Step 2: Verificar: sum por categoría == total; 36 procesos; top proveedores.

```python
import json; d=json.load(open('www/datos/indicadores-gasto-2026.json',encoding='utf-8'))
print(d['procesos'], round(d['monto_total']), [ (x['categoria'], round(x['monto'])) for x in d['por_categoria'] ])
```

- [ ] Step 3: Commit. `git add www/datos/indicadores-gasto-2026.json && git commit -m "data: generate spend indicators JSON"`

---

### Task 3: Documentar la brecha de salarios en `DATA_INVENTORY.md`

- [ ] Step 1: Añadir sección "Brecha investigada — nómina/salarios de la Muni" con las 3 vías, URLs, frenos y la conclusión (no accesible estructurado hoy; OCR/hessaka inviable ahora).
- [ ] Step 2: Commit. `git add DATA_INVENTORY.md && git commit -m "docs: document investigated salary/nomina gap and spend indicators source"`

---

### Task 4: verificación + push

- [ ] Step 1: `python -m unittest discover -s scripts/tests` (todos OK).
- [ ] Step 2: Verificar que la web/lab puede leer el nuevo JSON (ruta relativa mismas).
- [ ] Step 3: Commit docs de spec/plan + `git push`.

---

## Criterios de éxito
- Indicadores JSON con datos reales (36 procesos; distribución categorías; top proveedores).
- Sumas por categoría == monto total.
- Brecha de salarios documentada (3 vías con evidencia).
- Tests pasan; sin dependencias nuevas.