
from pathlib import Path

from src.document_parser import extract_text
from src.matcher import analyze_resume


def main():
    # Ask for the resume file location.
    resume_path = input(
        "Enter the path to your PDF or DOCX resume: "
    ).strip().strip('"')

    # Read the job description from the terminal.
    print("\nPaste the job description below.")
    print("When finished, press Ctrl+Z and Enter on Windows.\n")

    job_description_lines = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        job_description_lines.append(line)

    job_description = "\n".join(job_description_lines)

    # Extract text from the resume.
    resume_text = extract_text(Path(resume_path))

    # Analyze the resume against the job description.
    results = analyze_resume(
        resume_text,
        job_description
    )

    # Display the results.
    print("\n========== ResumeIQ Analysis ==========")

    print(f"Text similarity: {results['similarity_score']}%")
    print(f"Skill match: {results['skill_match_percentage']}%")

    print("\nMatched skills:")
    print(
        ", ".join(results["matched_skills"])
        or "None detected"
    )

    print("\nPotential skill gaps:")
    print(
        ", ".join(results["missing_skills"])
        or "None detected"
    )

    print("\nSkills detected in resume:")
    print(
        ", ".join(results["resume_skills"])
        or "None detected"
    )

    print("\n=======================================")


if __name__ == "__main__":
    main()
