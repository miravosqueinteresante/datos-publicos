import csv
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _traducir_categoria(c):
    mapa = {"goods": "Bienes", "services": "Servicios", "works": "Obras"}
    return mapa.get(c, c)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def calcular_indicadores(csv_texto):
    filas = list(csv.DictReader(csv_texto.splitlines()))
    por_categoria = {}
    por_proveedor = {}
    por_tipo = {}
    valor_estimado_total = 0
    monto_adjudicado_total = 0
    monto_contratado_total = 0
    sin_adjudicacion = 0
    for f in filas:
        ve = _num(f.get("valor_estimado"))
        ma = _num(f.get("monto_adjudicado"))
        mc = _num(f.get("monto_contratado"))
        valor_estimado_total += ve
        monto_adjudicado_total += ma
        monto_contratado_total += mc
        if (int(f.get("n_adjudicaciones") or 0) or 0) == 0:
            sin_adjudicacion += 1
        # Las distribuciones y el ranking se calculan SOBRE lo adjudicado,
        # no sobre el valor estimado de procesos aun no adjudicados.
        cat = _traducir_categoria(f.get("categoria") or "Sin categoría")
        por_categoria[cat] = por_categoria.get(cat, 0) + ma
        prov = f.get("proveedor") or ""
        if prov:
            por_proveedor[prov] = por_proveedor.get(prov, 0) + ma
        tipo = f.get("tipo_procedimiento") or "Sin tipo"
        por_tipo[tipo] = por_tipo.get(tipo, 0) + ma
    top_prov = sorted(por_proveedor.items(), key=lambda x: -x[1])[:10]
    top_list = []
    for p, m in top_prov:
        pct = (m / monto_adjudicado_total * 100) if monto_adjudicado_total else 0
        top_list.append({"proveedor": p, "monto": round(m), "pct_del_adjudicado": round(pct, 1)})
    return {
        "procesos": len(filas),
        "valor_estimado_total": round(valor_estimado_total),
        "monto_adjudicado_total": round(monto_adjudicado_total),
        "monto_contratado_total": round(monto_contratado_total),
        "procesos_sin_adjudicacion": sin_adjudicacion,
        "por_categoria": [{"categoria": c, "monto": round(m)} for c, m in
                          sorted(por_categoria.items(), key=lambda x: -x[1])],
        "por_tipo_procedimiento": [{"tipo": t, "monto": round(m)} for t, m in
                                    sorted(por_tipo.items(), key=lambda x: -x[1])],
        "top_proveedores": top_list,
        "monto_total": round(monto_adjudicado_total),
    }


def _rutas(anio):
    csv_ruta = os.path.join(ROOT_DIR, "data", f"contrataciones_muni_{anio}.csv")
    json_ruta = os.path.join(ROOT_DIR, "www", "datos", f"indicadores-gasto-{anio}.json")
    return csv_ruta, json_ruta


def main():
    for anio in ["2023", "2024", "2025", "2026"]:
        csv_ruta, json_ruta = _rutas(anio)
        if not os.path.exists(csv_ruta):
            print(f"[indicadores {anio}] no existe {csv_ruta}, omitido")
            continue
        with open(csv_ruta, encoding="utf-8") as f:
            ind = calcular_indicadores(f.read())
        os.makedirs(os.path.dirname(json_ruta), exist_ok=True)
        with open(json_ruta, "w", encoding="utf-8") as f:
            json.dump(ind, f, ensure_ascii=False, indent=2)
        print(f"Indicadores {anio}: {ind['procesos']} procesos, "
              f"{ind['monto_total']:.0f} PYG total")


if __name__ == "__main__":
    main()