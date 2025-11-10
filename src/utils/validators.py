import re
from typing import List

_LINKEDIN_COMPANY_RE = re.compile(r"^https?://(www\.)?linkedin\.com/company/[A-Za-z0-9\-\._%]+/?$", re.I)

def is_valid_linkedin_company_url(url: str) -> bool:
    return bool(_LINKEDIN_COMPANY_RE.match(url or ""))

def dedupe_urls(urls: List[str]) -> List[str]:
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out