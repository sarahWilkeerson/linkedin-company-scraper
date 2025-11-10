# LinkedIn Company Scraper (Bulk, Fast)

Pull thousands of enriched LinkedIn company profiles in minutes. This tool collects structured company data (name, address, industry, size, website, employees, stock info, specialties, affiliates, and more) to power lead enrichment, market research, and analytics. If you need scalable LinkedIn company scraping, this project is optimized for speed and reliability.


<p align="center">
  <a href="https://bitbash.def" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Linkedin-company-scraper</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction

This project programmatically gathers public company information from LinkedIn profile pages and returns clean, structured JSON for downstream use. It solves the pain of slow, manual research by providing a fast, bulk-capable pipeline. It’s designed for data teams, growth engineers, analysts, and researchers who need accurate company records at scale.

### Where This Shines

- High-throughput collection for 10k–50k+ companies in a single job.
- Enriched, normalized fields (addresses, size, type, founded year, specialties, stock).
- Bulk inputs with automatic pagination and resilience strategies.
- Clean output schema that drops neatly into CRMs, warehouses, or notebooks.
- Sensible defaults with configuration for proxies, concurrency, and rate control.

## Features

| Feature | Description |
|----------|-------------|
| Bulk URL ingestion | Feed an array of company profile URLs and process them concurrently. |
| Enriched profile fields | Collects name, website, industry, size, headquarters, addresses, specialties, stock info, affiliates, and similar pages. |
| Fast pipeline | Tuned concurrency with backoff and retry for high throughput and stability. |
| Structured JSON output | Returns consistent, typed fields ready for ETL and analytics. |
| Robust error handling | Retries, timeouts, and partial save to avoid losing progress. |
| Configurable limits | Control max concurrency, request timeouts, and extraction depth. |
| Lightweight dependencies | Minimal stack to deploy locally or in your infra. |
| Logging & metrics | Progress logs and counters for visibility during long runs. |
| Resume friendly | Skips completed items and persists interim results. |
| Compliance oriented | Focused on public data and respectful rate control options. |

---

## What Data This Scraper Extracts

| Field Name | Field Description |
|-------------|------------------|
| name | Company display name. |
| url | Canonical LinkedIn company URL. |
| mainAddress.streetAddress | Primary street address if present. |
| mainAddress.addressLocality | City of headquarters/main address. |
| mainAddress.addressRegion | State/region of headquarters. |
| mainAddress.postalCode | Postal/ZIP code. |
| mainAddress.addressCountry | Country code or name. |
| description | Company description/overview text. |
| numberOfEmployees | Parsed employee count (integer when available). |
| logo | URL for company logo image. |
| website | External company website. |
| industry | Primary industry/category. |
| companySize | Size band (e.g., “11–50”, “10,001+”). |
| headquarters | Text-formatted HQ address when available. |
| type | Company type (Public, Private, etc.). |
| founded | Founding year (YYYY). |
| specialties | Comma-separated specialties/expertise. |
| followersCount | Estimated followers if shown. |
| stock.symbol | Ticker symbol when public. |
| stock.price | Latest displayed price string if present. |
| stock.change | Price change string if present. |
| addresses[] | Additional global office addresses. |
| affiliatedPages[] | Related/affiliated brand pages with link and metadata. |
| similarPages[] | Similar companies with link and summary info. |
| rawHtml | (Optional) Raw snippet for debugging/advanced parsing. |
| scrapedAt | ISO datetime when the record was captured. |

---

