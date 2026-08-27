import csv
import os
import re
import urllib.request

URL_PDF = "https://www.asuncion.gov.py/wp-content/uploads/2025/08/Rendicion-de-Cuentas-2024.pdf"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIN_VERSIONAR = os.path.join(ROOT, "data", "_sin_versionar")
PDF_LOCAL = os.path.join(SIN_VERSIONAR, "rendicion-cuentas-2024.pdf")
OUTPUT = os.path.join(ROOT, "data", "presupuesto_ejecucion_2024.csv")

COLUMNAS = ["ejercicio", "nivel", "denominacion", "presupuesto_vigente",
            "obligado", "porcentaje_ejecucion", "fuente", "url"]


def normalizar_numero(texto):
    txt = (texto or "").strip()
    if not txt or txt.endswith("%"):
        return None
    txt = txt.replace(".", "").replace(",", ".")
    try:
        return float(txt)
    except ValueError:
        return None


def parsear_fila(campos):
    nivel = (campos[0] or "").strip()
    denominacion = (campos[1] or "").strip()
    vigente = normalizar_numero(campos[2]) if len(campos) > 2 else None
    obligado = normalizar_numero(campos[3]) if len(campos) > 3 else None
    pct = obligado / vigente * 100 if (vigente and obligado is not None) else None
    return {
        "nivel": nivel,
        "denominacion": denominacion,
        "presupuesto_vigente": vigente,
        "obligado": obligado,
        "porcentaje_ejecucion": round(pct, 2) if pct is not None else None,
    }


def validar_totales(filas, total_vigente, total_obligado, tol=0.5):
    errores = []
    suma_v = sum((f["presupuesto_vigente"] or 0) for f in filas)
    suma_o = sum((f["obligado"] or 0) for f in filas)
    if abs(suma_v - total_vigente) > tol:
        errores.append(f"vigente: suma {suma_v:.1f} != total {total_vigente}")
    if abs(suma_o - total_obligado) > tol:
        errores.append(f"obligado: suma {suma_o:.1f} != total {total_obligado}")
    return errores


def extraer_tabla(pdf_path, pagina_idx=3, y_min=780):
    """Extrae la tabla de ejecución del gasto de la página 4, usando bloques
    con coordenadas y filtrando la región de la tabla (debajo del encabezado).
    get_text() plano mezcla la tabla de ingresos con la de gastos; bloques evita eso."""
    import fitz
    doc = fitz.open(pdf_path)
    bloques = doc[pagina_idx].get_text("blocks")
    filas = []
    for b in bloques:
        x0, y0, x1, y1, texto, bid, bn = b
        if y0 < y_min:
            continue
        partes = [p.strip() for p in texto.split("\n")]
        partes = [p for p in partes if p]
        if not partes:
            continue
        # fila con nivel (100..900) seguido de denominación y montos
        m = re.match(r"^\d{3}$", partes[0] or "")
        if m:
            campos = partes
            if len(campos) >= 2:
                filas.append(parsear_fila(campos[:5]))
    return filas


def descargar_pdf():
    os.makedirs(SIN_VERSIONAR, exist_ok=True)
    if not os.path.exists(PDF_LOCAL):
        print(f"Descargando {URL_PDF} ...")
        urllib.request.urlretrieve(URL_PDF, PDF_LOCAL)
    return PDF_LOCAL


def escribir_csv(filas, ejercicio="2024"):
    total_v = round(sum((f["presupuesto_vigente"] or 0) for f in filas), 3)
    total_o = round(sum((f["obligado"] or 0) for f in filas), 3)
    total_pct = round(total_o / total_v * 100, 2) if total_v else None
    fila_total = {
        "nivel": "TOTAL", "denominacion": "TOTAL GENERAL",
        "presupuesto_vigente": total_v, "obligado": total_o,
        "porcentaje_ejecucion": total_pct,
    }
    filas_salida = [dict(f, ejercicio=ejercicio,
                         fuente="Rendición de Cuentas 2024", url=URL_PDF) for f in filas]
    filas_salida.append(dict(fila_total, ejercicio=ejercicio,
                             fuente="Rendición de Cuentas 2024", url=URL_PDF))
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(filas_salida)
    return fila_total


def main():
    pdf = descargar_pdf()
    filas = extraer_tabla(pdf)
    print(f"Filas objeto del gasto extraídas: {len(filas)}")
    for f in filas:
        print("  ", f["nivel"], f["denominacion"], f["presupuesto_vigente"], f["obligado"])
    total = escribir_csv(filas)
    print(f"Total vigente {total['presupuesto_vigente']} · obligado {total['obligado']} "
          f"· {total['porcentaje_ejecucion']}%")
    print(f"Dataset: {OUTPUT}")


if __name__ == "__main__":
    main()