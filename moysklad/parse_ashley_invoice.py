#!/usr/bin/env python3
"""Parse Ashley "Consolidated Invoice" PDFs (from ECommServ@ashleyfurniture.com) into trip rows.

Usage: python3 -I moysklad/parse_ashley_invoice.py OUT.csv INVOICE.pdf [INVOICE.pdf ...]
Writes/appends rows `trip;article;qty;eta;note` (same format as trips.csv).
ETA rule: invoice date + 35 days. Needs `pdftotext` (poppler-utils).
"""
import csv, datetime, os, re, subprocess, sys

ITEM = re.compile(r"^\s*([A-Z0-9][A-Z0-9-]+)\s+(?:([A-Z])\s+)?([A-Z]{2})\s+(\d+)\s+(\d+)\s+(\d+)\s+"
                  r"([\d,]+\.\d\d)\s+([\d,]+\.\d\d)\s+(?:([\d,]+\.\d\d)\s+)?([\d,]+\.\d\d)\s+([\d,]+\.\d\d)\s*$")
ETA_DAYS = 35


def parse(pdf):
    text = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True, text=True).stdout
    lines = text.splitlines()
    inv = trip = inv_date = None
    rows, totals, due = [], {}, {}
    for i, l in enumerate(lines):
        m = re.search(r"INVOICE NUMBER:\s*(\d+)", l)
        if m:
            inv = m.group(1)
        m = re.search(r"^\s*(\d\d)/(\d\d)/(\d{4})\s+\d+\s+\$", l)
        if m:
            inv_date = datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2)))
        # "C473035  CBD  40HC  037823 01 335"  or  "C073867  CBD  40HC  025277  335"
        m = re.match(r"^\s*[A-Z]\d{5,}\s.*?\s0*(\d{4,6})(?:\s+\d\d)?\s+\d{2,4}\s*$", l)
        if m:
            trip = m.group(1)
        m = re.search(r"AMOUNT DUE \(USD\)\s+\$\s*([\d,]+\.\d\d)", l)
        if m:
            due[inv] = float(m.group(1).replace(",", ""))
        m = ITEM.match(l)
        if m:
            desc = lines[i + 1].strip() if i + 1 < len(lines) else ""
            ext = float(m.group(11).replace(",", ""))
            totals[inv] = totals.get(inv, 0) + ext
            rows.append({"trip": trip, "article": m.group(1), "ordered": int(m.group(5)),
                         "shipped": int(m.group(6)), "inv": inv, "date": inv_date, "desc": desc, "b": m.group(2) or ""})
    bad = {k: (round(totals.get(k, 0), 2), v) for k, v in due.items() if abs(totals.get(k, 0) - v) > 0.02}
    return rows, bad


def main():
    out, pdfs = sys.argv[1], sys.argv[2:]
    new = not os.path.exists(out)
    with open(out, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if new:
            w.writerow(["trip", "article", "qty", "eta", "note"])
        for pdf in pdfs:
            rows, bad = parse(pdf)
            trips = sorted({r["trip"] for r in rows})
            qty = sum(r["shipped"] for r in rows)
            short = [(r["article"], r["ordered"], r["shipped"]) for r in rows if r["shipped"] < r["ordered"]]
            print(f"{os.path.basename(pdf)}: trip {','.join(trips)} | строк {len(rows)} | шт {qty} | "
                  f"недогруз {short or 'нет'} | {'суммы сходятся' if not bad else 'РАСХОЖДЕНИЕ СУММ ' + str(bad)}")
            for r in rows:
                eta = (r["date"] + datetime.timedelta(days=ETA_DAYS)).isoformat() if r["date"] else ""
                w.writerow([r["trip"], r["article"], r["shipped"], eta,
                            f"инвойс {r['inv']} от {r['date']}; {r['desc']}" + ("; backorder" if r["b"] else "")])


if __name__ == "__main__":
    main()
