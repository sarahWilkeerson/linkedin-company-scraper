import asyncio
import random
from typing import Optional, Dict

import aiohttp

from .throttler import AdaptiveThrottler
from utils.logging import get_logger

log = get_logger(__name__)

class HttpClient:
    def __init__(self,
                 max_concurrency: int = 8,
                 timeout: int = 30,
                 proxy_file: Optional[str] = None,
                 user_agent: Optional[str] = None):
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._timeout = aiohttp.ClientTimeout(total=timeout)
        self._session: Optional[aiohttp.ClientSession] = None
        self._proxies = self._load_proxies(proxy_file) if proxy_file else []
        self._user_agent = user_agent or "Mozilla/5.0"
        self._throttler = AdaptiveThrottler(max_rate=max_concurrency * 4)

    async def __aenter__(self):
        headers = {
            "User-Agent": self._user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        }
        self._session = aiohttp.ClientSession(timeout=self._timeout, headers=headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()

    @staticmethod
    def _load_proxies(path: str):
        proxies = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        proxies.append(line)
        except FileNotFoundError:
            log.warning("Proxy file not found: %s", path)
        return proxies

    def _pick_proxy(self) -> Optional[str]:
        if not self._proxies:
            return None
        return random.choice(self._proxies)

    async def get_text(self, url: str) -> str:
        assert self._session is not None, "HttpClient must be used within an async context manager"
        proxy = self._pick_proxy()
        retry_delays = [0.5, 1.5, 3.0, 5.0]
        for attempt, delay in enumerate([0] + retry_delays, start=1):
            await self._throttler.wait()  # adaptive backoff throttle
            async with self._semaphore:
                try:
                    if delay:
                        await asyncio.sleep(delay)
                    async with self._session.get(url, proxy=proxy) as resp:
                        text = await resp.text(errors="ignore")
                        if resp.status >= 500:
                            # transient server issue; increase throttle pressure
                            self._throttler.feedback(success=False)
                            raise aiohttp.ClientResponseError(
                                resp.request_info, resp.history, status=resp.status, message="Server error"
                            )
                        elif resp.status in (403, 429):
                            self._throttler.feedback(success=False)
                            log.warning("Received %s for %s (attempt %d). Backing off.", resp.status, url, attempt)
                            continue
                        else:
                            self._throttler.feedback(success=True)
                            return text
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    self._throttler.feedback(success=False)
                    log.warning("Request error for %s: %s (attempt %d)", url, e, attempt)
                    continue
        raise RuntimeError(f"Failed to fetch after retries: {url}")