#!/usr/bin/env python3
"""Daily list of Ashley items sold in MoySklad customer orders (for re-ordering in Ashley Workbench).

Usage: python3 moysklad/ashley_sold.py [YYYY-MM-DD] [--out DIR]
Auth: the session's network proxy injects the MoySklad token for api.moysklad.ru;
no token is read or stored here. Read-only: only GET requests.
"""
import argparse, collections, csv, datetime, gzip, json, os, sys, urllib.parse, urllib.request

API = "https://api.moysklad.ru/api/remap/1.2"
BRAND_ATTR = "Бренд товара"
BRAND = "ashley"


def get(path, **params):
    url = path if path.startswith("http") else API + path
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip", "Accept": "application/json;charset=utf-8"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
    return json.loads(data)


def get_all(path, limit=100, **params):
    off, out = 0, []
    while True:
        d = get(path, limit=limit, offset=off, **params)
        out += d["rows"]
        off += limit
        if off >= d["meta"]["size"]:
            return out


def brand_of(entity):
    for a in entity.get("attributes", []):
        if a.get("name") == BRAND_ATTR:
            v = a.get("value")
            return (v.get("name") if isinstance(v, dict) else str(v)) or ""
    return ""


_cache = {}


def product_for(assortment):
    """Return the product card (with attributes) for a product / variant / bundle position."""
    t = assortment["meta"]["type"]
    if t == "variant":
        href = assortment["product"]["meta"]["href"]
        if href not in _cache:
            _cache[href] = get(href)
        return _cache[href]
    return assortment


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("date", nargs="?", help="YYYY-MM-DD (default: today, account time)")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    day = args.date or datetime.date.today().isoformat()

    orders = get_all("/entity/customerorder", limit=100,
                     filter=f"moment>={day} 00:00:00;moment<={day} 23:59:59",
                     expand="agent,owner,positions.assortment")

    items = collections.OrderedDict()
    for o in orders:
        positions = o.get("positions", {})
        rows = positions.get("rows", [])
        if positions.get("meta", {}).get("size", 0) > len(rows):  # more than expanded
            rows = get_all(positions["meta"]["href"], expand="assortment")
        for p in rows:
            a = p["assortment"]
            prod = product_for(a)
            comps = []
            if a["meta"]["type"] == "bundle":
                comps = get_all(a["components"]["meta"]["href"], expand="assortment")
            if BRAND not in brand_of(prod).lower():
                continue
            key = a.get("article") or prod.get("article") or a.get("code") or a["name"]
            it = items.setdefault(key, {"article": key, "name": a["name"], "qty": 0, "orders": [],
                                        "href": prod["meta"]["href"], "folder": prod.get("pathName", "")})
            it["qty"] += p["quantity"]
            it["orders"].append(f"{o['name']} ({o.get('agent', {}).get('name', '')})")

    # stock per product
    stock = {}
    if items:
        for r in get_all("/report/stock/all", limit=1000):
            href = r["meta"]["href"].split("?")[0]
            stock[href] = r
    for it in items.values():
        s = stock.get(it["href"], {})
        it["stock"] = s.get("stock", 0)
        it["reserve"] = s.get("reserve", 0)
        it["inTransit"] = s.get("inTransit", 0)

    rows = sorted(items.values(), key=lambda x: (x["folder"], x["name"]))
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, f"ashley_sold_{day}.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Артикул Ashley", "Название", "Продано, шт", "Остаток", "Резерв", "В пути", "Категория", "Заказы"])
        for it in rows:
            w.writerow([it["article"], it["name"], f"{it['qty']:g}", f"{it['stock']:g}", f"{it['reserve']:g}",
                        f"{it['inTransit']:g}", it["folder"], "; ".join(it["orders"])])

    print(f"Дата: {day} | заказов покупателей: {len(orders)} | позиций Ashley: {len(rows)} | CSV: {path}")
    print(json.dumps(rows, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main())
