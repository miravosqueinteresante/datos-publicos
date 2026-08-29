import os
import urllib.request

from connectors.ande import connector

SOURCES = {
    "bagp": "https://www.ande.gov.py/finanzas/BAGP%202025%20ANDE.pdf",
    "pliego": "https://www.ande.gov.py/docs/tarifas/PLIEGO21.pdf",
    "compilacion": "https://www.ande.gov.py/documentos_contables/747/ande_-_compilacion_estadistica_2000-2020.pdf",
}
CACHE = os.path.join("connectors", "ande", "_cache")
OUT = os.path.join("www", "datos", "ande-indicadores.json")


def _download(name, url):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, name + ".pdf")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    with open(path, "wb") as f:
        f.write(data)
    return path


def main():
    recs = []
    for name, url in SOURCES.items():
        path = _download(name, url)
        if name == "compilacion":
            recs += connector.run_compilacion(path, url)
        else:
            recs += connector.run_pdf(path, url)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(recs, OUT)
    print(f"ANDE connector: {len(recs)} indicadores -> {OUT}")
    for r in recs:
        print(f"  {r['indicador']}: {r['valor']} {r['unidad']} [{r['estado_verificacion']}]")


if __name__ == "__main__":
    main()
