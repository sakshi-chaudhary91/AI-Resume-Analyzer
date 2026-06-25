def find_missing_skills(detected_skills):

    required_skills = [
        "python",
        "sql",
        "git",
        "github",
        "html",
        "css",
        "javascript",
        "machine learning"
    ]

    missing_skills = []

    for skill in required_skills:

        if skill not in detected_skills:
            missing_skills.append(skill)

    return missing_skills