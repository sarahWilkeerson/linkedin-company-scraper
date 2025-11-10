import os
import sys
from bs4 import BeautifulSoup

# Make src importable
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from extractors.linkedin_company_parser import LinkedInCompanyParser  # noqa

def test_parse_basic_fields_from_meta():
    html = """
    <html>
      <head>
        <meta property="og:title" content="Contoso | LinkedIn" />
        <meta property="og:description" content="We make widgets for everyone." />
        <script type="application/ld+json">
        {
          "@context": "https://schema.org",
          "@type": "Organization",
          "name": "Contoso",
          "url": "https://www.contoso.example",
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "1 Infinite Lane",
            "addressLocality": "Metropolis",
            "addressRegion": "CA",
            "postalCode": "94000",
            "addressCountry": "US"
          }
        }
        </script>
      </head>
      <body>
        <div>10,001+ employees</div>
        <div>Founded 1999</div>
        <div>124,567 followers</div>
      </body>
    </html>
    """
    parser = LinkedInCompanyParser()
    data = parser.parse(html, base_url="https://www.linkedin.com/company/contoso", include_raw=False)
    assert data["name"] == "Contoso"
    assert data["description"] == "We make widgets for everyone."
    assert data["mainAddress"]["addressLocality"] == "Metropolis"
    assert data["companySize"].startswith("10,001")
    assert data["founded"] == 1999
    assert isinstance(data["followersCount"], int) and data["followersCount"] > 0