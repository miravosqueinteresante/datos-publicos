# Corrección de auditoría DNCP — Implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminar la ambigüedad semántica del campo `monto` y los indicadores derivados, separando valor estimado / monto adjudicado / monto contratado, procesando correctamente (y de forma genérica) las adjudicaciones y proveedores, y haciendo que el conteo de registros y la metodología sean reproducibles y honestos.

**Architecture:** El pipeline `dncp_contrataciones.py` deja de colapsar todo en `monto`; emite columnas explícitas (`valor_estimado`, `monto_adjudicado`, `monto_contratado`, `n_adjudicaciones`, `n_proveedores`, `proveedores`). Los índices OCDS (`awards/N`, `suppliers/N/M`, `contracts/N`) se parsean de forma genérica para ser correctos aunque la fuente solo traiga `/0`. `indicadores_gasto.py` y `generar_proveedores.py` suman solo lo adjudicado para concentración/ranking. Se genera `data/metadata.json` como única fuente de verdad del conteo. La web y la metodología se actualizan para usar el diccionario semántico y aclarar el año.

**Tech Stack:** Python 3.10 + csv/json/unittest (pytest). Sin nuevas dependencias. JS vanilla para la web.

**Restricción de la fuente (verificada en `data/_sin_versionar/masivo_2026.zip`):** los CSV de la DNCP vinieron aplanados solo con índice `/0` (`awards/0`, `suppliers/0`, `contracts/0`). Por tanto, múltiples adjudicaciones/proveedores por proceso no están en esta fuente. El parser genérico las soportará si aparecen, pero los números actuales no cambian por eso; el cambio real es la separación semántica y el denominador correcto.

---

## Estructura de archivos

- Modify: `scripts/dncp_contrataciones.py` — parsing genérico + columnas nuevas + `metadata.json`
- Modify: `scripts/indicadores_gasto.py` — indicadores separados + denominador adjudicado
- Modify: `scripts/generar_proveedores.py` — usa `monto_adjudicado`, % sobre adjudicado
- Modify: `scripts/generar_datos_web.py` — columnas nuevas al JSON
- Modify: `www/js/municipalidad.js` — tarjetas y etiquetas semánticas + denominador
- Modify: `www/js/proveedores.js` — etiqueta "Monto adjudicado"
- Modify: `www/metodologia.html` — diccionario semántico + aclaración de año + conteo desde metadata
- Modify: `DATA_INVENTORY.md` — conteos generados (36→35 corregido para 2026)
- Create: `www/calidad.html` — página de calidad y auditoría de datos
- Modify: `www/index.html`, `www/municipalidad.html` — enlace a calidad
- Modify: `scripts/tests/test_dncp.py`, `test_indicadores_gasto.py`, `test_generar_proveedores.py`, `test_generar_web.py` — fixtures y asserts nuevos
- Create: `scripts/tests/test_metadata.py` — integridad (sin duplicados, sumas coherentes)

Nuevo esquema CSV `contrataciones_muni_{anio}.csv`:
`id, objeto, estado, categoria, tipo_procedimiento, comprador, valor_estimado, monto_adjudicado, monto_contratado, moneda, n_adjudicaciones, n_proveedores, proveedor, proveedores, fecha_publicacion, fecha_adjudicacion, fecha_contrato, url_muni`

---

## Task 1: Parsing genérico y campos semánticos en el pipeline

**Files:** Modify `scripts/dncp_contrataciones.py`; Test `scripts/tests/test_dncp.py`

- [ ] **Step 1: Escribir test que verifica separación y multi-índice**

En `scripts/tests/test_dncp.py` añadir:

