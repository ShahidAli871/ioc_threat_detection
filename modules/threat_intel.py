import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from config import settings

CACHE_FILE = Path(settings.CACHE_DIR) / "ti_cache.json"


class ThreatIntel:
    def __init__(self):
        self._lock = asyncio.Lock()
        self._cache: Dict[str, Any] = {}
        self._rate_lock = asyncio.Lock()
        self._last_call = 0.0
        self._load_cache()

    def _load_cache(self):
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            if CACHE_FILE.exists():
                with open(CACHE_FILE, "r") as f:
                    self._cache = json.load(f)
        except Exception:
            self._cache = {}

    def _save_cache(self):
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(self._cache, f)
        except Exception:
            pass

    async def _rate_limit(self):
        async with self._rate_lock:
            now = asyncio.get_event_loop().time()
            delta = now - self._last_call
            if delta < settings.RATE_LIMIT_SECONDS:
                await asyncio.sleep(settings.RATE_LIMIT_SECONDS - delta)
            self._last_call = asyncio.get_event_loop().time()

    async def check(self, key: str, kind: str) -> Dict[str, Any]:
        """Check an IOC (url/ip/hash). This is a stubbed implementation that uses cache.
        Replace with real API calls to VirusTotal/AbuseIPDB/URLhaus as needed."""
        if not key:
            return {"ioc": key, "kind": kind, "malicious": False, "score": 0, "source": "none"}

        # cache hit
        if key in self._cache:
            return self._cache[key]

        # simulate rate-limit and an external call
        await self._rate_limit()

        # naive heuristic: suspicious if contains "bad" or endswith .exe
        mal = False
        score = 0
        if "bad" in key.lower() or key.lower().endswith(".exe"):
            mal = True
            score = 80

        res = {"ioc": key, "kind": kind, "malicious": mal, "score": score, "source": "stub"}
        self._cache[key] = res
        self._save_cache()
        return res

    async def bulk_check(self, iocs: Dict[str, list]):
        tasks = []
        for kind, items in iocs.items():
            for it in items:
                tasks.append(self.check(it, kind))
        results = await asyncio.gather(*tasks)
        return results