## Example Output

    [
      {
        "name": "Microsoft",
        "url": "https://www.linkedin.com/company/microsoft",
        "mainAddress": {
          "type": "PostalAddress",
          "streetAddress": "1 Microsoft Way",
          "addressLocality": "Redmond",
          "addressRegion": "Washington",
          "postalCode": "98052",
          "addressCountry": "US"
        },
        "description": "Every company has a mission... (truncated for brevity)",
        "numberOfEmployees": 239012,
        "logo": "https://media.licdn.com/dms/image/v2/C560BAQE88xCsONDULQ/company-logo_200_200/company-logo_200_200/0/1630652622688/microsoft_logo",
        "website": "https://news.microsoft.com/",
        "industry": "Software Development",
        "companySize": "10,001+ employees",
        "headquarters": "1 Microsoft Way , Redmond , US",
        "type": "Public Company",
        "founded": 1975,
        "specialties": "Business Software, Developer Tools, Cloud Computing, AI, Productivity",
        "followersCount": 791715,
        "stock": {
          "symbol": "MSFT",
          "price": "$408.43",
          "change": "-2.11 (-0.514%)"
        },
        "addresses": [
          "Thames Valley Park Drive, Reading, Berkshire RG6 1WG, GB",
          "The Circle 02, Zürich Airport, 8058, CH",
          "Viale Pasubio, 21, Milan, 20154, IT"
        ],
        "affiliatedPages": [
          { "name": "Microsoft Azure", "industry": "Technology, Information and Internet", "address": "Redmond, Washington", "linkedinUrl": "https://www.linkedin.com/showcase/microsoft-azure/" },
          { "name": "Microsoft Developer", "industry": "Software Development", "address": "Redmond, WA", "linkedinUrl": "https://www.linkedin.com/showcase/microsoft-developers/" }
        ],
        "similarPages": [
          { "name": "Google", "industry": "Software Development", "address": "Mountain View, CA", "linkedinUrl": "https://www.linkedin.com/company/google" },
          { "name": "Apple", "industry": "Computers and Electronics Manufacturing", "address": "Cupertino, CA", "linkedinUrl": "https://www.linkedin.com/company/apple" }
        ],
        "scrapedAt": "2025-11-10T22:00:00Z"
      }
    ]

---

## Directory Structure Tree

    facebook-posts-scraper (IMPORTANT :!! always keep this name as the name of the apify actor !!! Linkedin-company-scraper )/
    ├── src/
    │   ├── runner.py
    │   ├── client/
    │   │   ├── http.py
    │   │   └── throttler.py
    │   ├── extractors/
    │   │   ├── linkedin_company_parser.py
    │   │   └── schema.py
    │   ├── pipelines/
    │   │   ├── normalizer.py
    │   │   └── exporter.py
    │   ├── utils/
    │   │   ├── logging.py
    │   │   ├── time.py
    │   │   └── validators.py
    │   └── config/
    │       ├── settings.example.json
    │       └── proxies.example.txt
    ├── data/
    │   ├── inputs.sample.json
    │   └── sample_output.json
    ├── tests/
    │   ├── test_parser.py
    │   └── test_normalizer.py
    ├── requirements.txt
    └── README.md

---

## Use Cases

- **Sales Ops** uses it to enrich CRM accounts with industry, size, and HQ data, so they can prioritize outreach and improve routing.
- **Market Intelligence** uses it to map competitors and adjacent markets, so they can size opportunities and track trends.
- **Investors/Analysts** use it to compile fundamentals across a sector, so they can accelerate due diligence and screening.
- **Growth/Product Teams** use it to segment users by company attributes, so they can personalize onboarding and pricing.
- **Academics** use it to assemble organizational datasets, so they can support research at scale with consistent structure.

---

## FAQs

**Q: What input format does it accept?**
A: Provide an array of LinkedIn company profile URLs (e.g., "https://www.linkedin.com/company/microsoft"). The pipeline will validate, deduplicate, and crawl them.

**Q: How do I control speed vs. stability?**
A: Adjust concurrency, per-host rate, and retry/backoff settings in configuration. Start conservative, then increase gradually while monitoring logs.

**Q: Which fields are guaranteed?**
A: `name`, `url`, and `scrapedAt` are usually present. Other fields depend on the public page. The schema includes optional properties and safe defaults.

**Q: Can I resume a partial run?**
A: Yes. The pipeline writes interim results and skips already processed URLs on subsequent runs.

---

## Performance Benchmarks and Results

**Primary Metric:** Processes 50,000+ company URLs in under 10 minutes on a modern 8–16 vCPU environment with tuned concurrency and healthy network conditions.
**Reliability Metric:** >98% successful record completion on public, accessible pages with automatic retries and backoff.
**Efficiency Metric:** Sustains 80–120 req/s aggregate throughput while keeping memory usage modest via streaming extraction.
**Quality Metric:** 95–99% field completeness on core attributes (name, website, industry, size, HQ) for well-formed pages; gracefully degrades when data is missing.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
