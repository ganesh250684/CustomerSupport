import re


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"\b(?:\+?\d{1,3}[ -]?)?(?:\(?\d{3}\)?[ -]?)\d{3}[ -]?\d{4}\b")
ACCOUNT_RE = re.compile(r"\b(?:acct|account|customer)[-_ ]?id[: ]?[A-Za-z0-9-]{4,}\b", re.IGNORECASE)


def redact_pii(text: str) -> str:
    """Redact common PII patterns before writing logs."""
    redacted = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    redacted = PHONE_RE.sub("[REDACTED_PHONE]", redacted)
    redacted = ACCOUNT_RE.sub("[REDACTED_ACCOUNT_ID]", redacted)
    return redacted
