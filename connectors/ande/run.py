import os

from connectors.ande import connector

URL = "https://www.ande.gov.py/interna.php?id=14877"
OUT = os.path.join("www", "datos", "ande-indicadores.json")


def main():
    html = connector.fetch(URL)
    recs = connector.run(html, url=URL)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(recs, OUT)
    print(f"ANDE connector: {len(recs)} indicadores -> {OUT}")
    for r in recs:
        print(f"  {r['indicador']}: {r['valor']} {r['unidad']} [{r['estado_verificacion']}]")


if __name__ == "__main__":
    main()
