import email
import hashlib
from email import policy
from email.parser import BytesParser
from pathlib import Path
from typing import Dict, Any, List


class EmailParser:
    """Simple .eml parser to extract headers, body and attachments."""

    def parse_eml(self, file_path: str) -> Dict[str, Any]:
        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(file_path)

        with open(p, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        result: Dict[str, Any] = {
            "headers": dict(msg.items()),
            "metadata": {
                "from": msg.get("From"),
                "to": msg.get("To"),
                "subject": msg.get("Subject"),
                "date": msg.get("Date"),
            },
            "body": {"text": "", "html": ""},
            "attachments": [],
        }

        # extract body
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                disp = part.get_content_disposition()
                if disp == "attachment":
                    payload = part.get_payload(decode=True) or b""
                    name = part.get_filename()
                    sha256 = hashlib.sha256(payload).hexdigest()
                    result["attachments"].append({
                        "filename": name,
                        "content_type": ctype,
                        "size": len(payload),
                        "sha256": sha256,
                    })
                else:
                    if ctype == "text/plain":
                        result["body"]["text"] += part.get_content() or ""
                    elif ctype == "text/html":
                        result["body"]["html"] += part.get_content() or ""
        else:
            ctype = msg.get_content_type()
            if ctype == "text/plain":
                result["body"]["text"] = msg.get_content() or ""
            elif ctype == "text/html":
                result["body"]["html"] = msg.get_content() or ""

        return result
