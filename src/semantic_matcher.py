
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the pretrained model once when this module is imported.
# Reusing the model avoids reloading it for every analysis.
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(
    resume_text: str,
    job_description: str
) -> float:
    """
    Compare the semantic meaning of a resume and job description.

    Returns:
        Similarity score as a percentage between 0 and 100.
    """

    # Handle empty inputs before generating embeddings.
    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    # Convert both documents into numerical embeddings.
    embeddings = model.encode(
        [resume_text, job_description],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    # Compare the embeddings using cosine similarity.
    score = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1),
    )[0][0]

    # Convert to a percentage and keep the result in the 0–100 range.
    percentage = max(0.0, min(100.0, float(score) * 100))

    return round(percentage, 2)
