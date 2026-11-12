
import re

SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "c", "c++"
    ],
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "oracle"
    ],
    "Web Technologies": [
        "html", "css", "react", "node.js", "express.js"
    ],
    "Frameworks": [
        "django", "flask", "spring boot", "hibernate"
    ],
    "Tools and Technologies": [
        "git", "github", "docker", "aws", "azure"
    ],
    "Core Concepts": [
        "oop", "data structures", "algorithms",
        "rest api", "rest apis", "api", "apis",
        "dbms", "debugging"
    ]
}


def extract_keywords(text):
    text = text.lower()
    keywords = []

    for category, skills in SKILL_CATEGORIES.items():
        for skill in skills:
            pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'

            if re.search(pattern, text):
                keywords.append(skill)

    return sorted(set(keywords))


def compare_keywords(resume_keywords, jd_keywords):
    matched = sorted(set(resume_keywords) & set(jd_keywords))
    missing = sorted(set(jd_keywords) - set(resume_keywords))

    return matched, missing


def extract_weighted_skills(job_desc):

    # Identify required and preferred sections
    required_match = re.search(
        r"required skills\s*:\s*(.*?)(?=preferred skills\s*:|responsibilities\s*:|qualification\s*:|experience\s*:|$)",
        job_desc,
        re.IGNORECASE | re.DOTALL
    )

    preferred_match = re.search(
        r"preferred skills\s*:\s*(.*?)(?=responsibilities\s*:|qualification\s*:|experience\s*:|$)",
        job_desc,
        re.IGNORECASE | re.DOTALL
    )

    # Extract skills from both sections
    required_text = required_match.group(1) if required_match else ""
    preferred_text = preferred_match.group(1) if preferred_match else ""

    required_skills = set(extract_keywords(required_text))
    preferred_skills = set(extract_keywords(preferred_text))

    # A required skill takes priority if it appears in both
    preferred_skills -= required_skills

    # If no recognized sections exist, treat all identified skills as required
    if not required_match and not preferred_match:
        required_skills = set(extract_keywords(job_desc))

    return required_skills, preferred_skills
