import re

PATTERNS = {
    "IBAN": re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{11,26}\b"),
    "NATIONAL_ID": re.compile(r"\b\d{10}\b"),
    "CARD_PAN": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "PHONE": re.compile(r"\+?\d[\d\s-]{8,}\d"),
    "SECRETS": re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*\S+"),
}

def redact(text: str):
    hits, out = [], text
    for i, (name, rx) in enumerate(PATTERNS.items()):
        if rx.findall(out):
            hits.append(name)
            out = rx.sub("<" + name + "_" + str(i) + ">", out)
    return out, hits
