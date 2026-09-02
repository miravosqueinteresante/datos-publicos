from . import metadata
URL_YACYRETA = "https://paraguayoindependiente.com/2026/01/21/yacyreta-muestra-una-senal-preocupante-para-paraguay/"
def _r(ind, val, uni, periodo, fuente, url):
    return metadata.build_record(ind, val, uni, periodo, fuente=fuente, url=url, metodo="extraccion_manual", estado="verificado")
URL_EBY_2019 = "https://www.eby.gov.py/informe-de-produccion-anual-de-la-central-hidroelectrica-yacyreta/"
URL_ABC_2016 = "https://www.abc.com.py/edicion-impresa/suplementos/economico/2024/02/25/yacyreta-paraguay-uso-7-y-argentina-93/"
CURADOS = [
    _r("generacion_total", 21627.0, "GWh", 2016, "EBY", URL_ABC_2016),
    _r("generacion_total", 20827.0, "GWh", 2017, "EBY", "https://www.cooperativacalf.com.ar/yacyreta-registro-un-record-de-produccion-electrica-en-diciembre/"),
    _r("generacion_total", 19470.0, "GWh", 2018, "EBY", "https://www.eby.gov.py/al-cierre-de-2018-yacyreta-acumula-359-millones-de-mw-h/"),
    _r("generacion_total", 17281.0, "GWh", 2019, "EBY", URL_EBY_2019),
    _r("generacion_total", 13372.0, "GWh", 2021, "EBY", "https://economis.com.ar/yacyreta-tuvo-una-caida-del-10-en-la-generacion-durante-el-ano-2021/"),
    _r("generacion_total", 16130.0, "GWh", 2022, "EBY", "https://www.abc.com.py/economia/2023/01/01/yacyreta-entrega-de-energia-fue-20-mas-que-el-2021/"),
    _r("generacion_total", 19916.0, "GWh", 2023, "EBY", "https://www.abc.com.py/edicion-impresa/suplementos/economico/2024/02/25/yacyreta-paraguay-uso-7-y-argentina-93/"),
    _r("generacion_total", 16071.0, "GWh", 2024, "EBY", "https://www.abc.com.py/economia/2025/01/19/energia-de-yacyreta-la-ande-retiro-171-mas-de-la-central-en-2024/"),
    _r("generacion_total", 16103.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("suministro_paraguay", 3081.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("suministro_argentina", 13022.0, "GWh", 2025, "Entidad Binacional Yacyretá", URL_YACYRETA),
]
