import re
import unicodedata


def _norm(s):
    nfkd = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def extract_month(html):
    n = _norm(html)
    m_total = re.search(r"total.*?([\d.]+,\d+|\d+\.\d+|\d+)\s*mwh", n)
    m_sadi = re.search(r"sadi[^0-9]*([\d.]+,\d+|\d+\.\d+|\d+)\s*mwh", n)
    m_sinp = re.search(r"sinp[^0-9]*([\d.]+,\d+|\d+\.\d+|\d+)\s*mwh", n)
    if not m_total:
        m_total = re.search(r"([\d.]+,\d+)\s*mwh", n)
    def parse(v):
        if not v:
            return None
        v = v.replace(".", "").replace(",", ".")
        try:
            return float(v)
        except:
            return None
    total = parse(m_total.group(1)) if m_total else None
    sadi = parse(m_sadi.group(1)) if m_sadi else None
    sinp = parse(m_sinp.group(1)) if m_sinp else None
    if total is None:
        return None
    return {"total_mwh": total, "sadi_mwh": sadi, "sinp_mwh": sinp}


def extract(html):
    r = extract_month(html)
    return [r] if r else []


def extract_annual(html):
    n = _norm(html)
    m_bruta = re.search(r"generacion bruta de\s*([\d.]+)\s*mwh", n)
    m_neta = re.search(r"generacion total neta fue de\s*([\d.]+)\s*mwh", n)
    m_sinp = re.search(r"sinp\s*([\d.,]+)\s*mwh", n)
    m_sadi = re.search(r"sadi\s*([\d.,]+)\s*mwh", n)

    def parse(v):
        if not v:
            return None
        v = v.replace(".", "").replace(",", ".")
        try:
            return float(v)
        except:
            return None

    total_bruta = parse(m_bruta.group(1)) if m_bruta else None
    total_neta = parse(m_neta.group(1)) if m_neta else None
    sinp = parse(m_sinp.group(1)) if m_sinp else None
    sadi = parse(m_sadi.group(1)) if m_sadi else None
    total = total_neta if total_neta is not None else total_bruta
    if total is None:
        return None
    return {"total_mwh": total, "total_bruta": total_bruta, "total_neta": total_neta, "sadi_mwh": sadi, "sinp_mwh": sinp}


def find_annual_links(html):
    m = re.findall(r'href="([^"]*informe-de-produccion-anual[^"]*)"', html, flags=re.IGNORECASE)
    seen = set()
    out = []
    for u in m:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def find_generation_links(html):
    m = re.findall(r'href="([^"]*generacion-de-yacyreta[^"]*)"', html)
    seen = set()
    out = []
    for u in m:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out
