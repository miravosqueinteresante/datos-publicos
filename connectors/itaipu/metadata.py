from datetime import date


def build_record(indicador, valor, unidad, year, fuente, url,
                 metodo="extraccion_api", estado="extraido"):
    return {
        "id": f"itaipu-{indicador}-{year}",
        "entidad": "Itaipú Binacional",
        "entidad_id": "itaipu",
        "indicador": indicador,
        "valor": valor,
        "unidad": unidad,
        "fecha_inicio": f"{year}-01-01",
        "fecha_fin": f"{year}-12-31",
        "fuente": fuente,
        "documento": None,
        "url": url,
        "fecha_publicacion": None,
        "fecha_extraccion": date.today().isoformat(),
        "metodo_extraccion": metodo,
        "estado_verificacion": estado,
    }
