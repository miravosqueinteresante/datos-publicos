import os, sys
_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)
from connectors.yacyreta import connector
from connectors.yacyreta.curados import CURADOS
OUT = os.path.join("www", "datos", "yacyreta-indicadores.json")
def main():
    print("Yacyretá connector: descubriendo meses EBY...")
    try:
        months = connector.extract_months()
        print(f"  {len(months)} meses EBY parseados")
    except Exception as e:
        print(f"  EBY fetch fallo: {e}, usando curados")
        months = []
    recs = []
    if months:
        norm = connector.normalize(months)
        recs = connector.build(norm)
    recs += CURADOS
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    connector.store(recs, OUT)
    print(f"Yacyretá connector: {len(recs)} indicadores -> {OUT}")
    for r in recs:
        print(f"  {r['indicador']}: {r['valor']:.1f} {r['unidad']} ({r['fecha_inicio'][:4]}) [{r['estado_verificacion']}]")
if __name__ == "__main__":
    main()
