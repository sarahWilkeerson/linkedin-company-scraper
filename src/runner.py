import argparse
import asyncio
import json
import os
import sys
from typing import List, Dict, Any

# Ensure local imports work when running from repo root
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from client.http import HttpClient
from extractors.linkedin_company_parser import LinkedInCompanyParser
from pipelines.normalizer import normalize_company_record
from pipelines.exporter import Exporter
from utils.logging import get_logger
from utils.validators import is_valid_linkedin_company_url, dedupe_urls
from utils.time import now_iso_utc

log = get_logger(__name__)

async def process_url(client: HttpClient, url: str, include_raw: bool) -> Dict[str, Any]:
    parser = LinkedInCompanyParser()
    html = await client.get_text(url)
    parsed = parser.parse(html, base_url=url, include_raw=include_raw)
    normalized = normalize_company_record(parsed)
    normalized["url"] = url if not normalized.get("url") else normalized["url"]
    normalized["scrapedAt"] = normalized.get("scrapedAt") or now_iso_utc()
    return normalized

async def run(urls: List[str], output_path: str, concurrent: int, timeout: int, proxy_file: str = None,
              user_agent: str = None, include_raw: bool = False) -> None:
    urls = [u.strip() for u in urls if u and is_valid_linkedin_company_url(u)]
    urls = dedupe_urls(urls)
    if not urls:
        log.error("No valid LinkedIn company URLs provided.")
        return

    exporter = Exporter(output_path)
    exporter.open()

    async with HttpClient(
        max_concurrency=concurrent,
        timeout=timeout,
        proxy_file=proxy_file,
        user_agent=user_agent,
    ) as client:

        sem = asyncio.Semaphore(concurrent)

        async def worker(u: str):
            async with sem:
                try:
                    record = await process_url(client, u, include_raw)
                    exporter.write(record)
                    log.info("Processed: %s", u)
                except Exception as e:
                    log.exception("Failed to process %s: %s", u, e)
                    exporter.write_error(u, str(e))

        tasks = [asyncio.create_task(worker(u)) for u in urls]
        await asyncio.gather(*tasks)

    exporter.close()
    log.info("Done. Wrote %d records to %s", exporter.records_written, output_path)

def read_input_urls(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "urls" in data and isinstance(data["urls"], list):
        return data["urls"]
    if isinstance(data, list):
        return data
    raise ValueError("Unsupported input file format. Expecting { 'urls': [...] } or a list of URLs.")

def main():
    ap = argparse.ArgumentParser(description="Bulk LinkedIn Company Scraper runner")
    ap.add_argument("--inputs", "-i", default=os.path.join(os.path.dirname(CURRENT_DIR), "data", "inputs.sample.json"),
                    help="Path to a JSON file containing { 'urls': [...] } or a JSON array of URLs.")
    ap.add_argument("--output", "-o", default=os.path.join(os.path.dirname(CURRENT_DIR), "data", "out.json"),
                    help="Path to the output JSON file (pretty-printed). Also writes a .jsonl alongside.")
    ap.add_argument("--concurrency", "-c", type=int, default=8, help="Max concurrent requests.")
    ap.add_argument("--timeout", "-t", type=int, default=30, help="Per-request timeout (seconds).")
    ap.add_argument("--proxies", "-p", default=os.path.join(CURRENT_DIR, "config", "proxies.example.txt"),
                    help="Path to a proxies file (optional).")
    ap.add_argument("--user-agent", "-ua", default="Mozilla/5.0 (compatible; BitbashLinkedInScraper/1.0)",
                    help="Override User-Agent header.")
    ap.add_argument("--include-raw", action="store_true", help="Include rawHtml snippet in the output records.")
    args = ap.parse_args()

    try:
        urls = read_input_urls(args.inputs)
    except Exception as e:
        print(f"Failed to read inputs from {args.inputs}: {e}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(run(
        urls=urls,
        output_path=args.output,
        concurrent=max(1, args.concurrency),
        timeout=max(5, args.timeout),
        proxy_file=args.proxies if os.path.exists(args.proxies) else None,
        user_agent=args.user_agent,
        include_raw=args.include_raw
    ))

if __name__ == "__main__":
    main()