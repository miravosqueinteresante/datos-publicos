import re

PLANTS = {
    "itaipú": "itaipu", "itaipu": "itaipu",
    "yacyretá": "yacyreta", "yacyreta": "yacyreta",
    "acaray": "acaray",
}

CONSUMO = re.compile(r"consumo total lleg[oó] a\s*([\d.]+)\s*GWh", re.I)
DEMANDA = re.compile(r"demanda m[aá]xima.*?([\d.]+)\s*MW", re.I | re.S)
GEN = re.compile(r"(Itaip[uú]|Yacyret[aá]|Acaray)[^0-9]*?([\d.]+)\s*GWh", re.I)


def extract(html):
    recs = []
    m = CONSUMO.search(html)
    if m:
        recs.append({"indicador": "consumo_total", "valor_raw": m.group(1),
                     "unidad": "GWh", "periodo_text": "2025"})
    m = DEMANDA.search(html)
    if m:
        recs.append({"indicador": "demanda_maxima", "valor_raw": m.group(1),
                     "unidad": "MW", "periodo_text": "2025"})
    for g in GEN.finditer(html):
        plant = PLANTS.get(g.group(1).lower(), g.group(1).lower())
        recs.append({"indicador": f"generacion_{plant}", "valor_raw": g.group(2),
                     "unidad": "GWh", "periodo_text": "2025"})
    return recs


def _sin_acentos(s):
    return (s.lower()
            .replace("á", "a").replace("é", "e").replace("í", "i")
            .replace("ó", "o").replace("ú", "u").replace("ñ", "n"))


def _numero_linea(line):
    m = re.search(r"([\d.]+)\s*$", line)
    return m.group(1) if m else None


def extract_consumo_categoria(text):
    grupos = [
        ("muy alta tension", "consumo_categoria_muy_alta_tension"),
        ("alta tension", "consumo_categoria_alta_tension"),
        ("electrointensivas", "consumo_categoria_electrointensivas"),
        ("alumbrado publico", "consumo_categoria_alumbrado_publico"),
        ("gubernamental", "consumo_categoria_gubernamental"),
        ("diferencial", "consumo_categoria_diferencial"),
        ("industrial", "consumo_categoria_industrial"),
        ("otros", "consumo_categoria_otros"),
        ("residencial", "consumo_categoria_residencial"),
    ]
    recs = []
    norm = _sin_acentos(text)
    for linea, nlinea in zip(text.splitlines(), norm.splitlines()):
        for nombre, ind in grupos:
            if re.search(r"\b" + re.escape(nombre) + r"\b", nlinea):
                num = _numero_linea(linea)
                if num:
                    recs.append({"indicador": ind, "valor_raw": num,
                                 "unidad": "MWh", "periodo_text": "2025"})
                break
    return recs


def extract_tarifas(text):
    tramos = [
        ("0-50", "tarifa_residencial_bt_0_50"),
        ("51-150", "tarifa_residencial_bt_51_150"),
        ("151-300", "tarifa_residencial_bt_151_300"),
        ("301-500", "tarifa_residencial_bt_301_500"),
        ("501-1000", "tarifa_residencial_bt_501_1000"),
        (">1000", "tarifa_residencial_bt_mas_1000"),
    ]
    recs = []
    norm = _sin_acentos(text)
    for linea, nlinea in zip(text.splitlines(), norm.splitlines()):
        for tramo, ind in tramos:
            if tramo in nlinea and "kwh" in nlinea:
                m = re.search(r"([\d.,]+)\s*$", linea)
                if m:
                    recs.append({"indicador": ind, "valor_raw": m.group(1),
                                 "unidad": "G/kWh", "periodo_text": "2024"})
                break
    return recs


def extract_perdidas(text):
    patrones = [
        (r"perdidas totales[^%\n]*?([\d.,]+)\s*%", "perdidas_totales"),
        (r"perdidas en distribucion[^%\n]*?([\d.,]+)\s*%", "perdidas_distribucion"),
        (r"perdidas en transmision[^%\n]*?([\d.,]+)\s*%", "perdidas_transmision"),
    ]
    recs = []
    norm = _sin_acentos(text)
    for pat, ind in patrones:
        m = re.search(pat, norm, re.I)
        if m:
            recs.append({"indicador": ind, "valor_raw": m.group(1),
                         "unidad": "%", "periodo_text": "dic-2025"})
    return recs


def extract_clientes(text):
    recs = []
    norm = _sin_acentos(text)
    m = re.search(r"total de clientes[^0-9]*?([\d.]+)", norm, re.I)
    if m:
        recs.append({"indicador": "clientes_total", "valor_raw": m.group(1),
                     "unidad": "clientes", "periodo_text": "2025"})
    m2 = re.search(r"([\d.]+)\s*nuev(?:as|os)\s+(?:familias|clientes)", norm, re.I)
    if not m2:
        m2 = re.search(r"nuev(?:as|os) (?:familias|clientes)[^0-9]*?([\d.]+)", norm, re.I)
    if m2:
        recs.append({"indicador": "clientes_nuevos", "valor_raw": m2.group(1),
                     "unidad": "clientes", "periodo_text": "2025"})
    return recs


def pdf_text(path):
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError(
            "pdfplumber es requerido para extracción PDF (ver connectors/ande/requirements.txt)")
    with pdfplumber.open(path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)