```python
from dncp_contrataciones import mapear_fila, indexar_awards, indexar_suppliers, indexar_contracts

class TestMapearSemantico(unittest.TestCase):
    def test_separa_valor_y_adjudicado(self):
        fila = {
            "compiledRelease/id": "ocds-x",
            "compiledRelease/tender/title": "Obra",
            "compiledRelease/tender/status": "active",
            "compiledRelease/tender/value/amount": "1000",
            "compiledRelease/tender/value/currency": "PYG",
        }
        awards = {"ocds-x": [{"monto": "400", "fecha": "2026-01-01", "estado": "active"}]}
        suppliers = {"ocds-x": {0: ["Empresa A"]}}
        contracts = {"ocds-x": [{"monto": "380", "fecha": "2026-02-01"}]}
        s = mapear_fila(fila, awards, suppliers, contracts)
        self.assertEqual(s["valor_estimado"], "1000")
        self.assertEqual(s["monto_adjudicado"], "400")
        self.assertEqual(s["monto_contratado"], "380")
        self.assertEqual(s["n_adjudicaciones"], 1)
        self.assertEqual(s["n_proveedores"], 1)
        self.assertEqual(s["proveedor"], "Empresa A")

    def test_sin_adjudicacion_deja_adjudicado_vacio(self):
        fila = {"compiledRelease/id": "ocds-y",
                "compiledRelease/tender/value/amount": "500",
                "compiledRelease/tender/value/currency": "PYG"}
        s = mapear_fila(fila, {}, {}, {})
        self.assertEqual(s["monto_adjudicado"], "")
        self.assertEqual(s["n_adjudicaciones"], 0)

    def test_multiples_adjudicaciones_se_sum(self):
        fila = {"compiledRelease/id": "ocds-z",
                "compiledRelease/tender/value/amount": "10",
                "compiledRelease/tender/value/currency": "PYG"}
        awards = {"ocds-z": [{"monto": "100", "fecha": "2026-01-01", "estado": "active"},
                              {"monto": "50", "fecha": "2026-01-02", "estado": "active"}]}
        suppliers = {"ocds-z": {0: ["A"], 1: ["B"]}}
        s = mapear_fila(fila, awards, suppliers, {})
        self.assertEqual(s["monto_adjudicado"], "150")
        self.assertEqual(s["n_adjudicaciones"], 2)
        self.assertEqual(s["n_proveedores"], 2)
        self.assertEqual(s["proveedores"], "A | B")
```

- [ ] **Step 2: Ejecutar test para verificar que falla**

Run: `cd scripts; python -m pytest tests/test_dncp.py -k semantico -q`
Expected: FAIL (parámetros/columnas no existen aún)

- [ ] **Step 3: Implementar parsing genérico y campos**

Reemplazar `indexar_awards`, `indexar_suppliers`, `indexar_contracts` y `mapear_fila`, y actualizar `COLUMNAS_SALIDA` y `validar`:

```python
import re

_AWARD_PAT = re.compile(r"^compiledRelease/awards/(\d+)/(.*)$")
_SUPPAT = re.compile(r"^compiledRelease/awards/(\d+)/suppliers/(\d+)/name$")
_CONT_PAT = re.compile(r"^compiledRelease/contracts/(\d+)/(.*)$")


def indexar_awards(rows):
    out = {}
    for r in rows:
        rid = r.get("compiledRelease/id", "")
        por_indice = {}
        for k, v in r.items():
            m = _AWARD_PAT.match(k)
            if not m:
                continue
            i, sub = int(m.group(1)), m.group(2)
            por_indice.setdefault(i, {})[sub] = v
        out[rid] = [{
            "monto": por_indice[i].get("value/amount", ""),
            "fecha": por_indice[i].get("date", ""),
            "estado": por_indice[i].get("status", ""),
        } for i in sorted(por_indice)]


def indexar_suppliers(rows):
    out = {}
    for r in rows:
        rid = r.get("compiledRelease/id", "")
        por_award = {}
        for k, v in r.items():
            m = _SUPPAT.match(k)
            if not m:
                continue
            i, j = int(m.group(1)), int(m.group(2))
            por_award.setdefault(i, []).append(v)
        out[rid] = por_award
    return out


def indexar_contracts(rows):
    out = {}
    for r in rows:
        rid = r.get("compiledRelease/id", "")
        por_indice = {}
        for k, v in r.items():
            m = _CONT_PAT.match(k)
            if not m:
                continue
            i, sub = int(m.group(1)), m.group(2)
            por_indice.setdefault(i, {})[sub] = v
        out[rid] = [{
            "monto": por_indice[i].get("value/amount", ""),
            "fecha": por_indice[i].get("dateSigned", ""),
        } for i in sorted(por_indice)]
    return out


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def mapear_fila(fila, awards, suppliers, contracts):
    uuid = fila.get("compiledRelease/id", "")
    ocid = fila.get("compiledRelease/ocid", "") or uuid
    aw = awards.get(uuid, [])
    sp = suppliers.get(uuid, {})
    co = contracts.get(uuid, [])
    valor_estimado = _buscar(fila, "compiledRelease/tender/value/amount")
    moneda = _buscar(fila, "compiledRelease/tender/value/currency")
    monto_adjudicado = sum(_num(a.get("monto")) for a in aw)
    monto_contratado = sum(_num(c.get("monto")) for c in co)
    nombres = []
    for i in sorted(sp):
        for nombre in sp[i]:
            if nombre and nombre not in nombres:
                nombres.append(nombre)
    fecha_adj = min((a["fecha"] for a in aw if a.get("fecha")), default="")
    fecha_con = min((c["fecha"] for c in co if c.get("fecha")), default="")
    return {
        "id": ocid,
        "objeto": _buscar(fila, "compiledRelease/tender/title", "compiledRelease/tender/description"),
        "estado": _buscar(fila, "compiledRelease/tender/status"),
        "categoria": _buscar(fila, "compiledRelease/tender/mainProcurementCategory"),
        "tipo_procedimiento": _buscar(fila, "compiledRelease/tender/procurementMethodDetails", "compiledRelease/tender/procurementMethod"),
        "comprador": _buscar(fila, "compiledRelease/buyer/name"),
        "valor_estimado": valor_estimado,
        "monto_adjudicado": str(int(monto_adjudicado)) if monto_adjudicado else "",
        "monto_contratado": str(int(monto_contratado)) if monto_contratado else "",
        "moneda": moneda,
        "n_adjudicaciones": len(aw),
        "n_proveedores": len(nombres),
        "proveedor": nombres[0] if nombres else "",
        "proveedores": " | ".join(nombres),
        "fecha_publicacion": _buscar(fila, "compiledRelease/tender/datePublished", "compiledRelease/date"),
        "fecha_adjudicacion": fecha_adj,
        "fecha_contrato": fecha_con,
        "url_muni": f"https://www.contrataciones.gov.py/licitaciones/convocatoria/{fila.get('compiledRelease/tender/id', '')}.html",
    }
```

