from typing import Dict, Any
import re

def _clean_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def normalize_company_record(record: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(record)  # shallow copy
    # Normalize strings
    for key in ("name", "description", "website", "industry", "companySize", "headquarters", "type", "specialties", "logo"):
        if out.get(key) and isinstance(out[key], str):
            out[key] = _clean_whitespace(out[key])

    # Normalize website
    if out.get("website"):
        site = out["website"].strip()
        if site.startswith("//"):
            site = "https:" + site
        if not re.match(r"^https?://", site):
            site = "https://" + site
        out["website"] = site

    # Clamp employee count
    if out.get("numberOfEmployees") is not None:
        try:
            out["numberOfEmployees"] = int(out["numberOfEmployees"])
        except Exception:
            out["numberOfEmployees"] = None

    # Normalize address object shape
    if "mainAddress" in out and isinstance(out["mainAddress"], dict):
        addr = out["mainAddress"]
        addr.setdefault("type", "PostalAddress")
        for k in ("streetAddress", "addressLocality", "addressRegion", "postalCode", "addressCountry"):
            if addr.get(k) == "":
                addr[k] = None

    # Stock sub-object
    if "stock" in out and isinstance(out["stock"], dict):
        out["stock"].setdefault("symbol", None)
        out["stock"].setdefault("price", None)
        out["stock"].setdefault("change", None)
    else:
        out["stock"] = {"symbol": None, "price": None, "change": None}

    # Arrays
    for a in ("addresses", "affiliatedPages", "similarPages"):
        if a not in out or not isinstance(out[a], list):
            out[a] = []

    # Followers count integer
    if out.get("followersCount") is not None:
        try:
            out["followersCount"] = int(out["followersCount"])
        except Exception:
            out["followersCount"] = None

    return out