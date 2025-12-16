import asyncio
import json
from pathlib import Path
from typing import Dict, Any

from modules.email_parser import EmailParser
from modules.ioc_extractor import extract_iocs
from modules.threat_intel import ThreatIntel
from modules.analyzer import calculate_risk
from modules.reporter import write_report


class PhishingPipeline:
    def __init__(self):
        self.parser = EmailParser()
        self.ti = ThreatIntel()

    async def analyze(self, eml_path: str) -> Dict[str, Any]:
        parsed = self.parser.parse_eml(eml_path)
        text_blob = parsed.get("body", {}).get("text", "") + "\n" + parsed.get("body", {}).get("html", "")

        # include headers and subject in IOC extraction
        headers_blob = "\n".join([f"{k}: {v}" for k, v in parsed.get("headers", {}).items()])

        iocs = extract_iocs(text_blob + "\n" + headers_blob)

        ti_results = await self.ti.bulk_check(iocs)

        risk = calculate_risk(parsed, ti_results)

        report = {
            "input": eml_path,
            "parsed": parsed,
            "iocs": iocs,
            "threat_intel": ti_results,
            "risk": risk,
        }

        out_path = write_report(report, filename=Path(eml_path).stem + "_report.json")
        report["output_path"] = str(out_path)
        return report


def run_sync(eml_path: str) -> Dict[str, Any]:
    loop = asyncio.get_event_loop()
    pipeline = PhishingPipeline()
    return loop.run_until_complete(pipeline.analyze(eml_path))
