import json
from pathlib import Path
from typing import Any, Dict

from config import settings


def write_report(report: Dict[str, Any], filename: str = None) -> Path:
    out_dir = Path(settings.OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    if not filename:
        filename = "report.json"
    path = out_dir / filename
    with open(path, "w") as f:
        json.dump(report, f, indent=2)
    return path
