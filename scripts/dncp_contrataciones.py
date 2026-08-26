def es_de_asuncion(texto):
    if not texto:
        return False
    t = texto.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return "municipalidad de asuncion" in t


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
    uuid = fila.get("compiledRelease/id", "")
    ocid = fila.get("compiledRelease/ocid", "") or uuid
    aw, sp, co = awards.get(uuid, {}), suppliers.get(uuid, {}), contracts.get(uuid, {})
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
        "url_muni": f"https://www.contrataciones.gov.py/licitaciones/convocatoria/{fila.get('compiledRelease/tender/id', '')}.html",
    }


def validar(filas):
    errores = []
    for f in filas:
        if not f.get("id"):
            errores.append("fila sin id")
            continue
        if not f.get("objeto"):
            errores.append(f"proceso {f['id']} sin objeto")
        monto = f.get("monto", "")
        if monto and not str(monto).replace(".", "", 1).isdigit():
            errores.append(f"proceso {f['id']} monto no numérico: {monto}")
    return errores


def verificar_consistencia(filas_records):
    """Verifica que filtrar por nombre de comprador y por ID SICP de la Muni
    produce el mismo conjunto de procesos (control de calidad interno)."""
    por_nombre = [r for r in filas_records if es_de_asuncion(r.get("compiledRelease/buyer/name"))]
    por_id = [r for r in filas_records
              if (r.get("compiledRelease/buyer/id") or "").strip() == "DNCP-SICP-CODE-108"]
    iguales = len(por_nombre) == len(por_id) and not (
        {r.get("compiledRelease/id") for r in por_nombre} ^
        {r.get("compiledRelease/id") for r in por_id})
    msg = f"por nombre: {len(por_nombre)} · por SICP 108: {len(por_id)}"
    return iguales, msg


import csv
import os
import urllib.request
import zipfile

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
    ok, msg = verificar_consistencia(records)
    print(f"Verificación de consistencia: {msg} (estado: {'OK' if ok else 'ADVERTENCIA'})")
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