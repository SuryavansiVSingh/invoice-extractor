"""Core extraction logic: PDF -> text -> fields."""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path

import pdfplumber

# Labels in English and Dutch (Belgium / Netherlands)
LABELS = {
    "invoice_number": [r"invoice\s*(?:no\.?|number|#)", r"factuur\s*(?:nr\.?|nummer)"],
    "invoice_date": [r"invoice\s*date", r"date", r"factuurdatum", r"datum"],
    "due_date": [r"due\s*date", r"payment\s*due", r"vervaldatum", r"te\s*betalen\s*voor"],
    "vat": [r"vat(?:\s*\d+\s*%)?", r"btw(?:\s*\d+\s*%)?"],
    "total": [r"total\s*(?:due|amount)?", r"amount\s*due", r"totaal(?:\s*te\s*betalen)?", r"te\s*betalen"],
}

DATE_RE = r"(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})"
AMOUNT_RE = r"(?:€|EUR|\$|USD)?\s*(-?\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d{2}))"


@dataclass
class Invoice:
    file: str
    supplier: str | None = None
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None
    vat: float | None = None
    total: float | None = None
    currency: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def parse_amount(raw: str) -> float:
    """Turn '1.234,56', '1,234.56' or '1 234,56' into 1234.56."""
    s = raw.replace(" ", "").replace(" ", "")
    if "," in s and "." in s:
        # whichever separator comes last is the decimal separator
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    return round(float(s), 2)


def _find_after(label_patterns: list[str], value_re: str, text: str) -> str | None:
    for label in label_patterns:
        m = re.search(rf"(?im)^.*?\b{label}(?![A-Za-z])\s*[:#]?\s*{value_re}", text)
        if m:
            return m.group(1).strip()
    return None


def extract_text(pdf_path: Path) -> str:
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def parse_text(text: str, file: str = "") -> Invoice:
    inv = Invoice(file=file)
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    inv.supplier = lines[0] if lines else None

    inv.invoice_number = _find_after(LABELS["invoice_number"], r"([A-Z0-9][A-Z0-9\-/]{2,})", text)
    inv.due_date = _find_after(LABELS["due_date"], DATE_RE, text)
    # invoice date: try specific labels first so "due date" isn't picked up
    inv.invoice_date = _find_after(LABELS["invoice_date"][:1] + LABELS["invoice_date"][2:3], DATE_RE, text) \
        or _find_after(LABELS["invoice_date"], DATE_RE, text)

    vat = _find_after(LABELS["vat"], AMOUNT_RE, text)
    inv.vat = parse_amount(vat) if vat else None

    # total: take the LAST matching total line (subtotals come first)
    totals = []
    for label in LABELS["total"]:
        totals += re.findall(rf"(?im)^(?!.*sub).*?\b{label}(?![A-Za-z])\s*:?\s*{AMOUNT_RE}", text)
    if totals:
        inv.total = parse_amount(totals[-1])

    if re.search(r"€|EUR", text):
        inv.currency = "EUR"
    elif re.search(r"\$|USD", text):
        inv.currency = "USD"
    return inv


def extract_invoice(pdf_path: str | Path) -> Invoice:
    pdf_path = Path(pdf_path)
    return parse_text(extract_text(pdf_path), file=pdf_path.name)
