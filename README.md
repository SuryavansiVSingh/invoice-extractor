# Invoice Extractor 🧾 → 📊

Turn a folder of PDF invoices into one clean Excel or CSV file.
Works with **Dutch (Belgium / Netherlands)** and **English** invoices.

Small businesses often type invoice details into a spreadsheet by hand. This tool reads each PDF and pulls out the fields you actually need for bookkeeping.

| Field | Examples it understands |
|---|---|
| Supplier | first line of the invoice |
| Invoice number | `Invoice Number`, `Factuurnummer`, `Factuur nr.` |
| Invoice date | `Invoice Date`, `Factuurdatum`, `Datum` |
| Due date | `Due Date`, `Vervaldatum`, `Te betalen voor` |
| VAT | `VAT 21%`, `BTW 6%` |
| Total | `Total due`, `Totaal`, `Totaal te betalen` |

Amounts in any common format are handled: `1.234,56` · `1,234.56` · `1 234,56`.

## Quick start

```bash
pip install -r requirements.txt
python -m invoice_extractor path/to/invoices -o invoices.xlsx
```

Output for the fictional sample invoices (create them with `python samples/make_samples.py`):

| file | supplier | invoice_number | invoice_date | due_date | vat | total |
|---|---|---|---|---|---|---|
| factuur_bakkerij_zonneveld.pdf | Bakkerij Zonneveld BV | BZ-2026-0142 | 14/09/2026 | 14/10/2026 | 49.20 | 869.20 |
| factuur_drukkerij_vanneste.pdf | Drukkerij Vanneste | 2026/553 | 01.10.2026 | 31.10.2026 | 239.40 | 1379.40 |
| invoice_northwind_studio.pdf | Northwind Studio Ltd | NW-00087 | 2026-09-02 | 2026-09-30 | 262.50 | 1512.50 |

The Excel file also gets a **TOTAL** row with live `SUM` formulas. Invoices where the number or total couldn't be found are listed in the terminal so you can check them by hand.

## How it works

1. `pdfplumber` reads the text from each PDF page.
2. Regular expressions look for each label in English and Dutch and grab the value next to it.
3. Amounts are normalised (European vs. US decimal separators).
4. Results are written to Excel (`openpyxl`) or CSV.

## Run the tests

```bash
pip install -r requirements-dev.txt
pytest            # generates the fictional sample PDFs, then runs the tests
```

## Limitations / next steps

- Text-based PDFs only. Scanned invoices need OCR first (e.g. Tesseract).
- Unusual layouts may need extra label patterns in `invoice_extractor/extract.py`.
- Planned: optional AI fallback for invoices the rules can't read, and a simple drag-and-drop web page.

All companies in `samples/` are fictional.

## License

MIT
