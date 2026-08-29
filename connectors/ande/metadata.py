from datetime import date

from . import normalizer


def build_record(indicador, valor, unidad, periodo_text, fuente, url,
                 metodo="extraccion_html", estado="extraido", entidad="ANDE",
                 documento=None, fecha_publicacion=None):
    fi, ff = normalizer.parse_period(periodo_text)
    return {
        "id": f"{entidad}-{indicador}-{fi}",
        "entidad": entidad,
        "indicador": indicador,
        "valor": valor,
        "unidad": unidad,
        "fecha_inicio": fi,
        "fecha_fin": ff,
        "fuente": fuente,
        "documento": documento,
        "url": url,
        "fecha_publicacion": fecha_publicacion,
        "fecha_extraccion": date.today().isoformat(),
        "metodo_extraccion": metodo,
        "estado_verificacion": estado,
    }
