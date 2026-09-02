from . import metadata
URL_YACYRETA = "https://paraguayoindependiente.com/2026/01/21/yacyreta-muestra-una-senal-preocupante-para-paraguay/"
def _r(ind, val, uni, periodo, fuente, url):
    return metadata.build_record(ind, val, uni, periodo, fuente=fuente, url=url, metodo="extraccion_manual", estado="verificado")
CURADOS = [
    _r("generacion_yacyreta_paraguay", 3081.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("generacion_yacyreta_total", 16103.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
]
