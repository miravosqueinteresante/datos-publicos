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
