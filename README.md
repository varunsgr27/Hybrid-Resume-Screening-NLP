# Hybrid Resume Screening and Job Matching System Using NLP

A Python and Streamlit-based academic machine learning mini-project that compares a candidate's PDF resume with a job description. It combines **TF-IDF cosine similarity** with **weighted technical-skill coverage** to produce an interpretable hybrid matching score and show matched and missing skills.

> **Important:** The displayed score is a project-specific text and skill-matching score. It is not a score from a commercial Applicant Tracking System (ATS), a prediction of hiring probability, or a guarantee of shortlisting.

## Project Overview

Recruiters may need to compare many resumes against role requirements. This project explores a lightweight, explainable approach to resume screening by combining two signals:

1. **Text similarity:** Measures overlap between resume text and job-description text using a TF-IDF-style representation and cosine similarity.
2. **Technical-skill coverage:** Detects skills from a predefined dictionary and calculates weighted coverage. Required skills receive weight 2 and preferred skills receive weight 1.

The final hybrid score is calculated as:

**Hybrid Score = (0.40 × TF-IDF Similarity) + (0.60 × Weighted Skill Coverage)**

Both input components are expressed as percentages, so the resulting score is on a 0–100 scale.

## Features

- Upload a resume in PDF format.
- Paste a job description into the Streamlit interface.
- Extract PDF text using PyMuPDF.
- Calculate TF-IDF-style cosine similarity.
- Identify technical skills using a predefined, category-based skill dictionary.
- Give required skills greater weight than preferred skills when the job description uses the supported section labels.
- Display the hybrid score, text similarity, and skill-coverage percentage.
- List matched and missing skills.
- Provide suggestions based on missing skills.

## Technology Stack

- Python
- Streamlit
- PyMuPDF
- scikit-learn (listed in project dependencies)
- Regular expressions and Python standard library
- TF-IDF-style term weighting and cosine similarity

## Application Workflow

1. The user uploads a PDF resume and enters a job description.
2. PyMuPDF extracts text from the PDF.
3. The application calculates text similarity between the resume and job description.
4. The skill dictionary identifies supported technical skills in both texts.
5. Required and preferred skills are weighted to calculate skill coverage.
6. The application combines the two percentages using the 40:60 weighting.
7. Streamlit displays the score, matched skills, missing skills, and suggestions.

## Project Structure

```text
Hybrid-Resume-Screening-NLP/
├── app.py
├── resume_parser.py
├── ats_scoring.py
├── keyword_matcher.py
├── ats_scoring_baseline.py
├── keyword_matcher_baseline.py
├── create_evaluation_dataset.py
├── evaluate_ranking.py
├── run_comparison.py
├── run_experiment.py
├── requirements.txt
├── screenshots/
└── README.md
```

The baseline files preserve the earlier scoring and skill-dictionary implementations for comparison. The experiment scripts support dataset preparation, comparison, and ranking evaluation.

## Run the Application Locally

### 1. Clone this repository

```powershell
git clone https://github.com/varunsgr27/Hybrid-Resume-Screening-NLP.git
cd Hybrid-Resume-Screening-NLP
```

### 2. Create a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the app using the virtual environment's Python executable directly, or use Command Prompt activation:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start Streamlit

```powershell
python -m streamlit run app.py
```

Streamlit will provide a local URL in the terminal. Open it in your browser, upload a readable PDF resume, paste a job description, and select **Analyze Resume**.

## Experimental Evaluation

The project also includes scripts used for a comparative experiment with a subset of the Kaggle Resume Dataset:

- Dataset source: [Resume Dataset on Kaggle](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- Experiment subset: 25 records from the dataset's `INFORMATION-TECHNOLOGY` category.
- Job roles evaluated: IT Support Specialist, Network Administrator, and IT Systems Analyst.
- Comparison: Original versus expanded predefined skill dictionaries.
- Ranking metrics: Precision@5, Recall@5, Mean Reciprocal Rank (MRR), and NDCG@5.

The experimental dataset and generated result files are not included in this repository. They are excluded from version control because resume data may contain personal information. Obtain the dataset from its source and prepare the local experiment files before running the experiment scripts.

### Interpreting the Evaluation

The relevance labels used in the current ranking experiment are **provisional, automatically generated labels**, not independently annotated ground truth. Consequently, the ranking metrics are exploratory results for this project and must not be interpreted as independently validated ranking accuracy or evidence of real-world hiring performance.

The experiment used a selected subset of 25 records, not a random or representative sample of all resumes. The skill matcher is dictionary- and regular-expression-based; it does not understand every synonym, context, or equivalent skill. Results therefore depend on the resume text, job-description wording, skill dictionary, and selected sample.

## Screenshots

The following screenshots illustrate the application interface and analysis output:

![Application screenshot 1](screenshots/scr1.png)

![Application screenshot 2](screenshots/scr2.png)

![Application screenshot 3](screenshots/scr3.png)

## Limitations

- The skill dictionary is predefined and may miss synonyms, emerging technologies, or skills expressed in different wording.
- Matching is primarily lexical; it does not use a trained semantic language model.
- PDF text extraction may fail for scanned or image-only PDFs unless OCR is applied separately.
- The hybrid score is a heuristic project metric, not a standardized ATS score.
- Evaluation is based on a small selected sample and provisional relevance labels.
- The system should support human review, not make hiring decisions automatically.

## Future Work

- Expand and validate the skill dictionary, including synonym handling.
- Add OCR support for scanned resumes.
- Evaluate with a larger and independently human-labelled dataset.
- Explore semantic embeddings and compare them against the current lexical baseline.
- Add resume-section extraction and structured explanations.
- Improve usability and consider deployment after further testing.

## Academic Project

**Project title:** Hybrid Resume Screening and Job Matching System Using Natural Language Processing (NLP)  
**Course:** Machine Learning (25MCA31)  
**Project type:** MCA Machine Learning mini-project

## Acknowledgement and Attribution

This repository is an adapted and extended academic project based on the open-source [ATS Resume Analyzer by Shrihari Padatare](https://github.com/iamshrihari/ATS-Resume-Analyzer). The original repository's MIT license is retained in this project. The hybrid scoring changes, expanded skill dictionary, baseline comparison, and experiment scripts were added as part of this project.

## Author

**Varun D**  
GitHub: [@varunsgr27](https://github.com/varunsgr27)