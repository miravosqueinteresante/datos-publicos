import os
import urllib.request

SOURCES = {
    "bagp": "https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf",
    "pliego": "https://www.ande.gov.py/docs/tarifas/PLIEGO21.pdf",
    "compilacion": "https://www.ande.gov.py/documentos_contables/747/ande_-_compilacion_estadistica_2000-2020.pdf",
}
CACHE = os.path.join("connectors", "ande", "_cache")
OUT = os.path.join("www", "datos", "ande-indicadores.json")
OUT_MVP = os.path.join("www", "datos", "ande-indicadores-mvp.json")

# Indicadores prioritarios para el MVP (10 indicadores críticos)
MVP_INDICATORS = [
    "consumo_total",
    "demanda_maxima",
    "factor_carga",
    "clientes_total",
    "perdidas_totales",
    "consumo_categoria_residencial",
    "consumo_categoria_electrointensivas",
    "generacion_itaipu_paraguay",
    "generacion_yacyreta_paraguay",
    "generacion_yacyreta_total",
]


def _download(name, url):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name + ".pdf")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return path


def _filter_mvp(recs):
    """Retiene solo los indicadores de la lista MVP."""
    mvp_set = {MVP_INDICATORS}
    return [r for r in recs if r["indicador"] in MVP_INDICATORS]

def main(mvp=False):
    recs = []
    for name, url in SOURCES.items():
        path = _download(name, url)
        if name == "compilacion":
            recs += connector.run_compilacion(path, url)
        else:
            recs += connector.run_pdf(path, url)
    recs += curados.CURADOS
    # Filtrar a MVP si se solicita
    if mvp:
        recs = _filter_mvp(recs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(recs, OUT)
    # También generar archivo MVP
    if mvp:
        os.makedirs(os.path.dirname(OUT_MVP), exist_ok=True)
        connector.store(recs, OUT_MVP)
    print(f"ANDE connector: {len(recs)} indicadores -> {OUT}")
    if mvp:
        print(f"MVP indicators -> {OUT_MVP}")
    for r in recs:
        print(f"  {r['indicador']}: {r['valor']} {r['unidad']} [{r['estado_verificacion']}]")


if __name__ == "__main__":
    import sys
    mvp = "--mvp" in sys.argv
    main(mvp=mvp)
