import json
import urllib.request

from . import extractor, metadata, normalizer

CSV_URL = ("https://ons-aws-prod-opendata.s3.amazonaws.com/"
           "dataset/geracao_itaipu/GERACAO_ITAIPU.csv")


def fetch(url=None):
    """Descarga CSV del ONS."""
    if url is None:
        url = CSV_URL
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8")


def extract(text):
    """Parsea CSV y retorna filas horarias."""
    return extractor.parse_csv(text)


def normalize(rows):
    """Agrega a base anual y convierte a GWh."""
    yearly = normalizer.aggregate_yearly(rows)
    result = []
    for y in yearly:
        result.append(("generacion_total", normalizer.mw_to_gwh(y["generacion_total_mw"]), "GWh", y["year"]))
        result.append(("generacion_sector_60hz", normalizer.mw_to_gwh(y["generacion_60hz_mw"]), "GWh", y["year"]))
        result.append(("generacion_sector_50hz", normalizer.mw_to_gwh(y["generacion_50hz_mw"]), "GWh", y["year"]))
        result.append(("suministro_brasil", normalizer.mw_to_gwh(y["suministro_brasil_mw"]), "GWh", y["year"]))
        result.append(("suministro_paraguay", normalizer.mw_to_gwh(y["suministro_paraguay_mw"]), "GWh", y["year"]))
    return result


def build(normalized, url=CSV_URL):
    """Construye registros con trazabilidad."""
    records = []
    for indicador, valor, unidad, year in normalized:
        records.append(metadata.build_record(indicador, valor, unidad, year, fuente="ONS Brasil", url=url))
    return records


def store(records, path):
    """Guarda registros en JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
