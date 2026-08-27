# Datos Públicos — Presupuesto 2024: dataset de ejecución — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Crear `data/presupuesto_ejecucion_2024.csv` extrayendo la tabla de ejecución del gasto de la página 4 de la Rendición de Cuentas 2024, con validación de totales y trazabilidad.

**Architecture:** `scripts/presupuesto_2024.py` descarga el PDF (a `data/_sin_versionar/`), extrae la tabla de la página 4 (texto/coordenadas), normaliza números, valida totales, escribe CSV. TDD con unittest.

**Tech Stack:** Python 3.10 (stdlib: urllib, csv, re), PyMuPDF (fitz) para parseo PDF.

---

## Contexto
- Repo `datos-publicos`. Fuente: `https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf` (18 págs comprimidas; tabla en página 4).
- Tabla verificada (investigación previa): NIVEL / OBJETO / VIGENTE / OBLIGADO / %EJEC.
- Valores esperados (millones Gs): total vigente 2.360.168, obligado 1.253.270, 53%.

---

### Task 1: `scripts/presupuesto_2024.py` (TDD)

**Files:**
- Create: `scripts/presupuesto_2024.py`
- Create: `scripts/tests/test_presupuesto_2024.py`

- [ ] **Step 1: Test que falla — parsing de una línea de la tabla**

```python
import unittest, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from presupuesto_2024 import parsear_fila, validar_totales, normalizar_numero

class TestParsear(unittest.TestCase):
    def test_normalizar_numero(self):
        self.assertEqual(normalizar_numero("788.089"), 788.089)
        self.assertEqual(normalizar_numero("1.253.270"), 1253270.0)
        self.assertEqual(normalizar_numero("53%"), None)  # no es monto
    def test_parsear_fila_validar_campos(self):
        f = parsear_fila(["100", "Servicios Personales", "788.089", "727.234", "92%"])
        self.assertEqual(f["nivel"], "100")
        self.assertEqual(f["denominacion"], "Servicios Personales")
        self.assertEqual(f["presupuesto_vigente"], 788.089)
        self.assertEqual(f["obligado"], 727.234)
        self.assertEqual(round(f["porcentaje_ejecucion"], 2), 92.29)
    def test_validar_totales_ok(self):
        filas = [
            {"nivel": "100", "presupuesto_vigente": 788.089, "obligado": 727.234},
            {"nivel": "200", "presupuesto_vigente": 232.517, "obligado": 114.346},
        ]
        errores = validar_totales(filas, total_vigente=1020.606, total_obligado=841.58)
        self.assertEqual(len(errores), 0)
    def test_validar_totales_roto(self):
        filas = [{"nivel": "100", "presupuesto_vigente": 1.0, "obligado": 1.0}]
        errores = validar_totales(filas, total_vigente=999.0, total_obligado=1.0)
        self.assertGreater(len(errores), 0)

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar, debe fallar** (ImportError).

- [ ] **Step 3: Implementar**

```python
import csv
import os
import re
import urllib.request

URL_PDF = "https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIN_VERSIONAR = os.path.join(ROOT, "data", "_sin_versionar")
PDF_LOCAL = os.path.join(SIN_VERSIONAR, "rendicion-cuentas-2024.pdf")
OUTPUT = os.path.join(ROOT, "data", "presupuesto_ejecucion_2024.csv")


def normalizar_numero(texto):
    txt = (texto or "").strip()
    if not txt or txt.endswith("%"):
        return None
    txt = txt.replace(".", "").replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return None


def parsear_fila(campos):
    nivel = (campos[0] or "").strip()
    denominacion = (campos[1] or "").strip()
    vigente = normalizar_numero(campos[2]) if len(campos) > 2 else None
    obligado = normalizar_numero(campos[3]) if len(campos) > 3 else None
    pct = obligado / vigente * 100 if (vigente and obligado is not None) else None
    return {
        "nivel": nivel,
        "denominacion": denominacion,
        "presupuesto_vigente": vigente,
        "obligado": obligado,
        "porcentaje_ejecucion": round(pct, 2) if pct is not None else None,
    }


def validar_totales(filas, total_vigente, total_obligado, tol=0.5):
    errores = []
    suma_v = sum(f["presupuesto_vigente"] or 0 for f in filas)
    suma_o = sum(f["obligado"] or 0 for f in filas)
    if abs(suma_v - total_vigente) > tol:
        errores.append(f"vigente: suma {suma_v:.1f} != total {total_vigente}")
    if abs(suma_o - total_obligado) > tol:
        errores.append(f"obligado: suma {suma_o:.1f} != total {total_obligado}")
    return errores
```

(El `__main__` completa: descarga PDF, extrae página con PyMuPDF, detecta filas por regex de nivel numérico, valida contra los totales esperados y escribe CSV.)

- [ ] **Step 4: Tests pasan.** `python -m unittest discover -s scripts/tests`

- [ ] **Step 5: Commit.** `git add scripts/presupuesto_2024.py scripts/tests/test_presupuesto_2024.py && git commit -m "feat: add budget execution 2024 extraction pipeline (TDD)"`

---

### Task 2: `__main__` real — extracción del PDF

**Files:**
- Modify: `scripts/presupuesto_2024.py`
- Add: lógica con PyMuPDF (`fitz`)

- [ ] **Step 1: Completar `__main__`**

```python
def extraer_tabla(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    pagina = doc[3]  # página 4
    texto = pagina.get_text()
    # dividir en líneas y detectar filas que empiezan con nivel numérico (100/200/...)
    filas = []
    for linea in texto.splitlines():
        m = re.match(r"^\s*(\d{3})\s+(.+?)\s+([\d.]+)\s+([\d.]+)?\s*(\d+%)?$", linea)
        if m:
            filas.append(parsear_fila([m.group(1), m.group(2), m.group(3), m.group(4) or ""]))
    return filas
```

- [ ] **Step 2: Probar extracción real** (con el PDF ya descargado local o descargando).

Fix del parseo si PyMuPDF intercala las celdas de forma distinta (flatten by layout/coordenadas como fallback).

- [ ] **Step 3: Commit.** `git add scripts/presupuesto_2024.py && git commit -m "feat: extract 2024 spending table from rendicion PDF (main)"`

---

### Task 3: Generar el dataset real y validar contra totales de la rendición

- [ ] Step 1: `python scripts/presupuesto_2024.py` → `data/presupuesto_ejecucion_2024.csv`.
- [ ] Step 2: Verificar valores:
```python
import csv; rows=list(csv.DictReader(open('data/presupuesto_ejecucion_2024.csv',encoding='utf-8')))
print(len(rows)); print(rows)
```
Expected: 7 filas de nivel + total, vigente suma 2.360.168, obligado 1.253.270.
- [ ] Step 3: Commit. `git add data/presupuesto_ejecucion_2024.csv && git commit -m "data: add budget execution 2024 dataset"`

---

### Task 4: docs + push

- [ ] Step 1: Commit spec/plan docs.
- [ ] Step 2: `git push`.
- [ ] Step 3: `python -m unittest discover -s scripts/tests` (todos OK).

---

## Criterios de éxito
- Tests de parsing/validación pasan.
- Dataset con 7 niveles + total, totales validados (2.360.168 / 1.253.270 / 53%).
- Trazabilidad (fuente, url).
- No inventa: columnas no disponibles declaradas en docs.