import json

from . import extractor, metadata, normalizer, validators

ENERGY_UNITS = {"GWh", "MWh", "kWh"}
PDF_PARSERS = [
    extractor.extract_consumo_categoria,
    extractor.extract_tarifas,
    extractor.extract_perdidas,
    extractor.extract_clientes,
]


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


def _normalize_and_build(e, url, fuente, metodo):
    valor = normalizer.parse_number(e["valor_raw"])
    unidad = e["unidad"]
    if unidad in ENERGY_UNITS:
        valor, unidad = normalizer.convert_energy(valor, unidad)
    return metadata.build_record(
        indicador=e["indicador"], valor=valor, unidad=unidad,
        periodo_text=e["periodo_text"], fuente=fuente, url=url, metodo=metodo)


def _collect(raw, url, fuente, metodo, prior):
    built = []
    for e in raw:
        rec = _normalize_and_build(e, url, fuente, metodo)
        if validators.is_duplicate(rec, built):
            continue
        if prior and rec["indicador"] in prior:
            if validators.is_anomaly(prior[rec["indicador"]], rec["valor"]):
                rec["estado_verificacion"] = "requiere_revision"
        built.append(rec)
    return built


def run(html, url, fuente="ANDE", metodo="extraccion_html", prior=None):
    return _collect(extractor.extract(html), url, fuente, metodo, prior)


def run_text(text, url, fuente="ANDE", metodo="extraccion_pdf", parsers=None, prior=None):
    if parsers is None:
        parsers = PDF_PARSERS
    raw = []
    for parser in parsers:
        raw.extend(parser(text))
    return _collect(raw, url, fuente, metodo, prior)


def run_pdf(path, url, prior=None):
    text = extractor.pdf_text(path)
    return run_text(text, url, prior=prior)


def store(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
