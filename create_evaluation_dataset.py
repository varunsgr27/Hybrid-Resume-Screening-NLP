
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RESULT_FILE = BASE_DIR / "experiment_results" / "dictionary_comparison_results.csv"
RESUME_FILE = BASE_DIR / "datasets" / "resumes" / "it_25_resumes.csv"
OUTPUT_FILE = BASE_DIR / "experiment_results" / "manual_relevance_labels.csv"

with RESULT_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    results = list(csv.DictReader(f))

results = [
    row for row in results
    if row["Method"] == "Expanded Dictionary"
]

with RESUME_FILE.open("r", encoding="utf-8-sig", newline="") as f:
    resumes = {
        row["ID"]: row
        for row in csv.DictReader(f)
    }

results.sort(
    key=lambda row: (
        row["Job_Role"],
        -float(row["Hybrid_ATS_Score"])
    )
)

evaluation_rows = []

for row in results:
    resume = resumes[row["Resume_ID"]]

    evaluation_rows.append({
        "Resume_ID": row["Resume_ID"],
        "Job_Role": row["Job_Role"],
        "Hybrid_ATS_Score": row["Hybrid_ATS_Score"],
        "Matched_Skills": row["Matched_Skills"],
        "Missing_Skills": row["Missing_Skills"],
        "Resume_Text": resume["Resume_str"],
        "Relevance_Label": ""
    })

with OUTPUT_FILE.open(
    "w", encoding="utf-8-sig", newline=""
) as f:
    writer = csv.DictWriter(
        f, fieldnames=evaluation_rows[0].keys()
    )
    writer.writeheader()
    writer.writerows(evaluation_rows)

print("Evaluation dataset created successfully.")
print("Total resume-job pairs:", len(evaluation_rows))
print("Output file:", OUTPUT_FILE)
