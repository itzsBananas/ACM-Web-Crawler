def scholarship_score(html: str) -> float:
    # word frequencies and weights
    keywords = (
        ("scholarship", 2),
        ("women", 0.5),
        ("diverse", 1),
        ("diversity", 1)
    )

    # quick relevance check
    if html.count("scholarship") == 0:
        return 0

    # weighting
    total_score = 0
    for word, weight in keywords:
        total_score += html.count(word) * weight
    return total_score


