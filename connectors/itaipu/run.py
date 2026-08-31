import os
import sys

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

from connectors.itaipu import connector

OUT = os.path.join("www", "datos", "itaipu-indicadores.json")


def main():
    print("Itaipú connector: descargando datos del ONS...")
    text = connector.fetch()
    rows = connector.extract(text)
    print(f"  {len(rows)} registros horarios parseados")
    normalized = connector.normalize(rows)
    records = connector.build(normalized)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(records, OUT)
    print(f"Itaipú connector: {len(records)} indicadores -> {OUT}")
    for r in records:
        print(f"  {r['indicador']}: {r['valor']:.1f} {r['unidad']} ({r['fecha_inicio'][:4]}) [{r['estado_verificacion']}]")


if __name__ == "__main__":
    main()
