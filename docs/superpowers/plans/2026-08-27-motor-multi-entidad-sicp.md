# Datos Públicos — Motor multi-entidad por SICP — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Parametrizar `scripts/dncp_contrataciones.py` por SICP (entidad), manteniendo la Muni (108) como activa por defecto, sin romper la web/lab existentes.

**Architecture:** Reemplazar el filtro por nombre (`es_de_asuncion`) por un filtro por ID SICP (`es_entidad_por_sicp`); parametrizar `verificar_consistencia` y `main` por SICP; ampliar la CLI con un 2º argumento SICP (default "108"). TDD.

**Tech Stack:** Python 3.10 (stdlib), unittest.

---

## Contexto
- Repo `datos-publicos`. Motor actual: `scripts/dncp_contrataciones.py` (año parametrizado; entidad fija Muni por nombre).
- El flujo web consume `contrataciones_muni_{anio}.csv` → no cambiar el nombre del archivo para SICP 108.
- Tests existentes en `scripts/tests/test_dncp.py`.

---

### Task 1: Nuevo filtro por SICP (TDD)

**Files:**
- Modify: `scripts/dncp_contrataciones.py`
- Modify: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Test que falla — `es_entidad_por_sicp`**

Añadir en `test_dncp.py` (conservar `es_de_asuncion` por compatibilidad, pero los nuevos tests usan la nueva función):

```python
from dncp_contrataciones import es_entidad_por_sicp

class TestEsEntidadPorSicp(unittest.TestCase):
    def test_filtra_por_sicp_108(self):
        fila = {"compiledRelease/buyer/id": "DNCP-SICP-CODE-108"}
        self.assertTrue(es_entidad_por_sicp(fila, "108"))
    def test_rechaza_otro_sicp(self):
        fila = {"compiledRelease/buyer/id": "DNCP-SICP-CODE-226"}
        self.assertFalse(es_entidad_por_sicp(fila, "108"))
    def test_rechaza_sin_id(self):
        self.assertFalse(es_entidad_por_sicp({}, "108"))
```

- [ ] **Step 2: Ejecutar, debe fallar** (ImportError).

- [ ] **Step 3: Implementar** (reemplazar `es_de_asuncion` por la versión SICP al inicio del archivo):

```python
def es_entidad_por_sicp(fila, sicp):
    bid = (fila.get("compiledRelease/buyer/id") or "").strip()
    return bid == f"DNCP-SICP-CODE-{sicp}"
```

(Mantener `es_de_asuncion` solo si lo usan otros tests; los de `TestFiltrar` pueden seguir sobre `es_de_asuncion` o migrarse — decisión: conservar `es_de_asuncion` para no romper, pero delegar internamente.)

- [ ] **Step 4: Tests pasan.**

- [ ] **Step 5: Commit** — `git add scripts/dncp_contrataciones.py scripts/tests/test_dncp.py && git commit -m "feat: filter DNCP engine by SICP id (TDD)"`

---

### Task 2: Parametrizar verificación de consistencia

**Files:**
- Modify: `scripts/dncp_contrataciones.py`
- Modify: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Test que falla — `verificar_consistencia(filas, sicp)`**

```python
def test_consistencia_otra_entidad(self):
    filas = [
        {"compiledRelease/buyer/name": "Universidad Nacional de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-226"},
        {"compiledRelease/buyer/name": "Universidad Nacional de Asunción", "compiledRelease/buyer/id": "DNCP-SICP-CODE-226"},
        {"compiledRelease/buyer/name": "Ministerio de Salud", "compiledRelease/buyer/id": "DNCP-SICP-CODE-80"},
    ]
    ok, msg = verificar_consistencia(filas, sicp="226")
    self.assertTrue(ok)
    self.assertIn("2", msg)
```

- [ ] **Step 2: Implementar** — `verificar_consistencia(filas_records, sicp="108")`:

```python
def verificar_consistencia(filas_records, sicp="108"):
    esperado = f"DNCP-SICP-CODE-{sicp}"
    por_id = [r for r in filas_records if (r.get("compiledRelease/buyer/id") or "").strip() == esperado]
    por_nombre = [r for r in filas_records if es_de_asuncion(r.get("compiledRelease/buyer/name"))]
    # para entidad distinta a la Muni, usar el ID como primario y comparar por ID+nombre iguales
    iguales = len(por_id) == len(por_nombre) and not (
        {r.get("compiledRelease/id") for r in por_id} ^
        {r.get("compiledRelease/id") for r in por_nombre})
    msg = f"por SICP {sicp}: {len(por_id)} · por nombre: {len(por_nombre)}"
    return iguales, msg
```

