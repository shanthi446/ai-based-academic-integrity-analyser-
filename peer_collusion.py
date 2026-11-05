
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def detect_peer_collusion(student1, text1, student2, text2):

    if not text1.strip() or not text2.strip():
        return {
            "error": "Both assignments are required"
        }

    documents = [text1, text2]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        percentage = round(similarity * 100, 2)

        if percentage >= 75:
            status = "High Similarity"
        elif percentage >= 40:
            status = "Moderate Similarity"
        else:
            status = "Low Similarity"

        return {
            "student1": student1,
            "student2": student2,
            "similarity": percentage,
            "status": status,
            "method": "TF-IDF + Cosine Similarity"
        }

    except ValueError:
        return {
            "error": "Not enough meaningful text to compare"
        }
