#!/usr/bin/env python3
"""Daily list of Ashley items sold in MoySklad customer orders (for re-ordering in Ashley Workbench).

Usage: python3 moysklad/ashley_sold.py [YYYY-MM-DD] [--out DIR]
Auth: the session's network proxy injects the MoySklad token for api.moysklad.ru;
no token is read or stored here. Read-only: only GET requests.
"""
import argparse, collections, csv, datetime, gzip, json, os, re, sys, urllib.parse, urllib.request

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
    ap.add_argument("--from", dest="date_from", help="YYYY-MM-DD: report a period from this date to <date>")
    ap.add_argument("--trips", action="append", default=[],
                    help="extra trips CSV (e.g. parsed from Ashley invoices); a trip found here replaces "
                         "the same trip's rows in moysklad/trips.csv")
    args = ap.parse_args()
    day = args.date or datetime.date.today().isoformat()

    orders = get_all("/entity/customerorder", limit=100,
                     filter=f"moment>={args.date_from or day} 00:00:00;moment<={day} 23:59:59",
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
            if comps:
                it["components"] = [(c["assortment"]["meta"]["href"].split("?")[0], c["quantity"]) for c in comps]
            it["orders"].append(f"{o['name']} ({o.get('agent', {}).get('name', '')})")

    # stock per product
    stock = {}
    if items:
        for r in get_all("/report/stock/all", limit=1000):
            href = r["meta"]["href"].split("?")[0]
            stock[href] = r
    # In transit, one entry per trip:
    #  1) open MoySklad purchase orders (status not "Получено"/"Возврат поставщику"):
    #     ordered minus received; trip = first number in the PO description, else the PO number;
    #  2) moysklad/trips.csv: trips not yet entered into MoySklad (trip;article;qty;eta;note).
    #     Rows of a trip that already appears in a MoySklad PO description are skipped (no double count).
    transit = collections.defaultdict(list)  # href or article -> [{trip, qty, eta, src}]
    ms_trips = set()
    if items:
        for po in get_all("/entity/purchaseorder", limit=100, expand="state", order="moment,desc"):
            st = (po.get("state") or {}).get("name", "")
            if st in ("Получено", "Возврат поставщику") or not po.get("applicable"):
                continue
            desc = po.get("description") or ""
            m = re.search(r"\d{3,}", desc)
            trip = m.group(0) if m else f"заказ {po['name']}"
            if m:
                ms_trips.add(trip)
            eta = (po.get("deliveryPlannedMoment") or "")[:10]
            for p in get_all(po["positions"]["meta"]["href"], limit=1000):
                left = p["quantity"] - p.get("shipped", 0)
                if left <= 0 or p["assortment"]["meta"]["type"] == "variant":
                    continue
                href = p["assortment"]["meta"]["href"].split("?")[0]
                transit[href].append({"trip": trip, "qty": left, "eta": eta, "src": f"МойСклад {po['name']} ({st})"})
    trips_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trips.csv")
    by_trip = {}  # trip -> rows; later files override earlier ones for the same trip
    for fn in [trips_file] + args.trips:
        if not (items and os.path.exists(fn)):
            continue
        cur = collections.defaultdict(list)
        with open(fn, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                trip = (r.get("trip") or "").strip()
                if trip and (r.get("article") or "").strip():
                    cur[trip].append(r)
        by_trip.update(cur)
    for trip, rs in by_trip.items():
        if trip in ms_trips:
            continue
        for r in rs:
            transit["art:" + r["article"].strip().upper()].append(
                {"trip": trip, "qty": float(r.get("qty") or 0), "eta": (r.get("eta") or "").strip(),
                 "src": "инвойс Ashley"})

    # ETA overrides from the manager's delivery table (moysklad/trip_eta.csv)
    eta_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trip_eta.csv")
    if os.path.exists(eta_file):
        with open(eta_file, encoding="utf-8-sig") as f:
            over = {r["trip"].strip(): r["eta"].strip() for r in csv.DictReader(f, delimiter=";")}
        for lst in transit.values():
            for t in lst:
                if t["trip"] in over: t["eta"] = over[t["trip"]]
    for it in items.values():
        s = stock.get(it["href"], {})
        it["available"] = s.get("stock", 0) - s.get("reserve", 0)
        if it.get("components"):  # bundle (e.g. modular sofa "8614055/56"): no own stock -> sets buildable from parts
            def avail(h):
                r = stock.get(h, {})
                return r.get("stock", 0) - r.get("reserve", 0)
            it["available"] = max(0, min(avail(h) // q for h, q in it["components"] if q))
        it["transit"] = transit.get(it["href"], []) + transit.get("art:" + str(it["article"]).upper(), [])

    rows = sorted(items.values(), key=lambda x: (x["folder"], x["name"]))
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, f"ashley_plan_{args.date_from + '_' if args.date_from else ''}{day}.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Code", "Название", "Продано", "Доступно", "В пути, qty", "Trip", "Дата", "Источник", "Заказы покупателей"])
        for it in rows:
            base = [it["article"], it["name"], f"{it['qty']:g}", f"{it['available']:g}"]
            tr = it["transit"] or [{"trip": "", "qty": 0, "eta": "", "src": ""}]
            for i, t in enumerate(tr):
                w.writerow((base if i == 0 else ["", "", "", ""]) +
                           [f"{t['qty']:g}" if t["trip"] else "0", t["trip"], t["eta"], t["src"],
                            "; ".join(it["orders"]) if i == 0 else ""])

    print(f"Ashley заказ план | дата продаж: {(args.date_from + '..') if args.date_from else ''}{day} | заказов покупателей: {len(orders)} | позиций Ashley: {len(rows)} | CSV: {path}")
    for it in rows:
        tr = "; ".join(f"{t['qty']:g} шт trip {t['trip']} ~{t['eta']}" for t in it["transit"]) or "—"
        print(f"{it['article']} | {it['name']} | продано {it['qty']:g} | доступно {it['available']:g} | в пути: {tr}")


if __name__ == "__main__":
    sys.exit(main())
