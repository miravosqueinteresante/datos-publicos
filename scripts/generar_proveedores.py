import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
WEB_DATOS = os.path.join(ROOT, "www", "datos")
ANIOS = ["2023", "2024", "2025", "2026"]


CATEGORIAS_ES = {"goods": "Bienes", "services": "Servicios", "works": "Obras"}


def categoria_es(crudo):
    return CATEGORIAS_ES.get(crudo or "", crudo or "")


def es_directo(tipo):
    """True cuando el procedimiento NO es licitación pública (menor cuantía,
    directa, excepción, CVE...). 'Licitación Pública Nacional' es el único abierto."""
    t = (tipo or "").strip().lower()
    if not t:
        return False
    return "licitación" not in t


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
        anio = (r.get("fecha_adjudicacion") or "")[:4]
        e["anios"].add(anio)
        cat_es = categoria_es(r.get("categoria"))
        cat = cat_es or "Sin categoría"
        e["categorias"][cat] = e["categorias"].get(cat, 0) + monto
        if es_directo(r.get("tipo_procedimiento")):
            e["directo_monto"] += monto
        e["contratos_lista"].append({
            "objeto": r.get("objeto", ""),
            "anio": anio,
            "categoria": cat_es,
            "monto": monto,
            "procedimiento": r.get("tipo_procedimiento", ""),
            "fecha": r.get("fecha_adjudicacion", ""),
            "url": r.get("url_muni", ""),
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
    print(f"Top {len(top)} proveedores (ver www/datos/proveedores.json)")


if __name__ == "__main__":
    main()