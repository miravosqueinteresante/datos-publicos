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


def presupuesto_filas_a_json(filas):
    return [
        {
            "ejercicio": f[0], "nivel": f[1], "denominacion": f[2],
            "presupuesto_vigente": float(f[3]) if f[3] else None,
            "obligado": float(f[4]) if f[4] else None,
            "porcentaje_ejecucion": float(f[5]) if f[5] else None,
            "fuente": f[6], "url": f[7],
        }
        for f in filas
    ]


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


def generar_presupuesto(anio):
    origen = os.path.join(DATA_DIR, f"presupuesto_ejecucion_{anio}.csv")
    destino = os.path.join(WEB_DATOS, f"presupuesto-ejecucion-{anio}.json")
    if not os.path.exists(origen):
        print(f"[presupuesto {anio}] no existe {origen}, omitido")
        return 0
    with open(origen, encoding="utf-8") as f:
        filas = list(csv.reader(f))
    header = filas[0]
    datos = presupuesto_filas_a_json(filas[1:])
    os.makedirs(WEB_DATOS, exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Generados {len(datos)} registros de presupuesto {anio} en {destino}")
    return len(datos)


def main():
    for anio in ["2024", "2026"]:
        generar_contrataciones(anio)
        generar_presupuesto(anio)


if __name__ == "__main__":
    main()