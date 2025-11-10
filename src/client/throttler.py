import asyncio
import time

class AdaptiveThrottler:
    """
    Very lightweight adaptive throttler.
    Success reduces delay slightly, failures increase it quickly.
    """
    def __init__(self, max_rate: int = 32, min_delay: float = 0.01, max_delay: float = 2.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.current_delay = min_delay
        self.last_time = 0.0

    async def wait(self):
        now = time.monotonic()
        elapsed = now - self.last_time
        if elapsed < self.current_delay:
            await asyncio.sleep(self.current_delay - elapsed)
        self.last_time = time.monotonic()

    def feedback(self, success: bool):
        if success:
            # decay delay
            self.current_delay = max(self.min_delay, self.current_delay * 0.8)
        else:
            # spike delay
            self.current_delay = min(self.max_delay, self.current_delay * 1.7 + 0.05)