
import csv
import math
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "experiment_results"
    / "manual_relevance_labels.csv"
)

OUTPUT_DIR = BASE_DIR / "experiment_results"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Evaluation file not found: {INPUT_FILE}"
    )

with INPUT_FILE.open(
    "r", encoding="utf-8-sig", newline=""
) as f:
    rows = list(csv.DictReader(f))

if len(rows) != 75:
    raise ValueError(
        f"Expected 75 records, but found {len(rows)}"
    )

# Validate labels
for row in rows:
    label = row["Relevance_Label"].strip()

    if label not in ("0", "1"):
        raise ValueError(
            f"Invalid or blank label for resume "
            f"{row['Resume_ID']}: {label}"
        )

    row["Relevance_Label"] = int(label)
    row["Hybrid_ATS_Score"] = float(
        row["Hybrid_ATS_Score"]
    )

# Group records by job role
groups = defaultdict(list)

for row in rows:
    groups[row["Job_Role"]].append(row)

metrics = []
ranked_rows = []

for role, records in sorted(groups.items()):

    # Highest hybrid score ranks first
    records.sort(
        key=lambda r: (
            -r["Hybrid_ATS_Score"],
            r["Resume_ID"]
        )
    )

    relevant_total = sum(
        r["Relevance_Label"] for r in records
    )

    # Add ranking positions
    for rank, row in enumerate(records, start=1):
        ranked_rows.append({
            "Job_Role": role,
            "Rank": rank,
            "Resume_ID": row["Resume_ID"],
            "Hybrid_ATS_Score": row["Hybrid_ATS_Score"],
            "Relevance_Label": row["Relevance_Label"]
        })

    top5 = records[:5]

    relevant_top5 = sum(
        r["Relevance_Label"] for r in top5
    )

    precision_at_5 = relevant_top5 / 5

    recall_at_5 = (
        relevant_top5 / relevant_total
        if relevant_total else 0
    )

    # Mean Reciprocal Rank
    reciprocal_rank = 0

    for rank, row in enumerate(records, start=1):
        if row["Relevance_Label"] == 1:
            reciprocal_rank = 1 / rank
            break

    # NDCG@5
    dcg = sum(
    row["Relevance_Label"] / math.log2(rank + 1)
    for rank, row in enumerate(top5, start=1)
)

    ideal_relevance = sorted(
        [r["Relevance_Label"] for r in records],
        reverse=True
    )[:5]

    idcg = sum(
    relevance / math.log2(rank + 1)
    for rank, relevance in enumerate(
        ideal_relevance, start=1
    )
)
    ndcg_at_5 = dcg / idcg if idcg else 0

    metrics.append({
        "Job_Role": role,
        "Total_Resumes": len(records),
        "Relevant_Resumes": relevant_total,
        "Relevant_In_Top5": relevant_top5,
        "Precision_at_5": round(precision_at_5, 4),
        "Recall_at_5": round(recall_at_5, 4),
        "MRR": round(reciprocal_rank, 4),
        "NDCG_at_5": round(ndcg_at_5, 4)
    })

# Save ranking metrics
metrics_file = OUTPUT_DIR / "ranking_metrics.csv"

with metrics_file.open(
    "w", encoding="utf-8-sig", newline=""
) as f:
    writer = csv.DictWriter(
        f, fieldnames=metrics[0].keys()
    )
    writer.writeheader()
    writer.writerows(metrics)

# Save complete ranked resume lists
ranked_file = OUTPUT_DIR / "ranked_resumes.csv"

with ranked_file.open(
    "w", encoding="utf-8-sig", newline=""
) as f:
    writer = csv.DictWriter(
        f, fieldnames=ranked_rows[0].keys()
    )
    writer.writeheader()
    writer.writerows(ranked_rows)

print("\n========== RANKING EVALUATION ==========")
print("Total records:", len(rows))
print("Job roles:", len(groups))
print("Labels validated successfully.")

for result in metrics:
    print("\nJob Role:", result["Job_Role"])
    print("Relevant resumes:", result["Relevant_Resumes"])
    print("Relevant in Top 5:", result["Relevant_In_Top5"])
    print("Precision@5:", result["Precision_at_5"])
    print("Recall@5:", result["Recall_at_5"])
    print("MRR:", result["MRR"])
    print("NDCG@5:", result["NDCG_at_5"])

print("\nSaved metrics:", metrics_file)
print("Saved rankings:", ranked_file)