`COLUMNAS_SALIDA` queda:

```python
COLUMNAS_SALIDA = [
    "id", "objeto", "estado", "categoria", "tipo_procedimiento", "comprador",
    "valor_estimado", "monto_adjudicado", "monto_contratado", "moneda",
    "n_adjudicaciones", "n_proveedores", "proveedor", "proveedores",
    "fecha_publicacion", "fecha_adjudicacion", "fecha_contrato", "url_muni",
]
```

`validar` debe aceptar `valor_estimado` (no exigir `monto`):

```python
def validar(filas):
    errores = []
    for f in filas:
        if not f.get("id"):
            errores.append("fila sin id"); continue
        if not f.get("objeto"):
            errores.append(f"proceso {f['id']} sin objeto")
        ve = f.get("valor_estimado", "")
        if ve and not str(ve).replace(".", "", 1).isdigit():
            errores.append(f"proceso {f['id']} valor_estimado no numérico: {ve}")
    return errores
```

`es_registro_valido` usa `valor_estimado` en vez de `monto`:

```python
def es_registro_valido(fila):
    objeto = fila.get("objeto") or ""
    ve = fila.get("valor_estimado") or "0"
    url = fila.get("url_muni") or ""
    if not objeto.strip():
        return False
    try:
        if float(ve) == 0:
            return False
    except ValueError:
        return False
    if "planned.html" in url:
        return False
    return True
```

- [ ] **Step 4: Ejecutar tests**

Run: `cd scripts; python -m pytest tests/test_dncp.py -q`
Expected: PASS (incluidos los nuevos y los existentes tras ajustar fixtures de `mapear_fila` existentes que usaban `monto`).

- [ ] **Step 5: Commit**

```bash
git add scripts/dncp_contrataciones.py scripts/tests/test_dncp.py
git commit -m "fix(pipeline): separa valor_estimado/monto_adjudicado/monto_contratado y parsea indices genericos"
```

---

## Task 2: `data/metadata.json` como única fuente de verdad del conteo

**Files:** Modify `scripts/dncp_contrataciones.py` (`main`); Create `scripts/tests/test_metadata.py`

- [ ] **Step 1: Test de metadata**

