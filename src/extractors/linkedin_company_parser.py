from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import json
import re
from .schema import CompanyRecord
from utils.time import now_iso_utc

def _text(el) -> Optional[str]:
    if not el:
        return None
    t = el.get_text(" ", strip=True)
    return t or None

def _json_ld_blocks(soup: BeautifulSoup) -> List[dict]:
    blocks = []
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "{}")
            if isinstance(data, dict):
                blocks.append(data)
            elif isinstance(data, list):
                blocks.extend([d for d in data if isinstance(d, dict)])
        except Exception:
            continue
    return blocks

def _first_addr(obj: dict) -> Optional[dict]:
    addr = obj.get("address")
    if isinstance(addr, dict):
        return addr
    if isinstance(addr, list) and addr:
        return addr[0]
    return None

class LinkedInCompanyParser:
    """
    Heuristic parser for public LinkedIn company pages.
    Prefers JSON-LD, falls back to DOM text scraping with conservative selectors.
    """

    def parse(self, html: str, base_url: str, include_raw: bool = False) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")

        data: Dict[str, Any] = {
            "name": None,
            "url": base_url,
            "mainAddress": {
                "type": "PostalAddress",
                "streetAddress": None,
                "addressLocality": None,
                "addressRegion": None,
                "postalCode": None,
                "addressCountry": None,
            },
            "description": None,
            "numberOfEmployees": None,
            "logo": None,
            "website": None,
            "industry": None,
            "companySize": None,
            "headquarters": None,
            "type": None,
            "founded": None,
            "specialties": None,
            "followersCount": None,
            "stock": {
                "symbol": None,
                "price": None,
                "change": None,
            },
            "addresses": [],
            "affiliatedPages": [],
            "similarPages": [],
            "scrapedAt": now_iso_utc(),
        }

        # Prefer JSON-LD if available
        for block in _json_ld_blocks(soup):
            # Organization or LocalBusiness patterns
            if block.get("@type") in {"Organization", "Corporation", "LocalBusiness"} or "name" in block:
                data["name"] = data["name"] or block.get("name")
                data["logo"] = data["logo"] or (block.get("logo", {}) if isinstance(block.get("logo"), dict) else block.get("logo"))
                data["website"] = data["website"] or block.get("url") or block.get("sameAs")
                addr = _first_addr(block)
                if addr:
                    data["mainAddress"]["streetAddress"] = data["mainAddress"]["streetAddress"] or addr.get("streetAddress")
                    data["mainAddress"]["addressLocality"] = data["mainAddress"]["addressLocality"] or addr.get("addressLocality")
                    data["mainAddress"]["addressRegion"] = data["mainAddress"]["addressRegion"] or addr.get("addressRegion")
                    data["mainAddress"]["postalCode"] = data["mainAddress"]["postalCode"] or addr.get("postalCode")
                    data["mainAddress"]["addressCountry"] = data["mainAddress"]["addressCountry"] or (
                        addr.get("addressCountry", {}).get("name") if isinstance(addr.get("addressCountry"), dict)
                        else addr.get("addressCountry")
                    )
                if not data["description"]:
                    descr = block.get("description")
                    if isinstance(descr, str):
                        data["description"] = descr

        # Fallback: meta tags / simple selectors
        if not data["name"]:
            og_title = soup.find("meta", property="og:title") or soup.find("meta", attrs={"name": "title"})
            if og_title and og_title.get("content"):
                data["name"] = og_title["content"].split(" | ")[0].strip()

        if not data["description"]:
            og_desc = soup.find("meta", property="og:description") or soup.find("meta", attrs={"name": "description"})
            if og_desc and og_desc.get("content"):
                data["description"] = og_desc["content"].strip()

        # Heuristics for fields commonly present in LinkedIn DOM fragments (public)
        text = soup.get_text(" ", strip=True)

        # Followers (pattern like "791,715 followers")
        m = re.search(r"([\d,\.]+)\s+followers", text, re.I)
        if m:
            try:
                data["followersCount"] = int(m.group(1).replace(",", "").replace(".", ""))
            except ValueError:
                pass

        # Company size patterns e.g. "10,001+ employees"
        m = re.search(r"(\d[\d,\.]*\+?\s*employees)", text, re.I)
        if m and not data["companySize"]:
            data["companySize"] = m.group(1)

        # Founded year
        m = re.search(r"Founded\s+(\d{4})", text, re.I)
        if m:
            data["founded"] = int(m.group(1))

        # Industry hint
        m = re.search(r"Industry\s*[:|-]\s*([A-Za-z &/,\-]+)", text)
        if m and not data["industry"]:
            data["industry"] = m.group(1).strip()

        # Website hint
        if not data["website"]:
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if re.match(r"^https?://(www\.)?(?!linkedin\.com)[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}(/.*)?$", href):
                    data["website"] = href
                    break

        if include_raw:
            # store a small snippet to avoid massive payloads
            head = soup.find("head")
            snippet = str(head) if head else html[:2000]
            data["rawHtml"] = snippet

        # Final tidy up to comply with schema types
        # numberOfEmployees from "1,234 employees" if available in text
        if not data["numberOfEmployees"]:
            m = re.search(r"([\d,\.]+)\s+employees", text, re.I)
            if m:
                try:
                    data["numberOfEmployees"] = int(m.group(1).replace(",", "").replace(".", ""))
                except ValueError:
                    pass

        return data