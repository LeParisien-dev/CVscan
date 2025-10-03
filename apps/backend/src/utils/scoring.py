def score_text(text: str) -> int:
    """Simple scoring function for CV text."""
    if not text:
        return 0

    score = 0

    # Length-based score
    score += min(len(text) // 100, 50)  # max 50 points

    # Keyword-based score
    keywords = ["python", "fastapi", "ai", "machine learning", "docker"]
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 10

    return min(score, 100)  # max score = 100
