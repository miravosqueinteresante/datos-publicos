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
