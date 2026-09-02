import json, re, unicodedata, urllib.request
from . import extractor, metadata, normalizer
BASE="https://www.eby.gov.py"
LIST_URL=f"{BASE}/generacion-de-energia/"
MESES={"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,"agosto":8,"septiembre":9,"setiembre":9,"octubre":10,"noviembre":11,"diciembre":12}
def fetch(url=None):
    if url is None:
        url=LIST_URL
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")
def _norm(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s or "") if not unicodedata.combining(c)).lower()
def _parse_year(html):
    n=_norm(html)
    m=re.search(r"(\d{1,2})\s+([a-z]+),?\s*(20\d{2})", n)
    if m and m.group(2) in MESES:
        return int(m.group(3))
    if m:
        return int(m.group(3))
    m2=re.search(r"20\d{2}", n)
    return int(m2.group(0)) if m2 else None
def discover_month_urls(list_html=None):
    links=[]
    if list_html is not None:
        links+=extractor.find_generation_links(list_html)
    else:
        try:
            links+=extractor.find_generation_links(fetch(LIST_URL))
        except Exception:
            pass
    try:
        sm=fetch(f"{BASE}/wp-sitemap.xml")
        locs=re.findall(r"<loc>([^<]+)</loc>", sm)
        for loc in locs:
            if "wp-sitemap-posts-post-" in loc:
                try:
                    txt=fetch(loc)
                    links+=re.findall(r"https://[^<\s\"]*generacion-de-yacyreta[^<\s\"]*", txt)
                except Exception:
                    continue
        if not locs:
            for i in range(1,8):
                try:
                    txt=fetch(f"{BASE}/wp-sitemap-posts-post-{i}.xml")
                    links+=re.findall(r"https://[^<\s\"]*generacion-de-yacyreta[^<\s\"]*", txt)
                except Exception:
                    continue
    except Exception:
        pass
    page=1
    while page<60:
        try:
            html=fetch(f"{BASE}/category/noticias/page/{page}/")
            found=re.findall(r"https://[^\"\s<]*generacion-de-yacyreta[^\"\s<]*", html)
            if not found:
                found=extractor.find_generation_links(html)
                found=[f for f in found if "generacion-de-yacyreta" in f]
            if not found:
                break
            links+=found
            page+=1
        except Exception:
            break
    out=[]
    for l in links:
        if l.startswith("http"):
            out.append(l)
        elif l.startswith("/"):
            out.append(BASE+l)
        else:
            out.append(l)
    return list(dict.fromkeys(out))
def discover_annual_urls():
    links = []
    try:
        sm = fetch(f"{BASE}/wp-sitemap.xml")
        locs = re.findall(r"<loc>([^<]+)</loc>", sm)
        for loc in locs:
            if "wp-sitemap-posts-post-" in loc:
                try:
                    txt = fetch(loc)
                    links += re.findall(r"https://[^<\s\"]*informe-de-produccion-anual[^<\s\"]*", txt)
                except Exception:
                    continue
        if not locs:
            for i in range(1, 8):
                try:
                    txt = fetch(f"{BASE}/wp-sitemap-posts-post-{i}.xml")
                    links += re.findall(r"https://[^<\s\"]*informe-de-produccion-anual[^<\s\"]*", txt)
                except Exception:
                    continue
    except Exception:
        pass
    out = []
    for l in links:
        if l.startswith("http"):
            out.append(l)
        elif l.startswith("/"):
            out.append(BASE + l)
        else:
            out.append(l)
    return list(dict.fromkeys(out))


def extract_annuals(urls=None, htmls=None):
    annuals = []
    if htmls is None:
        if urls is None:
            urls = discover_annual_urls()
        htmls = []
        for u in urls:
            try:
                h = fetch(u)
                y = _parse_year(h)
                htmls.append((u, h, y))
            except Exception:
                continue
    for u, h, y in htmls:
        r = extractor.extract_annual(h)
        if r and y and 1990 < y < 2030:
            annuals.append({"year": y, "total_mwh": r["total_mwh"], "sadi_mwh": r.get("sadi_mwh"), "sinp_mwh": r.get("sinp_mwh"), "url": u, "total_bruta": r.get("total_bruta"), "total_neta": r.get("total_neta")})
    return annuals


def fetch_month(url):
    return fetch(url)
def extract_months(urls=None, htmls=None):
    months=[]
    if htmls is None:
        if urls is None:
            urls=discover_month_urls()
        htmls=[]
        for u in urls:
            try:
                h=fetch_month(u)
                y=_parse_year(h)
                htmls.append((u,h,y))
            except Exception:
                continue
    for u,h,y in htmls:
        r=extractor.extract_month(h)
        if r and y and 1990 < y < 2030:
            months.append({"year":y,"total_mwh":r["total_mwh"],"sadi_mwh":r["sadi_mwh"],"sinp_mwh":r["sinp_mwh"],"url":u})
    return months
def normalize(months, annuals=None):
    annuals = annuals or []
    yearly = normalizer.aggregate_yearly(months) if months else []
    by_ann = {a["year"]: a for a in annuals if a.get("year") and a.get("total_mwh") is not None}
    out = []
    for a in sorted(annuals, key=lambda x: x["year"]):
        if a["year"] not in by_ann:
            continue
        out.append(("generacion_total", normalizer.mwh_to_gwh(a["total_mwh"]), "GWh", a["year"]))
        if a.get("sadi_mwh") is not None:
            out.append(("suministro_argentina", normalizer.mwh_to_gwh(a["sadi_mwh"]), "GWh", a["year"]))
        if a.get("sinp_mwh") is not None:
            out.append(("suministro_paraguay", normalizer.mwh_to_gwh(a["sinp_mwh"]), "GWh", a["year"]))
    for y in yearly:
        if y["year"] in by_ann:
            continue
        if y.get("meses", 12) < 9:
            continue
        out.append(("generacion_total",normalizer.mwh_to_gwh(y["total_mwh"]),"GWh",y["year"]))
        out.append(("suministro_argentina",normalizer.mwh_to_gwh(y["sadi_mwh"]),"GWh",y["year"]))
        out.append(("suministro_paraguay",normalizer.mwh_to_gwh(y["sinp_mwh"]),"GWh",y["year"]))
    return sorted(out, key=lambda x: (x[3], x[0]))
def build(normalized, url=LIST_URL):
    recs=[]
    for ind,val,uni,year in normalized:
        recs.append(metadata.build_record(ind,val,uni,year,fuente="EBY",url=url))
    return recs
def store(records, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
