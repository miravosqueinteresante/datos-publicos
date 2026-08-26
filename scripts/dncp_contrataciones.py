def es_de_asuncion(texto):
    if not texto:
        return False
    t = texto.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")
    return "municipalidad de asuncion" in t