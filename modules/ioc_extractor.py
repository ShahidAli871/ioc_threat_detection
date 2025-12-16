import re
from typing import Dict, List

# basic patterns
PATTERNS = {
    "urls": r"https?://[\w\-\.\/%\?=&#]+",
    "emails": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
    "sha256": r"\b[a-fA-F0-9]{64}\b",
    "sha1": r"\b[a-fA-F0-9]{40}\b",
    "md5": r"\b[a-fA-F0-9]{32}\b",
    "domains": r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b",
}


def extract_iocs(text: str) -> Dict[str, List[str]]:
    text = text or ""
    out: Dict[str, List[str]] = {}
    for name, pat in PATTERNS.items():
        found = re.findall(pat, text, flags=re.IGNORECASE)
        # basic cleanup/dedupe
        uniq = list(dict.fromkeys(found))
        out[name] = uniq
    return out
