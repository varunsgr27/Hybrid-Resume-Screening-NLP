
import streamlit as st

from resume_parser import extract_text_from_pdf
from ats_scoring import (
    calculate_ats_score,
    calculate_skill_coverage
)

st.set_page_config(
    page_title="ATS Resume Analyzer",
    layout="wide"
)

st.title("ATS Resume Analyzer")
st.write(
    "Upload your Resume PDF and paste the Job Description "
    "to analyze your resume."
)

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_desc = st.text_area(
    "Paste Job Description Here",
    height=250
)

if st.button("Analyze Resume"):

    if resume_file is None or job_desc.strip() == "":
        st.warning("Please upload a resume PDF and enter job description.")

    else:
        resume_text = extract_text_from_pdf(resume_file)

        if not resume_text.strip():
            st.error("No text found in the PDF. Please upload a readable PDF.")
        else:
            # Calculate Hybrid ATS Score
            ats_score, similarity = calculate_ats_score(
                resume_text, job_desc
            )

            # Calculate technical skill coverage
            skill_score, matched, missing = calculate_skill_coverage(
                resume_text, job_desc
            )

            # Display results
            st.subheader("ATS Analysis Results")

            st.metric("Hybrid ATS Score", f"{ats_score}/100")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "TF-IDF Similarity",
                    f"{similarity * 100:.2f}%"
                )

            with col2:
                st.metric(
                    "Technical Skill Coverage",
                    f"{skill_score:.2f}%"
                )

            st.progress(ats_score / 100)

            # Matched and missing skills
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Matched Technical Skills")

                if matched:
                    for skill in matched:
                        st.write(f"✓ {skill}")
                else:
                    st.info("No matching technical skills found.")

            with col2:
                st.subheader("Missing Technical Skills")

                if missing:
                    for skill in missing:
                        st.write(f"- {skill}")
                else:
                    st.success("All identified skills are matched!")

            # Suggestions
            st.subheader("Improvement Suggestions")

            if missing:
                st.write(
                    "Consider including these skills in your resume "
                    "if you genuinely have experience with them:"
                )

                for skill in missing[:10]:
                    st.write(f"- {skill}")
            else:
                st.success(
                    "Your resume contains all the identified "
                    "technical skills from this job description."
                )
