
import tempfile
from pathlib import Path

import streamlit as st

from src.document_parser import extract_text
from src.matcher import analyze_resume
from src.semantic_matcher import calculate_semantic_similarity


# Configure the browser page.
st.set_page_config(
    page_title="ResumeIQ",
    page_icon="📄",
    layout="wide",
)


# Main heading and introduction.
st.title("📄 ResumeIQ")
st.subheader("Resume and Job Description Analyzer")

st.write(
    "Compare your resume with a job description to identify "
    "text similarity, semantic similarity, matched skills, "
    "and potential skill gaps."
)

st.info(
    "ResumeIQ provides text-based analysis. Its scores are not "
    "official ATS scores or predictions of hiring success."
)


# Create two columns for the inputs.
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF or DOCX file",
        type=["pdf", "docx"],
    )

with right_column:
    st.subheader("Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=220,
        placeholder=(
            "Paste the job requirements, responsibilities, "
            "and required skills..."
        ),
    )


# Analyze the resume when the user clicks the button.
if st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
):

    if uploaded_file is None:
        st.error("Please upload a PDF or DOCX resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            # Save the uploaded file temporarily so the existing
            # document parser can read it.
            with tempfile.TemporaryDirectory() as temp_directory:
                resume_path = (
                    Path(temp_directory) / uploaded_file.name
                )

                resume_path.write_bytes(uploaded_file.getvalue())

                # Extract text from the uploaded resume.
                resume_text = extract_text(resume_path)

            # Calculate the existing text similarity and skill results.
            results = analyze_resume(
                resume_text,
                job_description,
            )

            # Calculate semantic similarity using Sentence Transformers.
            semantic_score = calculate_semantic_similarity(
                resume_text,
                job_description,
            )

            # Display all three analysis scores.
            st.divider()
            st.header("Analysis Results")

            score_column, semantic_column, skill_column = st.columns(3)

            with score_column:
                st.metric(
                    "Text Similarity",
                    f"{results['similarity_score']}%",
                )

            with semantic_column:
                st.metric(
                    "Semantic Similarity",
                    f"{semantic_score}%",
                )

            with skill_column:
                st.metric(
                    "Skill Match",
                    f"{results['skill_match_percentage']}%",
                )

            # Explain the three scores.
            with st.expander("What do these scores mean?"):
                st.write(
                    "**Text Similarity:** Measures overlap in the "
                    "wording of your resume and the job description."
                )

                st.write(
                    "**Semantic Similarity:** Compares the meaning "
                    "of the resume and job description using a "
                    "pretrained language model."
                )

                st.write(
                    "**Skill Match:** Measures the percentage of "
                    "recognized job-description skills detected "
                    "in your resume."
                )

                st.caption(
                    "These scores measure different things. They are "
                    "not probabilities of getting hired."
                )

            # Display matched skills and potential gaps.
            matched_column, missing_column = st.columns(2)

            with matched_column:
                st.subheader("✅ Matched Skills")

                if results["matched_skills"]:
                    for skill in results["matched_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No matching skills detected.")

            with missing_column:
                st.subheader("📌 Potential Skill Gaps")

                if results["missing_skills"]:
                    for skill in results["missing_skills"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No potential skill gaps detected.")

            # Generate rule-based resume improvement suggestions.
            st.divider()
            st.subheader("💡 Resume Improvement Suggestions")

            suggestions = []

            missing_skills = results["missing_skills"]
            similarity_score = results["similarity_score"]

            # Suggest reviewing job-related skills not detected.
            if missing_skills:
                suggestions.append(
                    "Review these job-related skills that were not "
                    "detected in your resume: "
                    + ", ".join(missing_skills[:5])
                    + ". Include them only if they reflect your real skills."
                )
            else:
                suggestions.append(
                    "All recognized job-description skills were detected. "
                    "Review whether your examples demonstrate these skills."
                )

            # Give suggestions based on textual similarity.
            if similarity_score < 30:
                suggestions.append(
                    "The text similarity is relatively low. Review your "
                    "project descriptions and experience to make relevant "
                    "qualifications clearer."
                )
            elif similarity_score < 50:
                suggestions.append(
                    "Consider making your most relevant projects, skills, "
                    "and experience more explicit in your resume."
                )
            else:
                suggestions.append(
                    "Your resume has reasonable textual overlap with the "
                    "job description. Support relevant skills with concrete "
                    "examples from your projects or experience."
                )

            # Provide a general improvement suggestion.
            suggestions.append(
                "Use specific project examples to demonstrate how you "
                "applied your skills, rather than listing keywords alone."
            )

            # Display each suggestion.
            for suggestion in suggestions:
                st.write(f"• {suggestion}")

            # Show all recognized skills from the resume.
            with st.expander("View All Skills Detected in Resume"):
                if results["resume_skills"]:
                    st.write(", ".join(results["resume_skills"]))
                else:
                    st.write("No known skills detected.")

            # Explain how to interpret the results.
            st.caption(
                "Skill matching uses a predefined skill dictionary. "
                "A skill gap means the skill was not detected; it does "
                "not prove that you lack that skill. Text similarity "
                "thresholds are guidance, not validated hiring criteria."
            )

        except (ValueError, FileNotFoundError) as error:
            st.error(str(error))

        except Exception as error:
            st.error(
                "An unexpected error occurred during analysis. "
                f"Details: {error}"
            )
