import os
import sys
import urllib.request

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from connectors.ande import connector, curados

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
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(recs, OUT)
    print(f"ANDE connector: {len(recs)} indicadores -> {OUT}")
    for r in recs:
        print(f"  {r['indicador']}: {r['valor']} {r['unidad']} [{r['estado_verificacion']}]")
    if mvp:
        mvp_recs = _filter_mvp(recs)
        os.makedirs(os.path.dirname(OUT_MVP), exist_ok=True)
        connector.store(mvp_recs, OUT_MVP)
        print(f"MVP: {len(mvp_recs)} indicadores -> {OUT_MVP}")


if __name__ == "__main__":
    mvp = "--mvp" in sys.argv
    main(mvp=mvp)
