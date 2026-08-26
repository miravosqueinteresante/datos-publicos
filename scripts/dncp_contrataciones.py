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