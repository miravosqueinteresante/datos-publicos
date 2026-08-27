import csv
import json
import os

RUTA_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data", "contrataciones_muni_2026.csv")
RUTA_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "www", "datos", "indicadores-gasto-2026.json")


def _traducir_categoria(c):
    mapa = {"goods": "Bienes", "services": "Servicios", "works": "Obras"}
    return mapa.get(c, c)


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
        cat = _traducir_categoria(f.get("categoria") or "Sin categoría")
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