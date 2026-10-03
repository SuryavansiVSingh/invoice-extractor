"""Generate fictional sample invoices for testing (all companies are made up)."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

HERE = Path(__file__).parent

SAMPLES = [
    ("factuur_bakkerij_zonneveld.pdf", [
        "Bakkerij Zonneveld BV",
        "Kerkstraat 12, 8000 Brugge",
        "",
        "Factuurnummer: BZ-2026-0142",
        "Factuurdatum: 14/09/2026",
        "Vervaldatum: 14/10/2026",
        "",
        "Broodleveringen september        € 820,00",
        "Subtotaal                        € 820,00",
        "BTW 6%                           € 49,20",
        "Totaal te betalen                € 869,20",
    ]),
    ("invoice_northwind_studio.pdf", [
        "Northwind Studio Ltd",
        "21 Example Road, London",
        "",
        "Invoice Number: NW-00087",
        "Invoice Date: 2026-09-02",
        "Due Date: 2026-09-30",
        "",
        "Website maintenance (10 h)       EUR 1.250,00",
        "Subtotal                         EUR 1.250,00",
        "VAT 21%                          EUR 262,50",
        "Total due                        EUR 1.512,50",
    ]),
    ("factuur_drukkerij_vanneste.pdf", [
        "Drukkerij Vanneste",
        "Industrielaan 5, 8370 Blankenberge",
        "",
        "Factuur nr.: 2026/553",
        "Datum: 01.10.2026",
        "Te betalen voor: 31.10.2026",
        "",
        "Flyers A5 (2.000 st.)            € 1 140,00",
        "Subtotaal                        € 1 140,00",
        "BTW 21%                          € 239,40",
        "Totaal                           € 1 379,40",
    ]),
]


def build():
    for name, lines in SAMPLES:
        c = canvas.Canvas(str(HERE / name), pagesize=A4)
        y = 800
        for i, line in enumerate(lines):
            c.setFont("Helvetica-Bold" if i == 0 else "Courier", 14 if i == 0 else 10)
            c.drawString(60, y, line)
            y -= 20
        c.save()


if __name__ == "__main__":
    build()
    print("Samples written to", HERE)
