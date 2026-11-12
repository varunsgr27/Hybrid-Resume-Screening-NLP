
import csv
from pathlib import Path

from ats_scoring_baseline import (
    calculate_ats_score as baseline_ats_score,
    calculate_skill_coverage as baseline_skill_coverage
)

from ats_scoring import (
    calculate_ats_score as improved_ats_score,
    calculate_skill_coverage as improved_skill_coverage
)

BASE_DIR = Path(__file__).resolve().parent

RESUME_FILE = BASE_DIR / "datasets" / "resumes" / "it_25_resumes.csv"

JD_FOLDER = BASE_DIR / "datasets" / "job_descriptions"

OUTPUT_FOLDER = BASE_DIR / "experiment_results"
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Only use these three job descriptions
JD_FILES = [
    JD_FOLDER / "it_support_specialist.txt",
    JD_FOLDER / "network_administrator.txt",
    JD_FOLDER / "it_systems_analyst.txt"
]

# Check that all required files exist
for file_path in [RESUME_FILE] + JD_FILES:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")

# Load resumes
with RESUME_FILE.open("r", encoding="utf-8-sig", newline="") as file:
    resumes = list(csv.DictReader(file))

print("Total resumes loaded:", len(resumes))

results = []

# Run both dictionary methods on identical inputs
for jd_file in JD_FILES:

    job_title = jd_file.stem.replace("_", " ").title()
    job_description = jd_file.read_text(encoding="utf-8")

    print("\nProcessing:", job_title)

    for resume in resumes:

        resume_text = resume["Resume_str"]

        methods = [
            ("Original Dictionary", baseline_ats_score,
             baseline_skill_coverage),

            ("Expanded Dictionary", improved_ats_score,
             improved_skill_coverage)
        ]

        for method_name, score_function, coverage_function in methods:

            ats_score, similarity = score_function(
                resume_text, job_description
            )

            skill_score, matched, missing = coverage_function(
                resume_text, job_description
            )

            results.append({
                "Resume_ID": resume["ID"],
                "Category": resume["Category"],
                "Job_Role": job_title,
                "Method": method_name,
                "TFIDF_Similarity_Percent": round(
                    similarity * 100, 2
                ),
                "Skill_Coverage_Percent": round(
                    skill_score, 2
                ),
                "Hybrid_ATS_Score": ats_score,
                "Matched_Skills": ", ".join(matched),
                "Missing_Skills": ", ".join(missing)
            })

# Sort results
results.sort(
    key=lambda row: (
        row["Job_Role"],
        row["Resume_ID"],
        row["Method"]
    )
)

# Save results
results_file = (
    OUTPUT_FOLDER / "dictionary_comparison_results.csv"
)

with results_file.open(
    "w", encoding="utf-8-sig", newline=""
) as file:

    writer = csv.DictWriter(
        file, fieldnames=results[0].keys()
    )

    writer.writeheader()
    writer.writerows(results)

print("\n========== EXPERIMENT SUMMARY ==========")
print("Total resumes:", len(resumes))
print("Job descriptions:", len(JD_FILES))
print("Methods compared: 2")
print("Total scoring records:", len(results))

# Print average scores for each role and method
print("\n========== AVERAGE SCORE COMPARISON ==========")

for jd_file in JD_FILES:

    job_title = jd_file.stem.replace("_", " ").title()

    for method in [
        "Original Dictionary",
        "Expanded Dictionary"
    ]:

        selected = [
            row for row in results
            if row["Job_Role"] == job_title
            and row["Method"] == method
        ]

        average_skill = sum(
            row["Skill_Coverage_Percent"]
            for row in selected
        ) / len(selected)

        average_hybrid = sum(
            row["Hybrid_ATS_Score"]
            for row in selected
        ) / len(selected)

        print(
            f"{job_title} | {method} | "
            f"Average Skill Coverage: {average_skill:.2f}% | "
            f"Average Hybrid Score: {average_hybrid:.2f}"
        )

print("\nResults saved to:", results_file)
