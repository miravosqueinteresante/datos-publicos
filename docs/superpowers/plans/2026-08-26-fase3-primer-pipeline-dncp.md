# Datos Públicos — FASE 3: Primer pipeline DNCP — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir el primer pipeline de datos de punta a punta: descargar los procesos de contratación de la Municipalidad de Asunción desde la DNCP, filtrar, limpiar y validar, produciendo `data/contrataciones_muni_2026.csv`.

**Architecture:** Script Python único (`scripts/dncp_contrataciones.py`) con funciones puras testables (parsing/filtro/limpieza) y un `__main__` que ejecuta el flujo completo (descargar ZIP → extraer records.csv → filtrar Muni → mapear columnas → validar → escribir CSV). Proceso manual primero.

**Tech Stack:** Python 3.10 (std: `zipfile`, `csv`, `urllib.request` — sin dependencias externas por ahora). Tests con `unittest` (stdlib, sin framework).

---

## Contexto

- Repo `datos-publicos`, raíz `C:\Users\pc\Desktop\Proyectos\Datos Publicos`, rama `main`.
- Fuente evaluada (FASE 2): CSV masivos DNCP, `masivo.zip` por año, módulo recs, año 2026.
- URL: `https://www.contrataciones.gov.py/images/opendata-v3/final/ocds/2026/masivo.zip`
- Ref: 70 procesos de la Muni en records.csv 2026 (nombres de columna OCDS: `compiledRelease/...`, con `buyer/name`).
- Se instala Python 3.10 (verificado en sesión). No hay pip de dependencias necesarias.

## Estructura de archivos

- `scripts/dncp_contrataciones.py` — pipeline completo.
- `scripts/tests/test_dncp.py` — tests unitarios (stdlib unittest).
- `data/contrataciones_muni_2026.csv` — dataset resultante (versionado).
- `.gitignore` — añadir `data/_sin_versionar/`.

## Esquema real verificado (26-ago-2026, tras inspección del ZIP)

El `masivo.zip` de un año contiene muchas tablas OCDS. Para el dataset de la Muni unimos **4 tablas por `compiledRelease/id` (OCID)**:

| Tabla | Columnas clave | Uso |
|---|---|---|
| `records.csv` | `compiledRelease/id`, `tender/title`, `tender/status`, `tender/mainProcurementCategory`, `tender/procurementMethod`, `tender/procurementMethodDetails`, `tender/value/amount`, `tender/value/currency`, `tender/datePublished`, `buyer/id`, `buyer/name` | Proceso (objeto, estado, categoría, valor referencial, fecha pública, comprador) |
| `awards.csv` | `compiledRelease/id`, `awards/0/status`, `awards/0/date`, `awards/0/value/amount`, `awards/0/value/currency` | Monto y fecha de adjudicación |
| `awa_suppliers.csv` | `compiledRelease/id`, `awards/0/id`, `awards/0/suppliers/0/id`, `awards/0/suppliers/0/name` | Nombre del proveedor adjudicado |
| `contracts.csv` | `compiledRelease/id`, `contracts/0/dateSigned`, `contracts/0/value/amount`, `contracts/0/status` | Fecha y monto de contrato |

Filtro por municipio: `records.csv` `compiledRelease/buyer/name` contiene "Municipalidad de Asunción" (o `buyer/id` == 108).

Nota: `records.csv` devuelve el **llamado** (sin proveedor/monto de adjudicación); esos campos se cruzan desde `awards.csv` + `awa_suppliers.csv` + `contracts.csv`.

---

### Task 1: Esqueleto del script + función de filtración por comprador

**Files:**
- Create: `scripts/dncp_contrataciones.py`
- Create: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Escribir el test que falla — filtración por comprador**

