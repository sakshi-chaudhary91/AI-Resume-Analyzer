ROLE_SKILLS = {

    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "llm",
        "langchain",
        "git"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "statistics"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git"
    ]
}
def find_role_missing_skills(role, detected_skills):

    required = ROLE_SKILLS.get(role, [])

    missing = []

    for skill in required:

        if skill.lower() not in [
            s.lower() for s in detected_skills
        ]:
            missing.append(skill)

    return missing