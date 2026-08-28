import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
WEB_DATOS = os.path.join(ROOT, "www", "datos")

CATEGORIAS_ES = {"goods": "Bienes", "services": "Servicios", "works": "Obras"}


def categoria_es(crudo):
    return CATEGORIAS_ES.get(crudo or "", crudo or "")


def fila_a_json(fila):
    monto_adj = fila.get("monto_adjudicado") or ""
    es_nulo = not monto_adj
    try:
        monto_num = float(monto_adj)
    except ValueError:
        monto_num = 0
        es_nulo = True
    try:
        valor_estimado = float(fila.get("valor_estimado") or 0)
    except ValueError:
        valor_estimado = 0
    try:
        monto_contratado = float(fila.get("monto_contratado") or 0)
    except ValueError:
        monto_contratado = 0
    return {
        "id": fila.get("id", ""),
        "objeto": fila.get("objeto", ""),
        "estado": fila.get("estado", ""),
        "categoria": categoria_es(fila.get("categoria", "")),
        "categoria_raw": fila.get("categoria", ""),
        "tipo_procedimiento": fila.get("tipo_procedimiento", ""),
        "comprador": fila.get("comprador", ""),
        "proveedor": fila.get("proveedor", ""),
        "valor_estimado": valor_estimado,
        "monto_adjudicado": monto_num,
        "monto_contratado": monto_contratado,
        "monto": monto_num,
        "monto_nulo": es_nulo,
        "n_adjudicaciones": int(fila.get("n_adjudicaciones") or 0),
        "n_proveedores": int(fila.get("n_proveedores") or 0),
        "proveedores": fila.get("proveedores", ""),
        "moneda": fila.get("moneda", ""),
        "fecha_publicacion": fila.get("fecha_publicacion", ""),
        "fecha_adjudicacion": fila.get("fecha_adjudicacion", ""),
        "fecha_contrato": fila.get("fecha_contrato", ""),
        "url_muni": fila.get("url_muni", ""),
    }


def generar(csv_texto):
    reader = csv.DictReader(csv_texto.splitlines())
    return [fila_a_json(f) for f in reader]


def generar_contrataciones(anio):
    origen = os.path.join(DATA_DIR, f"contrataciones_muni_{anio}.csv")
    destino = os.path.join(WEB_DATOS, f"contrataciones-{anio}.json")
    if not os.path.exists(origen):
        print(f"[contrataciones {anio}] no existe {origen}, omitido")
        return 0
    with open(origen, encoding="utf-8") as f:
        datos = generar(f.read())
    os.makedirs(WEB_DATOS, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Generados {len(datos)} registros de contrataciones {anio} en {destino}")
    return len(datos)


def main():
    for anio in ["2023", "2024", "2025", "2026"]:
        generar_contrataciones(anio)


if __name__ == "__main__":
    main()