(Nota: la comparación "por nombre" sigue usando `es_de_asuncion` porque es la entidad activa; para otras entidades la comprobación por nombre se ajustaría — se deja documentado que el primario es el ID.)

- [ ] **Step 3: Tests pasan.**

- [ ] **Step 4: Commit** — `git commit -m "feat: parametrize consistency check by SICP"`

---

### Task 3: `main(anio, sicp)` y CLI con SICP

**Files:**
- Modify: `scripts/dncp_contrataciones.py`
- Modify: `scripts/tests/test_dncp.py`

- [ ] **Step 1: Test que falla — `anio_sicp_desde_args`**

```python
from dncp_contrataciones import anio_sicp_desde_args

class TestArgsSicp(unittest.TestCase):
    def test_default_sicp_108(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2026"]), ("2026", "108"))
    def test_con_sicp(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2024", "226"]), ("2024", "226"))
    def test_con_sicp_solo(self):
        self.assertEqual(anio_sicp_desde_args(["x.py", "2026", "999"]), ("2026", "999"))
```

- [ ] **Step 2: Implementar**

```python
def anio_sicp_desde_args(args):
    anio = "2026"
    sicp = "108"
    if len(args) >= 2 and str(args[1]).isdigit():
        anio = args[1]
    if len(args) >= 3 and str(args[2]).isdigit():
        sicp = args[2]
    return anio, sicp
```

- [ ] **Step 3: Ajustar `main(anio="2026", sicp="108")`**:

```python
def main(anio="2026", sicp="108"):
    zip_path = descargar_zip(anio)
    print("Leyendo tablas ...")
    records = leer_tabla(zip_path, "records.csv")
    awards = indexar_awards(leer_tabla(zip_path, "awards.csv"))
    suppliers = indexar_suppliers(leer_tabla(zip_path, "awa_suppliers.csv"))
    contracts = indexar_contracts(leer_tabla(zip_path, "contracts.csv"))
    print(f"Total procesos {anio}: {len(records)}")
    ok, msg = verificar_consistencia(records, sicp)
    print(f"Verificación de consistencia: {msg} (estado: {'OK' if ok else 'ADVERTENCIA'})")
    entidad = [mapear_fila(f, awards, suppliers, contracts)
               for f in records if es_entidad_por_sicp(f, sicp)]
    errores = validar(entidad)
    if errores:
        print(f"Advertencias: {len(errores)}")
        for e in errores[:10]:
            print("  -", e)
    os.makedirs(DATA_DIR, exist_ok=True)
    # nombre de archivo: SICP 108 → muni (compat); otro → sicp
    sufijo = "muni" if sicp == "108" else f"ent{sicp}"
    out = os.path.join(DATA_DIR, f"contrataciones_{sufijo}_{anio}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_SALIDA)
        writer.writeheader()
        writer.writerows(entidad)
    print(f"Procesos entidad {sicp} {anio}: {len(entidad)}")
    print(f"Dataset escrito: {out}")
```

- [ ] **Step 4: Ajustar el `__main__`**:

```python
if __name__ == "__main__":
    anio, sicp = anio_sicp_desde_args(sys.argv)
    main(anio, sicp)
```

- [ ] **Step 5: Tests pasan** y `main` no se rompe (corrida manual verificada en Task 4).

- [ ] **Step 6: Commit** — `git commit -m "feat: accept SICP param in CLI (engine multi-entity)"`

---

### Task 4: Verificación real (Asunción intacta + otra entidad)

- [ ] **Step 1: Correr con SICP 108 (default, igual que antes)**

```bash
python scripts/dncp_contrataciones.py 2026
```
Expected: 36 procesos de la Muni; `data/contrataciones_muni_2026.csv` regenerado idéntico.

- [ ] **Step 2: Correr con otra entidad (SICP 226 — UNA)**

```bash
python scripts/dncp_contrataciones.py 2026 226
```
Expected: genera `data/contrataciones_ent226_2026.csv` con procesos de la UNA (número > 0). **No commiteamos este dataset** si es de otra entidad (decisión: solo lo verificamos; no es el foco activo).

- [ ] **Step 3: Verificar tests**

```bash
python -m unittest discover -s scripts/tests
```
Expected: todos OK.

- [ ] **Step 4: Commit** (labels/spec/plan) + push.

---

## Criterios de éxito
- `python scripts/dncp_contrataciones.py 2026` = igual que antes (Muni intacta).
- `.../2026 226` produce dataset de la UNA (motor general).
- Tests nuevos + existentes pasan.
- Web/lab no cambian (compat de archivo para SICP 108).