def es_de_asuncion(texto):
    if not texto:
        return False
    t = texto.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return "municipalidad de asuncion" in t


def es_entidad_por_sicp(fila, sicp):
    bid = (fila.get("compiledRelease/buyer/id") or "").strip()
    return bid == f"DNCP-SICP-CODE-{sicp}"


def es_del_anio(fila, anio):
    """Filtra por año real de adjudicación o publicación del proceso."""
    for campo in ("fecha_adjudicacion", "fecha_publicacion", "fecha_contrato"):
        fecha = fila.get(campo) or ""
        if fecha and fecha[:4] == anio:
            return True
    return False


def es_registro_valido(fila):
    """Excluye placeholders: sin objeto, sin valor estimado, o URL planned.html."""
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


COLUMNAS_SALIDA = [
    "id", "objeto", "estado", "categoria", "tipo_procedimiento", "comprador",
    "valor_estimado", "monto_adjudicado", "monto_contratado", "moneda",
    "n_adjudicaciones", "n_proveedores", "proveedor", "proveedores",
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
        "objeto": _buscar(fila, "compiledRelease/tender/title",
                          "compiledRelease/tender/description"),
        "estado": _buscar(fila, "compiledRelease/tender/status"),
        "categoria": _buscar(fila, "compiledRelease/tender/mainProcurementCategory"),
        "tipo_procedimiento": _buscar(fila, "compiledRelease/tender/procurementMethodDetails",
                                      "compiledRelease/tender/procurementMethod"),
        "comprador": _buscar(fila, "compiledRelease/buyer/name"),
        "valor_estimado": valor_estimado,
        "monto_adjudicado": str(int(monto_adjudicado)) if monto_adjudicado else "",
        "monto_contratado": str(int(monto_contratado)) if monto_contratado else "",
        "moneda": moneda,
        "n_adjudicaciones": len(aw),
        "n_proveedores": len(nombres),
        "proveedor": nombres[0] if nombres else "",
        "proveedores": " | ".join(nombres),
        "fecha_publicacion": _buscar(fila, "compiledRelease/tender/datePublished",
                                     "compiledRelease/date"),
        "fecha_adjudicacion": fecha_adj,
        "fecha_contrato": fecha_con,
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
        ve = f.get("valor_estimado", "")
        if ve and not str(ve).replace(".", "", 1).isdigit():
            errores.append(f"proceso {f['id']} valor_estimado no numérico: {ve}")
    return errores


def verificar_consistencia(filas_records, sicp="108"):
    """Verifica consistencia entre ID SICP y nombre del comprador.

    El cross-check por nombre aplica solo a la entidad activa (108, la Muni),
    cuyo nombre se conoce. Para otras entidades (parametrizadas por SICP), la
    verificación se hace por el ID (decisión: el ID es el primario robusto)."""
    esperado = f"DNCP-SICP-CODE-{sicp}"
    por_id = [r for r in filas_records
              if (r.get("compiledRelease/buyer/id") or "").strip() == esperado]
    if sicp == "108":
        por_nombre = [r for r in filas_records if es_de_asuncion(r.get("compiledRelease/buyer/name"))]
        iguales = len(por_id) == len(por_nombre) and not (
            {r.get("compiledRelease/id") for r in por_id} ^
            {r.get("compiledRelease/id") for r in por_nombre})
        msg = f"por SICP {sicp}: {len(por_id)} · por nombre: {len(por_nombre)}"
    else:
        iguales = True
        msg = f"por SICP {sicp}: {len(por_id)} · cross-check por nombre: solo entidad activa (108)"
    return iguales, msg


import csv
import datetime
import json
import os
import re
import sys
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


def parse_csv_robusto(texto):
    """Parsea CSV respetando comillas (maneja comas dentro de valores).
    Devuelve lista de dicts con la primera línea como encabezado."""
    import csv as _csv
    reader = _csv.reader(texto.splitlines())
    filas = list(reader)
    if not filas:
        return []
    header = filas[0]
    return [dict(zip(header, row)) for row in filas[1:] if row]


def leer_tabla(zip_path, nombre):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(nombre) as f:
            buf = f.read().decode("utf-8")
    return parse_csv_robusto(buf)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


_AWARD_PAT = re.compile(r"^compiledRelease/awards/(\d+)/(.*)$")
_SUP_PAT = re.compile(r"^compiledRelease/awards/(\d+)/suppliers/(\d+)/name$")
_CONT_PAT = re.compile(r"^compiledRelease/contracts/(\d+)/(.*)$")


def indexar_awards(rows):
    """Recolecta TODAS las adjudicaciones (awards/N) de cada release, no solo /0."""
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
    return out


def indexar_suppliers(rows):
    """Recolecta todos los proveedores por adjudicación (awards/N/suppliers/M)."""
    out = {}
    for r in rows:
        rid = r.get("compiledRelease/id", "")
        por_award = {}
        for k, v in r.items():
            m = _SUP_PAT.match(k)
            if not m:
                continue
            i, j = int(m.group(1)), int(m.group(2))
            por_award.setdefault(i, []).append(v)
        out[rid] = por_award
    return out


def indexar_contracts(rows):
    """Recolecta TODOS los contratos (contracts/N) de cada release."""
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


def construir_metadata(anio, filas, sicp):
    con_adjudicacion = sum(1 for f in filas if int(f.get("n_adjudicaciones") or 0) > 0)
    return {
        "dataset": f"contrataciones_muni_{anio}",
        "anio": anio,
        "sicp": sicp,
        "registros": len(filas),
        "con_adjudicacion": con_adjudicacion,
        "sin_adjudicacion": len(filas) - con_adjudicacion,
        "generado_en": datetime.date.today().isoformat(),
        "fuente": "DNCP OCDS (masivo)",
        "licencia": "CC BY 4.0",
    }


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
    entidad = [f for f in entidad if es_del_anio(f, anio)]
    entidad = [f for f in entidad if es_registro_valido(f)]
    errores = validar(entidad)
    if errores:
        print(f"Advertencias: {len(errores)}")
        for e in errores[:10]:
            print("  -", e)
    os.makedirs(DATA_DIR, exist_ok=True)
    sufijo = "muni" if sicp == "108" else f"ent{sicp}"
    out = os.path.join(DATA_DIR, f"contrataciones_{sufijo}_{anio}.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNAS_SALIDA)
        writer.writeheader()
        writer.writerows(entidad)
    print(f"Procesos entidad {sicp} {anio} (válidos): {len(entidad)}")
    print(f"Dataset escrito: {out}")
    meta = construir_metadata(anio, entidad, sicp)
    meta_ruta = os.path.join(DATA_DIR, f"metadata_{anio}.json")
    with open(meta_ruta, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"Metadata: {meta_ruta}")


def anio_sicp_desde_args(args):
    anio = "2026"
    sicp = "108"
    if len(args) >= 2 and str(args[1]).isdigit():
        anio = args[1]
    if len(args) >= 3 and str(args[2]).isdigit():
        sicp = args[2]
    return anio, sicp


if __name__ == "__main__":
    anio, sicp = anio_sicp_desde_args(sys.argv)
    main(anio, sicp)