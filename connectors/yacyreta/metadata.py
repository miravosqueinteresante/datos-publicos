from datetime import date

def build_record(indicador, valor, unidad, year, fuente, url, metodo="extraccion_html", estado="extraido"):
    return {"id": f"yacyreta-{indicador}-{year}", "entidad": "Entidad Binacional Yacyretá", "entidad_id": "yacyreta", "indicador": indicador, "valor": valor, "unidad": unidad, "fecha_inicio": f"{year}-01-01", "fecha_fin": f"{year}-12-31", "fuente": fuente, "documento": None, "url": url, "fecha_publicacion": None, "fecha_extraccion": date.today().isoformat(), "metodo_extraccion": metodo, "estado_verificacion": estado}
