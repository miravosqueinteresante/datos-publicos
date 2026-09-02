import json, re, urllib.request
from . import extractor, metadata, normalizer

BASE = "https://www.eby.gov.py"
LIST_URL = f"{BASE}/generacion-de-energia/"

def fetch(url=None):
    if url is None:
        url = LIST_URL
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")

def discover_month_urls(list_html=None):
    if list_html is None:
        list_html = fetch(LIST_URL)
    links = extractor.find_generation_links(list_html)
    if len(links) < 5:
        try:
            sm = fetch(f"{BASE}/wp-sitemap.xml")
            links += re.findall(r'https://[^<]*generacion-de-yacyreta[^<]*', sm)
        except Exception:
            pass
    abs_links = []
    for l in links:
        if l.startswith("http"):
            abs_links.append(l)
        elif l.startswith("/"):
            abs_links.append(BASE + l)
        else:
            abs_links.append(l)
    return list(dict.fromkeys(abs_links))

def fetch_month(url):
    return fetch(url)

def extract_months(urls=None, htmls=None):
    months = []
    if htmls is None:
        if urls is None:
            urls = discover_month_urls()
        htmls = []
        for u in urls:
            try:
                h = fetch_month(u)
                m = re.search(r"(\d{1,2})\s+\w+,\s*(\d{4})", h)
                year = int(m.group(2)) if m else None
                if not year:
                    m2 = re.search(r"20\d{2}", h)
                    year = int(m2.group(0)) if m2 else None
                htmls.append((u, h, year))
            except Exception:
                continue
    for u, h, y in htmls:
        r = extractor.extract_month(h)
        if r and y and 1990 < y < 2030:
            months.append({"year": y, "total_mwh": r["total_mwh"], "sadi_mwh": r["sadi_mwh"], "sinp_mwh": r["sinp_mwh"], "url": u})
    return months

def normalize(months):
    yearly = normalizer.aggregate_yearly(months)
    out = []
    for y in yearly:
        if y.get("meses", 12) < 9:
            continue
        out.append(("generacion_total", normalizer.mwh_to_gwh(y["total_mwh"]), "GWh", y["year"]))
        out.append(("suministro_argentina", normalizer.mwh_to_gwh(y["sadi_mwh"]), "GWh", y["year"]))
        out.append(("suministro_paraguay", normalizer.mwh_to_gwh(y["sinp_mwh"]), "GWh", y["year"]))
    return out

def build(normalized, url=LIST_URL):
    recs = []
    for ind, val, uni, year in normalized:
        recs.append(metadata.build_record(ind, val, uni, year, fuente="EBY", url=url))
    return recs

def store(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
