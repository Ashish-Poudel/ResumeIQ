# ResumeIQ — Resume and Job Description Analyzer

ResumeIQ is an NLP-based project that analyzes a resume against a job description. It measures text similarity, compares semantic meaning, identifies relevant skills, highlights potential skill gaps, and provides rule-based improvement suggestions.

## Features

- **Resume Parsing:** Extracts text from PDF and DOCX files.
- **Text Similarity:** Uses TF-IDF and cosine similarity to measure textual overlap.
- **Semantic Similarity:** Uses Sentence Transformers to compare the meaning of a resume and a job description.
- **Skill Matching:** Identifies recognized skills using a predefined skill dictionary.
- **Skill Gap Analysis:** Highlights job-related skills that were not detected in the resume.
- **Improvement Suggestions:** Provides rule-based suggestions for improving resume relevance.
- **Interactive Interface:** Uses Streamlit to display analysis results.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Sentence Transformers
- PyMuPDF
- python-docx

## Project Structure

```text
ResumeIQ/
├── src/
│   ├── app.py
│   ├── document_parser.py
│   ├── matcher.py
│   ├── semantic_matcher.py
│   └── text_cleaner.py
├── sample_data/
├── tests/
├── requirements.txt
└── README.md
```

The `sample_data` and `tests` folders are included if present in the project.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ResumeIQ
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL after publishing the project.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run ResumeIQ

From the project's root directory, execute:

```bash
python -m streamlit run src/app.py
```

Streamlit will provide a local URL to open in your browser.

The first semantic analysis may take longer because the pretrained Sentence Transformer model may need to be downloaded.

## How It Works

1. The user uploads a PDF or DOCX resume.
2. ResumeIQ extracts and cleans the resume text.
3. The user supplies a job description.
4. TF-IDF and cosine similarity calculate textual similarity.
5. Sentence Transformers generates embeddings to calculate semantic similarity.
6. A predefined skill dictionary identifies matched skills and potential gaps.
7. Rule-based logic generates resume improvement suggestions.
8. Streamlit displays the results.

## Understanding the Scores

- **Text Similarity:** Measures overlap in wording between the resume and job description.
- **Semantic Similarity:** Measures similarity between their embedding representations.
- **Skill Match:** Measures the proportion of recognized job-description skills detected in the resume.

These scores measure different aspects of relevance. They are not official ATS scores or probabilities of getting hired. Skill gaps indicate that a skill was not detected, not necessarily that the candidate lacks it.

## Limitations

- Scanned PDFs without selectable text are not processed using OCR.
- Skill matching depends on a predefined dictionary and may miss synonyms or context.
- Semantic similarity does not independently verify qualifications or work experience.
- Improvement suggestions use rules rather than personalized generative AI.
- Similarity scores should be interpreted as supporting signals, not hiring decisions.

## Future Improvements

- Improve contextual skill extraction.
- Evaluate matching quality using a larger set of realistic resumes and job descriptions.
- Improve handling of complex resume layouts and document sections.
- Add more comprehensive evaluation metrics when a suitable labeled dataset is available.

