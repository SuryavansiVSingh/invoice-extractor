from pathlib import Path

import pytest

from invoice_extractor.extract import extract_invoice, parse_amount

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


@pytest.mark.parametrize("raw,expected", [
    ("1.234,56", 1234.56), ("1,234.56", 1234.56), ("1 140,00", 1140.0),
    ("869,20", 869.2), ("49.20", 49.2),
])
def test_parse_amount(raw, expected):
    assert parse_amount(raw) == expected


@pytest.mark.parametrize("file,number,date,due,vat,total", [
    ("factuur_bakkerij_zonneveld.pdf", "BZ-2026-0142", "14/09/2026", "14/10/2026", 49.20, 869.20),
    ("invoice_northwind_studio.pdf", "NW-00087", "2026-09-02", "2026-09-30", 262.50, 1512.50),
    ("factuur_drukkerij_vanneste.pdf", "2026/553", "01.10.2026", "31.10.2026", 239.40, 1379.40),
])
def test_samples(file, number, date, due, vat, total):
    inv = extract_invoice(SAMPLES / file)
    assert inv.invoice_number == number
    assert inv.invoice_date == date
    assert inv.due_date == due
    assert inv.vat == vat
    assert inv.total == total
    assert inv.currency == "EUR"