```python
import unittest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import es_de_asuncion

class TestFiltrar(unittest.TestCase):
    def test_nombre_municipalidad(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asuncion"))
    def test_nombre_con_tilde(self):
        self.assertTrue(es_de_asuncion("Municipalidad de Asunción"))
    def test_no_es_otro_org(self):
        self.assertFalse(es_de_asuncion("Ministerio de Salud Pública"))
    def test_no_universidad(self):
        self.assertFalse(es_de_asuncion("Universidad Nacional de Asunción"))

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Ejecutar el test, debe fallar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: FAIL con `ModuleNotFoundError: No module named 'dncp_contrataciones'`.

- [ ] **Step 3: Implementar la función**

En `scripts/dncp_contrataciones.py`:

```python
def es_de_asuncion(texto):
    if not texto:
        return False
    t = texto.lower().replace("á", "a")
    return "municipalidad de asuncion" in t
```

- [ ] **Step 4: Ejecutar los tests, deben pasar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 4 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/dncp_contrataciones.py scripts/tests/test_dncp.py
git commit -m "feat: add DNCP pipeline stub with buyer filter (TDD)"
```

---

### Task 2: Mapeo y extracción de columnas (join por OCID: records + awards + suppliers + contracts)

**Files:**
- Modify: `scripts/dncp_contrataciones.py`
- Modify: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Escribir el test que falla — mapeo de columnas OCDS**

En `scripts/tests/test_dncp.py`, añadir:

```python
from dncp_contrataciones import mapear_fila

class TestMapear(unittest.TestCase):
    def test_extrae_campos_clave(self):
        fila = {
            "compiledRelease/id": "ocds-03ad3f-999",
            "compiledRelease/tender/title": "Construcción de vereda",
            "compiledRelease/tender/status": "active",
            "compiledRelease/buyer/name": "Municipalidad de Asuncion",
            "compiledRelease/tender/value/amount": "150000000",
            "compiledRelease/tender/value/currency": "PYG",
        }
        salida = mapear_fila(fila, {}, {}, {})
        self.assertEqual(salida["id"], "ocds-03ad3f-999")
        self.assertEqual(salida["objeto"], "Construcción de vereda")
        self.assertEqual(salida["monto"], "150000000")
    def test_campos_faltantes_quedan_vacios(self):
        salida = mapear_fila({"compiledRelease/id": "x"}, {}, {}, {})
        self.assertEqual(salida["objeto"], "")
```

- [ ] **Step 2: Ejecutar tests, deben fallar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: FAIL con `ImportError: cannot import name 'mapear_fila'`.

- [ ] **Step 3: Implementar `mapear_fila`**

El join se hace ANTES: los índices `awards`, `suppliers` y `contracts` son dicts `{ocid: valor}`. La función recibe la fila de records + los 3 índices.

En `scripts/dncp_contrataciones.py` añadir:

```python
COLUMNAS_SALIDA = [
    "id", "objeto", "estado", "categoria", "tipo_procedimiento",
    "comprador", "proveedor", "monto", "moneda",
    "fecha_publicacion", "fecha_adjudicacion", "fecha_contrato", "url_muni",
]

def _buscar(fila, *rutas):
    for r in rutas:
        if fila.get(r):
            return fila[r]
    return ""

def mapear_fila(fila, awards, suppliers, contracts):
    ocid = fila.get("compiledRelease/id", "")
    aw, sp, co = awards.get(ocid, {}), suppliers.get(ocid, {}), contracts.get(ocid, {})
    return {
        "id": ocid,
        "objeto": _buscar(fila, "compiledRelease/tender/title",
                          "compiledRelease/tender/description"),
        "estado": _buscar(fila, "compiledRelease/tender/status"),
        "categoria": _buscar(fila, "compiledRelease/tender/mainProcurementCategory"),
        "tipo_procedimiento": _buscar(fila, "compiledRelease/tender/procurementMethod",
                                      "compiledRelease/tender/procurementMethodDetails"),
        "comprador": _buscar(fila, "compiledRelease/buyer/name"),
        "proveedor": sp.get("proveedor", ""),
        "monto": aw.get("monto", "") or _buscar(fila, "compiledRelease/tender/value/amount"),
        "moneda": aw.get("moneda", "") or _buscar(fila, "compiledRelease/tender/value/currency"),
        "fecha_publicacion": _buscar(fila, "compiledRelease/tender/datePublished",
                                     "compiledRelease/date"),
        "fecha_adjudicacion": aw.get("fecha", ""),
        "fecha_contrato": co.get("fecha", ""),
        "url_muni": f"https://www.contrataciones.gov.py/datos/adquisiciones/{ocid}",
    }
```

