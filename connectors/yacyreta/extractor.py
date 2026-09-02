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


def find_generation_links(html):
    m = re.findall(r'href="([^"]*generacion-de-yacyreta[^"]*)"', html)
    seen = set()
    out = []
    for u in m:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out
