import json

from . import extractor, metadata, normalizer, validators

ENERGY_UNITS = {"GWh", "MWh", "kWh"}


def fetch(url, opener=None):
    if opener is None:
        import urllib.request
        with urllib.request.urlopen(url) as r:
            raw = r.read()
        for enc in ("utf-8", "latin-1"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("utf-8", errors="replace")
    return opener(url)


def run(html, url, fuente="ANDE", metodo="extraccion_html", prior=None):
    extracted = extractor.extract(html)
    built = []
    for e in extracted:
        valor = normalizer.parse_number(e["valor_raw"])
        unidad = e["unidad"]
        if unidad in ENERGY_UNITS:
            valor, unidad = normalizer.convert_energy(valor, unidad)
        rec = metadata.build_record(
            indicador=e["indicador"], valor=valor, unidad=unidad,
            periodo_text=e["periodo_text"], fuente=fuente, url=url, metodo=metodo)
        if validators.is_duplicate(rec, built):
            continue
        if prior and rec["indicador"] in prior:
            if validators.is_anomaly(prior[rec["indicador"]], rec["valor"]):
                rec["estado_verificacion"] = "requiere_revision"
        built.append(rec)
    return built


def store(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
