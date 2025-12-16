import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

# API keys (read from env)
VIRUSTOTAL_API_KEY = os.getenv("VIRUSTOTAL_API_KEY")
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY")
URLHAUS_API_KEY = os.getenv("URLHAUS_API_KEY")

# Cache & rate limiting
CACHE_DIR = os.getenv("CACHE_DIR", BASE_DIR / "data" / "cache")
CACHE_TTL = int(os.getenv("CACHE_TTL", "86400"))  # seconds
RATE_LIMIT_SECONDS = float(os.getenv("RATE_LIMIT_SECONDS", "1"))

# Output
OUTPUT_DIR = os.getenv("OUTPUT_DIR", BASE_DIR / "data" / "output")

# Risk thresholds
RISK_THRESHOLDS = {
    "HIGH": 80,
    "MEDIUM": 50,
}
