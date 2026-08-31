from datetime import date

from . import entidad as entidad_mod, normalizer


def build_record(indicador, valor, unidad, periodo_text, fuente, url,
                 metodo="extraccion_html", estado="extraido", entidad="ANDE",
                 documento=None, fecha_publicacion=None):
    eid = entidad_mod.nombre_a_id(entidad) if isinstance(entidad, str) else entidad
    if eid is None:
        eid = "ande"
    fi, ff = normalizer.parse_period(periodo_text)
    return {
        "id": f"{eid}-{indicador}-{fi}",
        "entidad": entidad,
        "entidad_id": eid,
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
