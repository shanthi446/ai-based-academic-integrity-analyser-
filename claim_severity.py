
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def analyze_claim_severity(original_claim, submitted_claim):

    if not original_claim.strip() or not submitted_claim.strip():
        return {
            "error": "Both claims are required"
        }

    try:

        documents = [
            original_claim,
            submitted_claim
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        similarity_score = round(similarity * 100, 2)

        transformation = round(
            100 - similarity_score, 2
        )

        if transformation <= 25:
            severity = "Low"

        elif transformation <= 60:
            severity = "Moderate"

        else:
            severity = "High"

        return {
            "similarity": similarity_score,
            "transformation": transformation,
            "severity": severity,
            "status": "Analysis Completed"
        }

    except ValueError:

        return {
            "error": "Unable to compare claims"
        }
