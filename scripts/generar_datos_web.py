import csv
import json
import os

RUTA_ORIGEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "contrataciones_muni_2026.csv")
RUTA_DESTINO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "www", "datos", "contrataciones-2026.json")


CATEGORIAS_ES = {"goods": "Bienes", "services": "Servicios", "works": "Obras"}


def categoria_es(crudo):
    return CATEGORIAS_ES.get(crudo or "", crudo or "")


def fila_a_json(fila):
    monto = fila.get("monto") or ""
    es_nulo = not monto
    try:
        monto_num = float(monto)
    except ValueError:
        monto_num = 0
        es_nulo = True
    return {
        "id": fila.get("id", ""),
        "objeto": fila.get("objeto", ""),
        "estado": fila.get("estado", ""),
        "categoria": categoria_es(fila.get("categoria", "")),
        "categoria_raw": fila.get("categoria", ""),
        "tipo_procedimiento": fila.get("tipo_procedimiento", ""),
        "comprador": fila.get("comprador", ""),
        "proveedor": fila.get("proveedor", ""),
        "monto": monto_num,
        "monto_nulo": es_nulo,
        "moneda": fila.get("moneda", ""),
        "fecha_publicacion": fila.get("fecha_publicacion", ""),
        "fecha_adjudicacion": fila.get("fecha_adjudicacion", ""),
        "fecha_contrato": fila.get("fecha_contrato", ""),
        "url_muni": fila.get("url_muni", ""),
    }


def generar(csv_texto):
    reader = csv.DictReader(csv_texto.splitlines())
    return [fila_a_json(f) for f in reader]


def main():
    with open(RUTA_ORIGEN, encoding="utf-8") as f:
        datos = generar(f.read())
    os.makedirs(os.path.dirname(RUTA_DESTINO), exist_ok=True)
    with open(RUTA_DESTINO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Generados {len(datos)} registros en {RUTA_DESTINO}")


if __name__ == "__main__":
    main()