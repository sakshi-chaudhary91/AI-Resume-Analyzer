def calculate_ats_score(text, skills):

    score = 0
    breakdown = {}

    # Skills Score (40 Marks)
    skills_score = min(len(skills) * 5, 40)
    score += skills_score
    breakdown["Skills"] = skills_score

    # Projects Section (20 Marks)
    if "project" in text.lower():
        score += 20
        breakdown["Projects"] = 20
    else:
        breakdown["Projects"] = 0

    # Education Section (10 Marks)
    if "education" in text.lower():
        score += 10
        breakdown["Education"] = 10
    else:
        breakdown["Education"] = 0

    # Contact Information (20 Marks)
    contact_score = 0

    if "@" in text:
        contact_score += 10

    if "linkedin" in text.lower():
        contact_score += 5

    if "github" in text.lower():
        contact_score += 5

    score += contact_score
    breakdown["Contact"] = contact_score

    # Final Score
    breakdown["Total"] = score

    return breakdown