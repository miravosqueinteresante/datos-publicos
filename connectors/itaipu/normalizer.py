from collections import defaultdict


def aggregate_yearly(rows):
    """Agrega datos horarios a base anual (suma MW → GWh)."""
    by_year = defaultdict(lambda: {
        "total": 0.0, "60hz": 0.0, "50hz": 0.0, "50hz_br": 0.0, "br": 0.0, "count": 0
    })
    for row in rows:
        year = row["din_instante"].year
        by_year[year]["total"] += row["val_itaipu_total"]
        by_year[year]["60hz"] += row["val_itaipu_60hz"]
        by_year[year]["50hz"] += row["val_itaipu_50hz"]
        by_year[year]["50hz_br"] += row["val_itaipu_50hz_br"]
        by_year[year]["br"] += row["val_itaipu_br"]
        by_year[year]["count"] += 1
    result = []
    for year in sorted(by_year):
        d = by_year[year]
        result.append({
            "year": year,
            "generacion_total_mw": d["total"],
            "generacion_60hz_mw": d["60hz"],
            "generacion_50hz_mw": d["50hz"],
            "suministro_brasil_mw": d["br"],
            "suministro_paraguay_mw": d["50hz"] - d["50hz_br"],
            "horas": d["count"],
        })
    return result


def mw_to_gwh(mw_hours):
    """Convierte MW·horas a GWh."""
    return mw_hours / 1000.0
