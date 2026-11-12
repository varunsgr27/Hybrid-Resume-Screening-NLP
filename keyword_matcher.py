
import re

SKILL_CATEGORIES = {
    "Programming Languages": [
        "python", "java", "javascript", "c", "c++",
        "c#", "php", "ruby", "perl"
    ],

    "Databases": [
        "sql", "mysql", "postgresql", "mongodb",
        "oracle", "database management", "database management systems"
    ],

    "Web Technologies": [
        "html", "css", "react", "node.js", "express.js"
    ],

    "Frameworks": [
        "django", "flask", "spring boot", "hibernate"
    ],

    "Tools and Technologies": [
        "git", "github", "docker", "aws", "azure",
        "sharepoint", "microsoft office", "microsoft excel",
        "excel", "microsoft project", "visio", "active directory",
        "remedy", "cisco", "citrix", "compTIA"
    ],

    "Networking": [
        "networking", "network operations", "network security",
        "network infrastructure", "computer networks",
        "lan", "wan", "telecommunications",
        "network configuration", "connectivity"
    ],

    "IT Support": [
        "technical support", "troubleshooting",
        "hardware", "software", "operating systems",
        "windows", "linux", "installation", "configuration",
        "system administration", "desktop support",
        "help desk", "it support", "user support",
        "incident management", "ticketing system"
    ],

    "Systems and Analysis": [
        "system analysis", "systems analysis",
        "requirements gathering", "data analysis",
        "project management", "business process improvement",
        "documentation", "quality assurance",
        "process improvement", "systems integration"
    ],

    "Security": [
        "information security", "cybersecurity",
        "security operations", "risk analysis",
        "security management", "access control"
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
            pattern = r'(?<!\w)' + re.escape(skill.lower()) + r'(?!\w)'

            if re.search(pattern, text):
                keywords.append(skill.lower())

    return sorted(set(keywords))


def compare_keywords(resume_keywords, jd_keywords):
    matched = sorted(set(resume_keywords) & set(jd_keywords))
    missing = sorted(set(jd_keywords) - set(resume_keywords))

    return matched, missing


def extract_weighted_skills(job_desc):

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

    required_text = required_match.group(1) if required_match else ""
    preferred_text = preferred_match.group(1) if preferred_match else ""

    required_skills = set(extract_keywords(required_text))
    preferred_skills = set(extract_keywords(preferred_text))

    preferred_skills -= required_skills

    if not required_match and not preferred_match:
        required_skills = set(extract_keywords(job_desc))

    return required_skills, preferred_skills
