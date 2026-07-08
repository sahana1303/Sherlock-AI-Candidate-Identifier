from rapidfuzz import fuzz


def calculate_score(row, candidate_name, candidate_email):

    confidence = 0
    reasons = []

    display = str(row["display_name"]).lower()
    email = str(row["email"]).lower()
    transcript = str(row["transcript"]).lower()

    candidate_name = candidate_name.lower()
    candidate_email = candidate_email.lower()

    # ----------------------------
    # Email Match
    # ----------------------------
    if email == candidate_email:
        confidence += 40
        reasons.append("Candidate email matched")

    # ----------------------------
    # Name Similarity
    # ----------------------------
    similarity = fuzz.partial_ratio(candidate_name, display)

    if similarity >= 70:
        confidence += 25
        reasons.append(f"Display name similarity ({similarity}%)")

    # ----------------------------
    # Speaking Time
    # ----------------------------
    if row["speaking_time"] >= 300:
        confidence += 15
        reasons.append("Long speaking duration")

    # ----------------------------
    # Webcam
    # ----------------------------
    if str(row["webcam"]).upper() == "ON":
        confidence += 10
        reasons.append("Webcam enabled")

    # ----------------------------
    # Transcript Keywords
    # ----------------------------
    keywords = [
        "ai",
        "machine learning",
        "deep learning",
        "python",
        "data",
        "data science",
        "artificial intelligence",
        "neural network",
        "model"
    ]

    keyword_count = 0

    for word in keywords:
        if word in transcript:
            keyword_count += 1

    confidence += min(keyword_count * 2, 10)

    if keyword_count > 0:
        reasons.append(f"{keyword_count} AI keywords detected")

    confidence = min(confidence, 100)

    return confidence, reasons