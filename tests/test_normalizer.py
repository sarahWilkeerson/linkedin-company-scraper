import os
import sys

ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from pipelines.normalizer import normalize_company_record  # noqa

def test_normalize_types_and_urls():
    rec = {
        "name": "  Foo Inc  ",
        "website": "foo.com",
        "followersCount": "1234",
        "numberOfEmployees": "200",
        "mainAddress": {
            "streetAddress": "",
            "addressLocality": " City  ",
            "addressRegion": "  ST ",
            "postalCode": "",
            "addressCountry": "US"
        },
        "stock": {}
    }
    out = normalize_company_record(rec)
    assert out["name"] == "Foo Inc"
    assert out["website"].startswith("https://")
    assert out["followersCount"] == 1234
    assert out["numberOfEmployees"] == 200
    assert out["mainAddress"]["streetAddress"] is None
    assert out["mainAddress"]["addressLocality"] == "City"
    assert out["stock"]["symbol"] is None