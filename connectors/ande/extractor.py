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


def _norm(s):
    if s is None:
        return ""
    return (s.lower()
            .replace("á", "a").replace("é", "e").replace("í", "i")
            .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
            .replace(" ", " "))


def _flat(t):
    return " ".join(_norm(c) for row in t for c in row if c)


# ---- PDF text (pérdidas) ----

def extract_perdidas(text):
    patrones = [
        (r"perdidas totales[^%\n]*?([\d.,]+)\s*%", "perdidas_totales"),
        (r"perdidas en distribucion[^%\n]*?([\d.,]+)\s*%", "perdidas_distribucion"),
        (r"perdidas en transmision[^%\n]*?([\d.,]+)\s*%", "perdidas_transmision"),
    ]
    recs = []
    norm = _norm(text)
    for pat, ind in patrones:
        ms = list(re.finditer(pat, norm, re.I))
        if not ms:
            continue
        val = ms[0].group(1)
        if ind == "perdidas_distribucion" and len(ms) > 1:
            vals = [m.group(1) for m in ms]
            if "20,03" in vals:
                val = "20,03"
            elif "20.03" in vals:
                val = "20.03"
            else:
                val = ms[-1].group(1)
        recs.append({"indicador": ind, "valor_raw": val,
                     "unidad": "%", "periodo_text": "dic-2025"})
    return recs


# ---- PDF tables ----

CAT_MAP = {
    "residencial": "residencial",
    "industrial": "industrial",
    "otros": "otros",
    "gubernamental": "gubernamental",
    "diferencial": "diferencial",
    "alta tension": "alta_tension",
    "muy alta tension": "muy_alta_tension",
    "consumidores intensivo especial": "electrointensivas",
    "alumbrado publico": "alumbrado_publico",
}

RANGE_MAP = {
    "0 - 50 kwh": "0_50",
    "51 - 150 kwh": "51_150",
    "151 - 300 kwh": "151_300",
    "301 - 500 kwh": "301_500",
    "501 - 1000 kwh": "501_1000",
    "mayor a 1000 kwh": "mas_1000",
}


def _find_table(tables, *needles):
    needles = [_norm(n) for n in needles]
    for t in tables:
        f = _norm(_flat(t))
        if all(n in f for n in needles):
            return t
    return None


def extract_clientes(tables):
    t = _find_table(tables, "cantidad de", "usuarios", "categoria")
    if not t:
        return []
    for row in t:
        if _norm(row[0]).strip() == "total" and len(row) >= 3 and row[2]:
            return [{"indicador": "clientes_total", "valor_raw": row[2].strip(),
                     "unidad": "clientes", "periodo_text": "2025"}]
    return []


def extract_consumo_categoria(tables):
    t = _find_table(tables, "cantidad de", "usuarios", "categoria")
    if not t:
        return []
    recs = []
    for row in t:
        if not row or not row[0]:
            continue
        slug = CAT_MAP.get(_norm(row[0]).strip())
        if slug and len(row) >= 2 and row[1]:
            recs.append({"indicador": f"consumo_categoria_{slug}",
                         "valor_raw": row[1].strip(), "unidad": "kWh",
                         "periodo_text": "2025"})
    return recs


def extract_clientes_categoria(tables):
    t = _find_table(tables, "cantidad de", "usuarios", "categoria")
    if not t:
        return []
    recs = []
    for row in t:
        if not row or not row[0]:
            continue
        slug = CAT_MAP.get(_norm(row[0]).strip())
        if slug and len(row) >= 3 and row[2] and row[2].strip() not in ("", "-"):
            recs.append({"indicador": f"clientes_categoria_{slug}",
                         "valor_raw": row[2].strip(), "unidad": "clientes",
                         "periodo_text": "2025"})
    return recs


def extract_generacion_serie(tables):
    t = _find_table(tables, "origen de la energia", "itaipu y yacyreta", "acaray")
    if not t:
        return []
    data = None
    for row in t:
        if row and row[0] and "\n" in row[0] and re.match(r"\d{4}", row[0].strip()):
            data = row
            break
    if not data:
        return []
    years = [y.strip() for y in data[0].split("\n") if re.match(r"\d{4}", y.strip())]

    def col(idx):
        if idx >= len(data) or not data[idx]:
            return []
        return [v.strip() for v in data[idx].split("\n") if v.strip()]

    acaray = col(1)
    binac = col(3)
    recs = []
    for i, year in enumerate(years):
        if i < len(acaray) and acaray[i]:
            recs.append({"indicador": "generacion_nacional_acaray_termicas",
                         "valor_raw": acaray[i], "unidad": "MWh", "periodo_text": year})
        if i < len(binac) and binac[i]:
            recs.append({"indicador": "generacion_binacional_itaipu_yacyreta",
                         "valor_raw": binac[i], "unidad": "MWh", "periodo_text": year})
    return recs


def extract_sin_indicators(tables):
    t = _find_table(tables, "factor de carga", "año 2025")
    if not t:
        return []
    periodo = "2025"
    for row in t:
        if row and any("año 2025" in _norm(c) for c in row if c):
            periodo = row[2].strip() if len(row) > 2 and row[2] else "2025"
    recs = []
    for row in t:
        if not row:
            continue
        n = _norm(row[0])
        if "consumo de energia electrica" in n and len(row) >= 3 and row[2]:
            recs.append({"indicador": "consumo_total", "valor_raw": row[2].strip(),
                         "unidad": "MWh", "periodo_text": periodo})
        elif "demanda maxima de potencia" in n and len(row) >= 3 and row[2]:
            recs.append({"indicador": "demanda_maxima", "valor_raw": row[2].strip(),
                         "unidad": "MW", "periodo_text": periodo})
        elif "factor de carga anual" in n and len(row) >= 3 and row[2]:
            recs.append({"indicador": "factor_carga", "valor_raw": row[2].strip(),
                         "unidad": "%", "periodo_text": periodo})
    return recs


def extract_tarifas(tables):
    t = _find_table(tables, "faja de consumo", "mayor a 1000 kwh")
    if not t:
        t = _find_table(tables, "faja de consumo", "g/kwh")
    if not t:
        return []
    recs = []
    for row in t:
        if not row or not row[0]:
            continue
        slug = RANGE_MAP.get(_norm(row[0]).strip())
        if slug and len(row) >= 3 and row[1]:
            recs.append({"indicador": f"tarifa_residencial_bt_{slug}",
                         "valor_raw": row[1].strip(), "unidad": "G/kWh",
                         "periodo_text": "2021"})
    return recs


def pdf_text(path):
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError(
            "pdfplumber es requerido para extracción PDF (ver connectors/ande/requirements.txt)")
    with pdfplumber.open(path) as pdf:
        return "\n".join((page.extract_text() or "") for page in pdf.pages)


def pdf_tables(path):
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError(
            "pdfplumber es requerido para extracción PDF (ver connectors/ande/requirements.txt)")
    with pdfplumber.open(path) as pdf:
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())
    return tables
