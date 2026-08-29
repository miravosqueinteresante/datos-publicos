from . import metadata

URL_ITAIPU = ("https://www.itaipu.gov.py/noticias/energia/"
              "itaipu-suministro-25-768-gwh-de-energia-electrica-a-paraguay-en-el-2025")
URL_YACYRETA = ("https://paraguayoindependiente.com/2026/01/21/"
                "yacyreta-muestra-una-senal-preocupante-para-paraguay/")


def _r(indicador, valor, unidad, periodo, fuente, url):
    return metadata.build_record(
        indicador, valor, unidad, periodo, fuente=fuente, url=url,
        metodo="extraccion_manual", estado="verificado")


CURADOS = [
    _r("generacion_itaipu_paraguay", 25768.0, "GWh", "2025",
       "Itaipú Binacional", URL_ITAIPU),
    _r("generacion_yacyreta_paraguay", 3081.0, "GWh", "2025",
       "Entidad Binacional Yacyretá", URL_YACYRETA),
    _r("generacion_yacyreta_total", 16103.0, "GWh", "2025",
       "Entidad Binacional Yacyretá", URL_YACYRETA),
]
