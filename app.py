
from flask import Flask, render_template, request, jsonify

from modules.peer_collusion import detect_peer_collusion
from modules.claim_severity import analyze_claim_severity
from modules.risk_propagation import calculate_integrity_risk
from modules.metadata_forensics import analyze_metadata
from modules.evidence_score import analyze_evidence_depth
from modules.llm_integration import generate_integrity_report


app = Flask(__name__)
app.secret_key = "academic_integrity_project"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # STUDENT DETAILS

    student_id = request.form.get("student_id", "")
    student_name = request.form.get("student_name", "")
    title = request.form.get("title", "")
    original_claim = request.form.get("original_claim", "")
    submitted_claim = request.form.get("submitted_claim", "")
    assignment = request.form.get("assignment", "")

    # EVIDENCE DETAILS

    evidence_text = request.form.get("evidence_text", "")

    # PEER DETAILS

    peer_student_id = request.form.get("peer_student_id", "")
    peer_assignment = request.form.get("peer_assignment", "")

    # DOCUMENT METADATA FORENSICS

    document = request.files.get("document")

    filename = (
        document.filename
        if document and document.filename
        else "No document uploaded"
    )

    metadata = {
        "filename": filename,
        "file_type": "Not Available",
        "author": "Not Available",
        "created": "Not Available",
        "modified": "Not Available",
        "creator": "Not Available",
        "status": "No document uploaded"
    }

    if document and document.filename:
        metadata = analyze_metadata(document)

    # CLAIM TRANSFORMATION SEVERITY

    claim_result = analyze_claim_severity(
        original_claim,
        submitted_claim
    )

    # EVIDENCE DEPTH SCORE

    evidence_result = analyze_evidence_depth(
        evidence_text
    )

    # PEER COLLUSION DETECTION

    peer_result = None

    if peer_student_id.strip() and peer_assignment.strip():

        peer_result = detect_peer_collusion(
            student_id,
            assignment,
            peer_student_id,
            peer_assignment
        )

    # INTEGRITY RISK CALCULATION

    risk_result = calculate_integrity_risk(
        claim_transformation=claim_result.get(
            "transformation", 0
        ),
        peer_similarity=(
            peer_result.get("similarity")
            if peer_result and "similarity" in peer_result
            else None
        ),
        evidence_depth=evidence_result.get("score", 0)
    )

    # LLM REPORT GENERATION

    llm_report = generate_integrity_report(
        claim_result=claim_result,
        evidence_result=evidence_result,
        metadata=metadata,
        risk_result=risk_result
    )

    # DISPLAY FINAL RESULT

    return render_template(
        "result.html",
        student_id=student_id,
        student_name=student_name,
        title=title,
        original_claim=original_claim,
        submitted_claim=submitted_claim,
        assignment=assignment,
        filename=filename,
        metadata=metadata,
        claim_result=claim_result,
        risk_result=risk_result,
        evidence_result=evidence_result,
        peer_result=peer_result,
        llm_report=llm_report
    )


@app.route("/peer-collusion")
def peer_collusion():
    return render_template("peer_collusion.html")


@app.route("/peer-collusion/analyze", methods=["POST"])
def analyze_peer_collusion():

    student1 = request.form.get("student1", "")
    text1 = request.form.get("text1", "")

    student2 = request.form.get("student2", "")
    text2 = request.form.get("text2", "")

    result = detect_peer_collusion(
        student1,
        text1,
        student2,
        text2
    )

    return render_template(
        "collusion_result.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
