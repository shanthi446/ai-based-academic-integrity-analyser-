
import re


def analyze_evidence_depth(evidence_text):

    if not evidence_text or not evidence_text.strip():
        return {
            "score": 0,
            "evidence_count": 0,
            "details": ["No supporting evidence provided"],
            "status": "Insufficient Evidence"
        }

    score = 0
    details = []

    # 1. Evidence length
    if len(evidence_text) >= 300:
        score += 20
        details.append("Detailed evidence provided")
    elif len(evidence_text) >= 100:
        score += 10
        details.append("Moderate evidence details")
    else:
        details.append("Evidence details are limited")

    # 2. Evidence count
    evidence_items = [
        line for line in evidence_text.splitlines()
        if line.strip()
    ]

    evidence_count = len(evidence_items)

    if evidence_count >= 3:
        score += 20
        details.append("Multiple evidence entries found")
    elif evidence_count >= 1:
        score += 10
        details.append("Evidence entry found")

    # 3. URL or DOI
    if re.search(r'https?://|doi\.org/', evidence_text, re.I):
        score += 20
        details.append("URL or DOI reference found")

    # 4. Citation year
    if re.search(r'\b(19|20)\d{2}\b', evidence_text):
        score += 20
        details.append("Publication year found")

    # 5. Citation indicators
    if re.search(
        r'\b(references|bibliography|source|author|journal|citation)\b',
        evidence_text,
        re.I
    ):
        score += 20
        details.append("Citation information found")

    return {
        "score": min(score, 100),
        "evidence_count": evidence_count,
        "details": details,
        "status": "Evidence Analysis Completed"
    }
