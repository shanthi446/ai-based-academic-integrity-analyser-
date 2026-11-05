
def calculate_integrity_risk(
    claim_transformation=0,
    peer_similarity=None,
    evidence_depth=None
):

    scores = {}
    weights = {}

    # Claim Transformation Indicator
    if claim_transformation is not None:
        scores["Claim Transformation"] = float(
            claim_transformation
        )
        weights["Claim Transformation"] = 0.40

    # Peer Collusion Indicator
    if peer_similarity is not None:
        scores["Peer Collusion"] = float(
            peer_similarity
        )
        weights["Peer Collusion"] = 0.35

    # Evidence Depth Indicator
    if evidence_depth is not None:
        scores["Evidence Gap"] = 100 - float(
            evidence_depth
        )
        weights["Evidence Gap"] = 0.25

    if not scores:
        return {
            "risk_score": 0,
            "risk_level": "Insufficient Data",
            "status": "No indicators available"
        }

    total_weight = sum(weights.values())

    risk_score = sum(
        scores[key] * weights[key]
        for key in scores
    ) / total_weight

    risk_score = round(risk_score, 2)

    if risk_score >= 70:
        risk_level = "High Risk"

    elif risk_score >= 40:
        risk_level = "Moderate Risk"

    else:
        risk_level = "Low Risk"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "indicators": scores,
        "status": "Preliminary Analysis Completed"
    }
