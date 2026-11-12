
import csv
from pathlib import Path

from ats_scoring import (
    calculate_ats_score,
    calculate_skill_coverage
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent

RESUME_FILE = BASE_DIR / "datasets" / "resumes" / "it_25_resumes.csv"
JD_FOLDER = BASE_DIR / "datasets" / "job_descriptions"
OUTPUT_FOLDER = BASE_DIR / "experiment_results"

OUTPUT_FOLDER.mkdir(exist_ok=True)

# Load 25 IT resumes
with RESUME_FILE.open("r", encoding="utf-8-sig", newline="") as file:
    resumes = list(csv.DictReader(file))

print("Total resumes loaded:", len(resumes))

results = []

# Process each job description
for jd_file in sorted(JD_FOLDER.glob("*.txt")):

    job_title = jd_file.stem.replace("_", " ").title()
    job_description = jd_file.read_text(encoding="utf-8")

    print("\nProcessing:", job_title)

    for resume in resumes:

        resume_text = resume["Resume_str"]

        # Calculate hybrid ATS score and TF-IDF similarity
        ats_score, similarity = calculate_ats_score(
            resume_text,
            job_description
        )

        # Calculate weighted skill coverage
        skill_score, matched, missing = calculate_skill_coverage(
            resume_text,
            job_description
        )

        results.append({
            "Resume_ID": resume["ID"],
            "Category": resume["Category"],
            "Job_Role": job_title,
            "TFIDF_Similarity_Percent": round(similarity * 100, 2),
            "Skill_Coverage_Percent": round(skill_score, 2),
            "Hybrid_ATS_Score": ats_score,
            "Matched_Skills": ", ".join(matched),
            "Missing_Skills": ", ".join(missing)
        })

# Sort results by job role and hybrid score
results.sort(
    key=lambda row: (row["Job_Role"], -row["Hybrid_ATS_Score"])
)

# Save detailed results
results_file = OUTPUT_FOLDER / "hybrid_matching_results.csv"

with results_file.open("w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# Display top 5 matches for each job role
print("\n========== EXPERIMENT RESULTS ==========")

for job_title in sorted(set(row["Job_Role"] for row in results)):

    job_results = [
        row for row in results
        if row["Job_Role"] == job_title
    ]

    print("\nJOB ROLE:", job_title)
    print("Total comparisons:", len(job_results))
    print("Top 5 matching resumes:")

    for row in job_results[:5]:
        print(
            f"Resume ID: {row['Resume_ID']} | "
            f"Hybrid Score: {row['Hybrid_ATS_Score']}/100"
        )

print("\n========================================")
print("Total comparisons:", len(results))
print("Results saved to:", results_file)
print("Experiment completed successfully!")