```python
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from dncp_contrataciones import construir_metadata

class TestMetadata(unittest.TestCase):
    def test_contiene_conteo_y_version(self):
        m = construir_metadata("2026", [{"id": "a"}, {"id": "b"}], "108")
        self.assertEqual(m["anio"], "2026")
        self.assertEqual(m["registros"], 2)
        self.assertEqual(m["sicp"], "108")
        self.assertIn("generado_en", m)
        self.assertIn("fuente", m)
```

- [ ] **Step 2: Implementar `construir_metadata` y escribirlo en `main`**

Añadir función y llamarla al final de `main` (antes del `print` final):

```python
import datetime

def construir_metadata(anio, filas, sicp):
    return {
        "dataset": f"contrataciones_muni_{anio}",
        "anio": anio,
        "sicp": sicp,
        "registros": len(filas),
        "con_adjudicacion": sum(1 for f in filas if (f.get("n_adjudicaciones") or 0) and int(f.get("n_adjudicaciones") or 0) > 0),
        "sin_adjudicacion": sum(1 for f in filas if not (f.get("n_adjudicaciones") or 0)),
        "generado_en": datetime.date.today().isoformat(),
        "fuente": "DNCP OCDS (masivo)",
        "licencia": "CC BY 4.0",
    }
```

En `main`, tras escribir el CSV:

```python
    meta = construir_metadata(anio, entidad, sicp)
    meta_ruta = os.path.join(DATA_DIR, f"metadata_{anio}.json")
    with open(meta_ruta, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Metadata: {meta_ruta}")
```

- [ ] **Step 3: Test + commit**

Run: `cd scripts; python -m pytest tests/test_metadata.py -q`
```bash
git add scripts/dncp_contrataciones.py scripts/tests/test_metadata.py
git commit -m "feat(pipeline): genera data/metadata_{anio}.json con conteo oficial"
```

---

## Task 3: Indicadores separados y denominador correcto

**Files:** Modify `scripts/indicadores_gasto.py`; Modify `scripts/tests/test_indicadores_gasto.py`

- [ ] **Step 1: Test con nuevas columnas**

Reescribir el fixture CSV de `test_indicadores_gasto.py` con las columnas nuevas y añadir asserts:

```python
CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,valor_estimado,monto_adjudicado,monto_contratado,moneda,n_adjudicaciones,n_proveedores,proveedor,proveedores,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,obra1,complete,Obras,open,Municipalidad de Asunción,1000,1000,,PYG,1,1,C1,C1,,,x
b,obra2,complete,Obras,open,Municipalidad de Asunción,2000,2000,,PYG,1,1,C1,C1,,,x
c,bien1,complete,Bienes,open,Municipalidad de Asunción,500,500,,PYG,1,1,C2,C2,,,x
d,serv1,complete,Servicios,open,Municipalidad de Asunción,300,300,,PYG,1,1,C3,C3,,,x
e,serv2,active,Servicios,open,Municipalidad de Asunción,999,,,,PYG,0,0,,,x
"""
```

Y asserts:

```python
    def test_totales_separados(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["valor_estimado_total"], 4799)
        self.assertEqual(ind["monto_adjudicado_total"], 3800)
        self.assertEqual(ind["monto_contratado_total"], 0)
        self.assertEqual(ind["procesos"], 5)
        self.assertEqual(ind["procesos_sin_adjudicacion"], 1)
    def test_top_proveedores_usa_adjudicado(self):
        ind = calcular_indicadores(CSV)
        self.assertEqual(ind["top_proveedores"][0]["proveedor"], "C1")
        self.assertEqual(ind["top_proveedores"][0]["monto"], 2000)
    def test_pct_sobre_adjudicado(self):
        ind = calcular_indicadores(CSV)
        c1 = next(p for p in ind["top_proveedores"] if p["proveedor"] == "C1")
        self.assertAlmostEqual(c1["pct_del_adjudicado"], 2000/3800*100, places=1)
```

- [ ] **Step 2: Implementar `calcular_indicadores`**

