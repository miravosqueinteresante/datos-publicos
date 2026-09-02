from . import metadata
URL_YACYRETA = "https://paraguayoindependiente.com/2026/01/21/yacyreta-muestra-una-senal-preocupante-para-paraguay/"
def _r(ind, val, uni, periodo, fuente, url):
    return metadata.build_record(ind, val, uni, periodo, fuente=fuente, url=url, metodo="extraccion_manual", estado="verificado")
URL_EBY_2019 = "https://www.eby.gov.py/informe-de-produccion-anual-de-la-central-hidroelectrica-yacyreta/"
URL_ABC_2016 = "https://www.abc.com.py/edicion-impresa/suplementos/economico/2024/02/25/yacyreta-paraguay-uso-7-y-argentina-93/"
CURADOS = [
    _r("generacion_total", 21627.0, "GWh", 2016, "EBY", URL_ABC_2016),
    _r("generacion_total", 17281.0, "GWh", 2019, "EBY", URL_EBY_2019),
    _r("generacion_total", 16103.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("suministro_paraguay", 3081.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("suministro_argentina", 13022.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
]
