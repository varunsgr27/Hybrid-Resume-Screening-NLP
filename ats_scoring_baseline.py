
import re
import math
from collections import Counter

from keyword_matcher_baseline import (
    extract_keywords,
    extract_weighted_skills
)


def calculate_tfidf_similarity(resume_text, job_desc):
    resume_words = re.findall(r'\b[a-zA-Z]+\b', resume_text.lower())
    jd_words = re.findall(r'\b[a-zA-Z]+\b', job_desc.lower())
    vocabulary = set(resume_words + jd_words)

    def calculate_tf(words):
        total = len(words)
        counts = Counter(words)
        return {
            word: count / total
            for word, count in counts.items()
        } if total else {}

    def calculate_idf(word):
        documents = [resume_words, jd_words]
        count = sum(word in doc for doc in documents)
        return math.log(3 / (1 + count)) + 1

    def calculate_vector(words):
        tf = calculate_tf(words)
        return {
            word: tf[word] * calculate_idf(word)
            for word in tf
        }

    resume_vector = calculate_vector(resume_words)
    jd_vector = calculate_vector(jd_words)

    dot_product = sum(
        resume_vector.get(word, 0) * jd_vector.get(word, 0)
        for word in vocabulary
    )

    magnitude1 = math.sqrt(
        sum(v ** 2 for v in resume_vector.values())
    )
    magnitude2 = math.sqrt(
        sum(v ** 2 for v in jd_vector.values())
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


def calculate_skill_coverage(resume_text, job_desc):
    resume_skills = set(extract_keywords(resume_text))
    required_skills, preferred_skills = extract_weighted_skills(job_desc)

    total_weight = (
        len(required_skills) * 2
    ) + len(preferred_skills)

    if total_weight == 0:
        return 0, [], []

    matched_required = resume_skills & required_skills
    matched_preferred = resume_skills & preferred_skills

    matched = sorted(matched_required | matched_preferred)
    missing = sorted(
        (required_skills | preferred_skills) - resume_skills
    )

    matched_weight = (
        len(matched_required) * 2
    ) + len(matched_preferred)

    skill_score = (matched_weight / total_weight) * 100

    return skill_score, matched, missing


def calculate_ats_score(resume_text, job_desc):
    similarity = calculate_tfidf_similarity(
        resume_text, job_desc
    )

    tfidf_score = similarity * 100

    skill_score, matched, missing = calculate_skill_coverage(
        resume_text, job_desc
    )

    ats_score = (
        0.4 * tfidf_score
    ) + (0.6 * skill_score)

    return round(ats_score), similarity