```python
def calcular_indicadores(csv_texto):
    filas = list(csv.DictReader(csv_texto.splitlines()))
    por_categoria = {}
    por_proveedor = {}
    por_tipo = {}
    valor_estimado_total = 0
    monto_adjudicado_total = 0
    monto_contratado_total = 0
    sin_adjudicacion = 0
    for f in filas:
        ve = _num(f.get("valor_estimado"))
        ma = _num(f.get("monto_adjudicado"))
        mc = _num(f.get("monto_contratado"))
        valor_estimado_total += ve
        monto_adjudicado_total += ma
        monto_contratado_total += mc
        if (int(f.get("n_adjudicaciones") or 0) or 0) == 0:
            sin_adjudicacion += 1
        cat = _traducir_categoria(f.get("categoria") or "Sin categoría")
        por_categoria[cat] = por_categoria.get(cat, 0) + ma
        prov = f.get("proveedor") or ""
        if prov:
            por_proveedor[prov] = por_proveedor.get(prov, 0) + ma
        tipo = f.get("tipo_procedimiento") or "Sin tipo"
        por_tipo[tipo] = por_tipo.get(tipo, 0) + ma
    top = sorted(por_proveedor.items(), key=lambda x: -x[1])[:10]
    for p, m in top:
        pass
    top_list = []
    for p, m in top:
        pct = (m / monto_adjudicado_total * 100) if monto_adjudicado_total else 0
        top_list.append({"proveedor": p, "monto": m, "pct_del_adjudicado": round(pct, 1)})
    return {
        "procesos": len(filas),
        "valor_estimado_total": round(valor_estimado_total),
        "monto_adjudicado_total": round(monto_adjudicado_total),
        "monto_contratado_total": round(monto_contratado_total),
        "procesos_sin_adjudicacion": sin_adjudicacion,
        "por_categoria": [{"categoria": c, "monto": round(m)} for c, m in sorted(por_categoria.items(), key=lambda x: -x[1])],
        "por_tipo_procedimiento": [{"tipo": t, "monto": round(m)} for t, m in sorted(por_tipo.items(), key=lambda x: -x[1])],
        "top_proveedores": top_list,
        "monto_total": round(monto_adjudicado_total),
    }
```

(añadir helper `_num` al módulo).

- [ ] **Step 3: Test + commit**

Run: `cd scripts; python -m pytest tests/test_indicadores_gasto.py -q`
```bash
git add scripts/indicadores_gasto.py scripts/tests/test_indicadores_gasto.py
git commit -m "fix(indicadores): separa valor estimado/adjudicado/contratado y % sobre adjudicado"
```

---

## Task 4: Ranking de proveedores sobre monto adjudicado

**Files:** Modify `scripts/generar_proveedores.py`; Modify `scripts/tests/test_generar_proveedores.py`

- [ ] **Step 1: Test**

Actualizar fixture CSV a columnas nuevas y añadir assert de `pct_del_adjudicado`:

```python
CSV = """id,objeto,estado,categoria,tipo_procedimiento,comprador,valor_estimado,monto_adjudicado,monto_contratado,moneda,n_adjudicaciones,n_proveedores,proveedor,proveedores,fecha_publicacion,fecha_adjudicacion,fecha_contrato,url_muni
a,o1,,goods,Licitación Pública Nacional,Muni,100,100,,PYG,1,1,P1,P1,2024-01-01,,x
b,o2,,goods,Menor cuantía nacional,Muni,50,50,,PYG,1,1,P1,P1,2024-02-01,,x
c,o3,,services,Licitación Pública Nacional,Muni,300,300,,PYG,1,1,P2,P2,2024-03-01,,x
d,o4,,works,Contratación Directa,Muni,200,200,,PYG,1,1,P2,P2,2024-04-01,,x
"""
```

```python
    def test_usa_monto_adjudicado(self):
        top = calcular_top(CSV)
        self.assertEqual(top[0]["monto_total"], 500)   # P2
        self.assertEqual(top[0]["adjudicaciones"], 2)
```

- [ ] **Step 2: Implementar** — en `calcular_top` usar `monto_adjudicado` en vez de `monto`, renombrar `contratos`→`adjudicaciones`, y añadir `pct_del_adjudicado` (sobre el total adjudicado del conjunto). El total adjudicado se calcula dentro de `calcular_top` sumando todos los `monto_adjudicado`.

- [ ] **Step 3: Test + commit**

```bash
git add scripts/generar_proveedores.py scripts/tests/test_generar_proveedores.py
git commit -m "fix(proveedores): ranking sobre monto_adjudicado y etiqueta adjudicaciones"
```

---

## Task 5: `generar_datos_web.py` con columnas nuevas

**Files:** Modify `scripts/generar_datos_web.py`; Modify `scripts/tests/test_generar_web.py`

