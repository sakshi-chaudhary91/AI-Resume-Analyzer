import re
def extract_skills(text):

    skills_db = [
        "python",
        "sql",
        "machine learning",
        "deep learning",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "react",
    ]

    detected = []
    text = text.lower()
    words = re.findall(r'\b\w+\b',text)

    for skill in skills_db:
        if " " in skill:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                detected.append(skill)
        else:
            if skill in words:
                detected.append(skill)
    return detected