from collections import defaultdict

def aggregate_yearly(months):
    by_year = defaultdict(lambda: {"total": 0.0, "sadi": 0.0, "sinp": 0.0, "count": 0})
    for m in months:
        y = m["year"]
        by_year[y]["total"] += m["total_mwh"]
        by_year[y]["sadi"] += (m.get("sadi_mwh") or 0)
        by_year[y]["sinp"] += (m.get("sinp_mwh") or 0)
        by_year[y]["count"] += 1
    out = []
    for y in sorted(by_year):
        d = by_year[y]
        out.append({"year": y, "total_mwh": d["total"], "sadi_mwh": d["sadi"], "sinp_mwh": d["sinp"], "meses": d["count"]})
    return out

def mwh_to_gwh(v):
    return v / 1000.0