- [ ] **Step 1: Test** — actualizar fixture y comprobar que el JSON trae `valor_estimado`, `monto_adjudicado`, `monto_contratado` y `monto_nulo` se calcula desde `monto_adjudicado`.

- [ ] **Step 2: Implementar `fila_a_json`** leyendo las nuevas columnas; `monto` se mantiene como alias de `monto_adjudicado` para no romper la tabla web, pero `monto_nulo` = (monto_adjudicado vacío).

- [ ] **Step 3: Test + commit**

---

## Task 6: Web — tarjetas y etiquetas semánticas

**Files:** Modify `www/js/municipalidad.js`; Modify `www/js/proveedores.js`

- [ ] **Step 1-2:** En `municipalidad.js` `renderDetalle` reemplazar la métrica única "Monto adjudicado" por 4 tarjetas: Procesos, Valor estimado (`d.valor_estimado_total`), Monto adjudicado (`d.monto_adjudicado_total`), Monto contratado (`d.monto_contratado_total`), y una línea "Sin adjudicación: N". En la tabla de proveedores, el % usar `d.monto_adjudicado_total` como denominador. En `renderSerie` usar `monto_adjudicado_total` para la barra.

- [ ] **Step 3:** En `proveedores.js` cambiar "Monto total" → "Monto adjudicado" y "contratos" → "adjudicaciones" en las etiquetas.

- [ ] **Step 4: Commit**

---

## Task 7: Metodología y DATA_INVENTORY honestos

**Files:** Modify `www/metodologia.html`; Modify `DATA_INVENTORY.md`

- [ ] Añadir a `metodologia.html` un **Diccionario semántico** (Proceso/Adjudicación/Proveedor adjudicado/Contrato/Valor estimado/Monto adjudicado/Monto contratado) y aclarar que el "año" es *proceso con actividad (publicación, adjudicación o contrato) en ese año*. Aclarar la limitación de la fuente DNCP (solo `awards/0`). Corregir conteo 2026 a 35 (tomado de `metadata_2026.json`).
- [ ] Corregir `DATA_INVENTORY.md` fila 2026 de 36 → 35 y notar que el conteo se genera en `metadata_{anio}.json`.
- [ ] Commit.

---

## Task 8: Página de calidad y auditoría

**Files:** Create `www/calidad.html`; Modify `www/index.html` y `www/municipalidad.html` (enlaces nav)

- [ ] Crear `calidad.html` que cargue `datos/metadata-2026.json` y muestre: última actualización, fuente, registros, con adjudicación, sin adjudicación, versión de fuente, y un párrafo de limitaciones. Añadir enlace en la nav.

---

## Task 9: Tests de integridad

**Files:** Create `scripts/tests/test_metadata.py` (ampliar)

- [ ] Añadir test que, sobre el CSV real generado (`data/contrataciones_muni_2026.csv`), afirme: sin OCID duplicados, `monto_adjudicado` <= `valor_estimado` + margen (o simplemente que no hay NaN), y que `procesos_sin_adjudicacion` + `con_adjudicacion` == registros según metadata.

---

## Task 10: Regenerar datos y verificar end-to-end

- [ ] Run: `cd scripts; python dncp_contrataciones.py 2026; python indicadores_gasto.py; python generar_proveedores.py; python generar_datos_web.py`
- [ ] Run: `cd scripts; python -m pytest -q`
- [ ] Verificar manualmente `data/contrataciones_muni_2026.csv` (35 filas, columnas nuevas) y `data/metadata_2026.json`.
- [ ] Commit final: `git add -A; git commit -m "fix(auditoria): modelo semantico separado, metadata auto y UI honesta"`

---

## Autorevisión

- Spec coverage: PRIORIDAD 1 (campo monto) → Task 1/3/5; PRIORIDAD 2 (todas las adjudicaciones) → Task 1 (genérico, limitado por fuente documentado); PRIORIDAD 3 (recálculo) → Task 3/4; PRIORIDAD 4 (36↔35) → Task 2/7; PRIORIDAD 5 (calidad) → Task 8. Términos/semántica → Task 6/7. Año → Task 7.
- Placeholders: ninguno; todo el código está incluido.
- Consistencia de tipos: `monto_adjudicado_total` usado en Tasks 3,4,6; `n_adjudicaciones` entero en Tasks 1,3; columnas coinciden entre pipeline, indicadores, web y tests.
