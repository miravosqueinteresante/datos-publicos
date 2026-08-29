import re
from datetime import date, timedelta


def parse_number(text):
    s = str(text).strip()
    s = s.replace("%", "").strip()
    s = re.sub(r"(?i)\b(GWh|MWh|kWh|MW|kW)\b", "", s).strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    elif "." in s and re.search(r"\.\d{3}$", s) and s.count(".") == 1:
        s = s.replace(".", "")
    return float(s)


_MONTHS = {
    "ene": 1, "enero": 1, "feb": 2, "mar": 3, "abr": 4, "abril": 4,
    "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "set": 9,
    "oct": 10, "nov": 11, "dic": 12, "diciembre": 12,
}


def parse_period(text):
    text = str(text).strip().lower()
    if re.fullmatch(r"\d{4}", text):
        y = int(text)
        return (f"{y}-01-01", f"{y}-12-31")
    m = re.fullmatch(r"([a-zé]+)-(\d{4})", text)
    if m and m.group(1) in _MONTHS:
        mon = _MONTHS[m.group(1)]
        y = int(m.group(2))
        last = 31 if mon == 12 else (date(y, mon + 1, 1) - timedelta(days=1)).day
        return (f"{y}-{mon:02d}-01", f"{y}-{mon:02d}-{last:02d}")
    ym = re.search(r"(\d{4})", text)
    if ym:
        y = int(ym.group(1))
        return (f"{y}-01-01", f"{y}-12-31")
    raise ValueError(f"Periodo no reconocido: {text}")


def convert_energy(value, unit):
    unit = unit.strip().upper()
    value = float(value)
    if unit == "GWH":
        return (value, "GWh")
    if unit == "MWH":
        return (value / 1000.0, "GWh")
    if unit == "KWH":
        return (value / 1_000_000.0, "GWh")
    raise ValueError(f"Unidad de energía no soportada: {unit}")
