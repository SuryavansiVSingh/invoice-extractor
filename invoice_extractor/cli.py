"""Command line: python -m invoice_extractor <folder-or-pdf> [-o out.xlsx]"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from openpyxl import Workbook

from .extract import Invoice, extract_invoice

COLUMNS = ["file", "supplier", "invoice_number", "invoice_date", "due_date", "vat", "total", "currency"]


def collect(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.pdf"))
    return [path]


def write_csv(rows: list[Invoice], out: Path) -> None:
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow(r.to_dict())


def write_xlsx(rows: list[Invoice], out: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoices"
    ws.append(COLUMNS)
    for r in rows:
        ws.append([r.to_dict()[c] for c in COLUMNS])
    ws.append([])
    ws.append(["TOTAL", None, None, None, None,
               f"=SUM(F2:F{len(rows) + 1})", f"=SUM(G2:G{len(rows) + 1})"])
    for col, width in zip("ABCDEFGH", [26, 24, 16, 13, 13, 10, 12, 9]):
        ws.column_dimensions[col].width = width
    wb.save(out)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Extract invoice data from PDFs into CSV or Excel.")
    p.add_argument("input", type=Path, help="PDF file or folder of PDFs")
    p.add_argument("-o", "--output", type=Path, default=Path("invoices.xlsx"),
                   help="Output file (.xlsx or .csv). Default: invoices.xlsx")
    args = p.parse_args(argv)

    files = collect(args.input)
    if not files:
        print("No PDF files found.", file=sys.stderr)
        return 1

    rows = []
    for f in files:
        try:
            rows.append(extract_invoice(f))
        except Exception as e:  # keep going if one file is broken
            print(f"Skipped {f.name}: {e}", file=sys.stderr)

    if args.output.suffix.lower() == ".csv":
        write_csv(rows, args.output)
    else:
        write_xlsx(rows, args.output)

    missing = [r.file for r in rows if r.total is None or r.invoice_number is None]
    print(f"Processed {len(rows)} invoice(s) -> {args.output}")
    if missing:
        print("Check manually (missing number or total): " + ", ".join(missing))
    return 0