- [ ] **Step 4: Ejecutar tests, deben pasar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/dncp_contrataciones.py scripts/tests/test_dncp.py
git commit -m "feat: map OCDS columns to flat CSV output (TDD)"
```

---

### Task 3: Función de validación del dataset

**Files:**
- Modify: `scripts/dncp_contrataciones.py`
- Modify: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Test que falla — validación**

```python
from dncp_contrataciones import validar

class TestValidar(unittest.TestCase):
    def test_filas_validas(self):
        filas = [
            {"id": "a", "objeto": "ob", "monto": "150"},
            {"id": "b", "objeto": "ob2", "monto": "300"},
        ]
        errores = validar(filas)
        self.assertEqual(len(errores), 0)
    def test_detecta_id_vacio(self):
        filas = [{"id": "", "objeto": "ob"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_objeto_vacio(self):
        filas = [{"id": "a", "objeto": ""}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
    def test_detecta_monto_no_numerico(self):
        filas = [{"id": "a", "objeto": "ob", "monto": "ABC"}]
        errores = validar(filas)
        self.assertEqual(len(errores), 1)
```

- [ ] **Step 2: Ejecutar tests, deben fallar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: FAIL con `ImportError: cannot import name 'validar'`.

- [ ] **Step 3: Implementar `validar`**

```python
def validar(filas):
    errores = []
    for f in filas:
        if not f["id"]:
            errores.append("fila sin id")
            continue
        if not f["objeto"]:
            errores.append(f"proceso {f['id']} sin objeto")
        if f["monto"] and not str(f["monto"]).replace(".", "", 1).isdigit():
            errores.append(f"proceso {f['id']} monto no numérico: {f['monto']}")
    return errores
```

- [ ] **Step 4: Ejecutar tests, deben pasar**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 10 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/dncp_contrataciones.py scripts/tests/test_dncp.py
git commit -m "feat: add dataset validation (TDD)"
```

---

### Task 4: `__main__` — flujo completo descarga-filtro-join-salida

**Files:**
- Modify: `scripts/dncp_contrataciones.py`

- [ ] **Step 1: Implementar `__main__` y funciones auxiliares**

En `scripts/dncp_contrataciones.py`, añadir:

```python
import csv, os, urllib.request, zipfile

URL_BASE = "https://www.contrataciones.gov.py/images/opendata-v3/final/ocds"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SIN_VERSIONAR = os.path.join(DATA_DIR, "_sin_versionar")

def descargar_zip(anio="2026", destino=SIN_VERSIONAR):
    os.makedirs(destino, exist_ok=True)
    zip_path = os.path.join(destino, f"masivo_{anio}.zip")
    if not os.path.exists(zip_path):
        url = f"{URL_BASE}/{anio}/masivo.zip"
        print(f"Descargando {url} ...")
        urllib.request.urlretrieve(url, zip_path)
    return zip_path

def leer_tabla(zip_path, nombre):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(nombre) as f:
            buf = f.read().decode("utf-8").splitlines()
    header = buf[0].split(",")
    return [dict(zip(header, ln.split(",", len(header) - 1))) for ln in buf[1:]]

def indexar_awards(rows):
    out = {}
    for r in rows:
        out[r.get("compiledRelease/id", "")] = {
            "monto": r.get("compiledRelease/awards/0/value/amount", ""),
            "moneda": r.get("compiledRelease/awards/0/value/currency", ""),
            "fecha": r.get("compiledRelease/awards/0/date", ""),
        }
    return out

def indexar_suppliers(rows):
    out = {}
    for r in rows:
        out[r.get("compiledRelease/id", "")] = {
            "proveedor": r.get("compiledRelease/awards/0/suppliers/0/name", ""),
        }
    return out

def indexar_contracts(rows):
    out = {}
    for r in rows:
        out[r.get("compiledRelease/id", "")] = {
            "fecha": r.get("compiledRelease/contracts/0/dateSigned", ""),
        }
    return out

def main(anio="2026"):
    zip_path = descargar_zip(anio)
    print("Leyendo tablas ...")
    records = leer_tabla(zip_path, "records.csv")
    awards = indexar_awards(leer_tabla(zip_path, "awards.csv"))
    suppliers = indexar_suppliers(leer_tabla(zip_path, "awa_suppliers.csv"))
    contracts = indexar_contracts(leer_tabla(zip_path, "contracts.csv"))
    print(f"Total procesos {anio}: {len(records)}")
    muni = [mapear_fila(f, awards, suppliers, contracts)
            for f in records if es_de_asuncion(f.get("compiledRelease/buyer/name", ""))]
    errores = validar(muni)
    if errores:
        print(f"Advertencias: {len(errores)}")
        for e in errores[:10]:
            print("  -", e)
    os.makedirs(DATA_DIR, exist_ok=True)
    out = os.path.join(DATA_DIR, f"contrataciones_muni_{anio}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_SALIDA)
        writer.writeheader()
        writer.writerows(muni)
    print(f"Procesos de la Muni {anio}: {len(muni)}")
    print(f"Dataset escrito: {out}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Ejecutar los tests — deben seguir pasando**

```bash
python -m unittest discover -s scripts/tests
```
Expected: 10 tests PASS (sin romper).

- [ ] **Step 3: Commit**

```bash
git add scripts/dncp_contrataciones.py .gitignore
git commit -m "feat: add DNCP pipeline main flow (download, filter, join, output)"
```

- [ ] **Step 4: Añadir `data/_sin_versionar/` a `.gitignore`**

Asegurar que `.gitignore` contiene:

```gitignore
# Datos sin versionar (ZIP/descargas)
data/_sin_versionar/
```

Commit:
```bash
git add .gitignore
git commit -m "chore: ignore unversioned downloaded data"
```

---

### Task 5: Ejecución real del pipeline y validación del dataset

**Files:**
- Create: `data/contrataciones_muni_2026.csv` (generado)

- [ ] **Step 1: Ejecutar el pipeline en modo real**

```bash
python scripts/dncp_contrataciones.py
```
Expected: descarga el ZIP 2026, extrae records.csv (5.951 filas), y escribe `data/contrataciones_muni_2026.csv` con **≥ 60 procesos** de la Muni (referencia FASE 2: 70).

- [ ] **Step 2: Verificar el dataset de salida**

```bash
python -c "import csv; rows=list(csv.DictReader(open('data/contrataciones_muni_2026.csv',encoding='utf-8'))); print('filas:', len(rows)); print('con id:', sum(1 for r in rows if r['id'])); print('con objeto:', sum(1 for r in rows if r['objeto'])); print('con proveedor:', sum(1 for r in rows if r['proveedor']))"
```
Expected: filas ≥ 60; con_id == filas; con_objeto == filas; con_proveedor ~mayoría.

- [ ] **Step 3: Commit del dataset**

```bash
git add data/contrataciones_muni_2026.csv
git commit -m "data: add Asuncion contracts dataset 2026 (from DNCP, CC BY 4.0)"
```

- [ ] **Step 4: Push**

```bash
git push
```

---

## Criterios de éxito (verificación final)

- `scripts/dncp_contrataciones.py` corre de inicio a fin y produce el dataset.
- `data/contrataciones_muni_2026.csv` versionado con ≥ 60 procesos de la Muni.
- Tests pasan (10 tests).
- CSV plano, legible, con trazabilidad (URL y fecha en el plan/README del dataset).
- El ZIP queda en `data/_sin_versionar/` (ignorado por git).
- Sin dependencias externas (solo stdlib).