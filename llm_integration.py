
def generate_integrity_report(
    claim_result,
    evidence_result,
    metadata,
    risk_result
):

    claim_severity = claim_result.get(
        "severity", "Not Available"
    )

    claim_transformation = claim_result.get(
        "transformation", 0
    )

    evidence_score = evidence_result.get(
        "score", 0
    )

    risk_score = risk_result.get(
        "risk_score", 0
    )

    risk_level = risk_result.get(
        "risk_level", "Unknown"
    )

    report = f"""
AI ACADEMIC INTEGRITY ANALYSIS REPORT

1. CLAIM TRANSFORMATION ANALYSIS

Severity: {claim_severity}
Transformation Score: {claim_transformation}%

2. EVIDENCE DEPTH ANALYSIS

Evidence Score: {evidence_score}%

3. DOCUMENT METADATA ANALYSIS

Author: {metadata.get('author', 'Not Available')}
File Type: {metadata.get('file_type', 'Not Available')}

4. INTEGRITY RISK ANALYSIS

Risk Score: {risk_score}%
Risk Level: {risk_level}

RECOMMENDATIONS:

"""

    if claim_transformation > 60:
        report += "- Review the transformed claim manually.\n"
    else:
        report += "- Claim transformation indicator is relatively low.\n"

    if evidence_score < 40:
        report += "- Add more supporting evidence and references.\n"
    else:
        report += "- Evidence details are reasonably complete.\n"

    if risk_score >= 70:
        report += "- Conduct a detailed human review.\n"
    else:
        report += "- Continue normal academic verification.\n"

    report += """
NOTE:
This automated report is only a preliminary review.
It does not prove academic misconduct.
"""

    return report
