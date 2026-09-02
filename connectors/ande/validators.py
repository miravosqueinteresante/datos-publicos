from datetime import date


def relative_change(prev, new):
    if not prev:
        return None
    return new / prev


def is_anomaly(prev, new, factor=5.0):
    rel = relative_change(prev, new)
    if rel is None:
        return False
    return rel > factor or rel < (1.0 / factor)


def _key(rec):
    return (
        rec.get("indicador"),
        rec.get("fecha_inicio"),
        rec.get("fecha_fin"),
        round(float(rec.get("valor", 0) or 0), 3),
    )


def is_duplicate(rec, recs):
    k = _key(rec)
    return any(_key(r) == k for r in recs)


def periods_overlap(a, b):
    sa, ea = date.fromisoformat(a["fecha_inicio"]), date.fromisoformat(a["fecha_fin"])
    sb, eb = date.fromisoformat(b["fecha_inicio"]), date.fromisoformat(b["fecha_fin"])
    return sa <= eb and sb <= ea


def _group(records):
    from collections import defaultdict
    g = defaultdict(list)
    for r in records:
        g[(r.get("fecha_inicio"), r.get("fecha_fin"))].append(r)
    if len(g) == 1 and (None, None) in g:
        return {("all", "all"): records}
    return g


def _rel_err(a, b):
    return abs(a - b) / abs(b) if b else float("inf")


def validate_itaipu(records, tol=0.005):
    errs = []
    for period, recs in _group(records).items():
        m = {r["indicador"]: float(r["valor"]) for r in recs if r.get("indicador") and r.get("valor") is not None}
        if all(k in m for k in ("generacion_sector_50hz", "generacion_sector_60hz", "generacion_total")):
            s = m["generacion_sector_50hz"] + m["generacion_sector_60hz"]
            if _rel_err(s, m["generacion_total"]) > tol:
                errs.append(f"itaipu {period}: 50hz+60hz {s:.2f} != total {m['generacion_total']:.2f} (tol {tol:.1%})")
        if all(k in m for k in ("suministro_paraguay", "suministro_brasil", "generacion_total")):
            s = m["suministro_paraguay"] + m["suministro_brasil"]
            if _rel_err(s, m["generacion_total"]) > tol:
                errs.append(f"itaipu {period}: py+br {s:.2f} != total {m['generacion_total']:.2f} (tol {tol:.1%})")
    return errs


def validate_yacyreta(records, tol=0.005):
    errs = []
    for period, recs in _group(records).items():
        m = {r["indicador"]: float(r["valor"]) for r in recs if r.get("indicador") and r.get("valor") is not None}
        if all(k in m for k in ("suministro_argentina", "suministro_paraguay", "generacion_total")):
            s = m["suministro_argentina"] + m["suministro_paraguay"]
            if _rel_err(s, m["generacion_total"]) > tol:
                errs.append(f"yacyreta {period}: ar+py {s:.2f} != total {m['generacion_total']:.2f} (tol {tol:.1%})")
    return errs


def validate_invariants(records):
    from collections import defaultdict
    groups = defaultdict(list)
    for r in records:
        k = (r.get("fecha_inicio"), r.get("fecha_fin"))
        groups[k].append(r)
    if len(groups) == 1 and (None, None) in groups:
        groups = {("all", "all"): records}
    errors = []
    for period, recs in groups.items():
        m = {r["indicador"]: float(r["valor"]) for r in recs if r.get("indicador") and r.get("valor") is not None}
        if all(x in m for x in ("perdidas_distribucion", "perdidas_transmision", "perdidas_totales")):
            s = m["perdidas_distribucion"] + m["perdidas_transmision"]
            if abs(s - m["perdidas_totales"]) > 0.05:
                errors.append(f"perdidas {period}: {m['perdidas_distribucion']}+{m['perdidas_transmision']}={s:.2f} != {m['perdidas_totales']} (tol 0.05)")
        consumo_cats = {k: v for k, v in m.items() if k.startswith("consumo_categoria_")}
        if consumo_cats and "consumo_total" in m:
            s = sum(consumo_cats.values())
            tot = m["consumo_total"]
            if tot and abs(s - tot) / abs(tot) > 0.01:
                errors.append(f"consumo {period}: sum categorias {s:.2f} != total {tot} (tol 1%)")
        clientes_cats = {k: v for k, v in m.items() if k.startswith("clientes_categoria_")}
        if clientes_cats and "clientes_total" in m:
            s = sum(clientes_cats.values())
            if abs(s - m["clientes_total"]) > 1:
                errors.append(f"clientes {period}: sum categorias {s:.0f} != total {m['clientes_total']:.0f} (tol 1)")
    return errors
