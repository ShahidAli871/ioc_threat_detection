from typing import Dict, Any, List


def calculate_risk(parsed_email: Dict[str, Any], ti_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    score = 0
    factors: List[str] = []

    # simple heuristics: subject/body
    subj = (parsed_email.get("metadata", {}).get("subject") or "").lower()
    body_text = (parsed_email.get("body", {}).get("text") or "")

    if any(w in subj for w in ["urgent", "action required", "verify"]):
        score += 15
        factors.append("suspicious_subject")

    if "login" in body_text.lower() and "password" in body_text.lower():
        score += 15
        factors.append("credential_phish")

    # attachments
    attachments = parsed_email.get("attachments", [])
    if attachments:
        score += min(20, 10 * len(attachments))
        factors.append("suspicious_attachments")

    # threat intel results
    malicious_count = sum(1 for r in ti_results if r.get("malicious"))
    score += min(40, malicious_count * 15)
    if malicious_count:
        factors.append(f"malicious_iocs={malicious_count}")

    # clamp
    score = max(0, min(100, score))

    classification = "LOW"
    if score >= 80:
        classification = "HIGH"
    elif score >= 50:
        classification = "MEDIUM"

    return {"score": score, "classification": classification, "factors": factors}
