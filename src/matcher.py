
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.text_cleaner import clean_text


# Skills are grouped by domain to support different job roles.
# Each key is the standardized skill name shown in the results.
# Each list contains alternative terms that may appear in a document.

SKILL_PATTERNS = {
    # Programming languages
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "java script"],
    "typescript": ["typescript"],
    "c": ["c programming", "c language"],
    "c++": ["c++"],
    "c#": ["c#", "c sharp"],
    "php": ["php"],
    "ruby": ["ruby"],
    "go": ["golang", "go programming"],
    "rust": ["rust programming"],
    "kotlin": ["kotlin"],
    "swift": ["swift programming"],
    "r programming": ["r programming", "r language"],
    "matlab": ["matlab"],
    "bash": ["bash", "bash scripting"],
    "powershell": ["powershell"],

    # Web development
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular", "angular.js", "angularjs"],
    "vue": ["vue.js", "vuejs"],
    "node.js": ["node.js", "nodejs"],
    "express.js": ["express.js", "expressjs"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "rest api": ["rest api", "restful api", "restful services"],
    "graphql": ["graphql"],
    "responsive design": ["responsive design", "responsive web design"],
    "web development": ["web development"],

    # Databases and data storage
    "sql": ["sql", "structured query language"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "sqlite": ["sqlite", "sqlite3"],
    "mongodb": ["mongodb", "mongo db"],
    "redis": ["redis"],
    "oracle database": ["oracle database", "oracle db"],
    "database design": ["database design"],
    "database management": ["database management", "database administration"],
    "data modeling": ["data modeling", "database modeling"],
    "data warehousing": ["data warehousing", "data warehouse"],
    "nosql": ["nosql", "no sql"],

    # Data science and analytics
    "data analysis": ["data analysis", "data analytics", "analyzing data"],
    "data science": ["data science"],
    "data cleaning": ["data cleaning", "data preprocessing"],
    "exploratory data analysis": [
        "exploratory data analysis",
        "eda",
    ],
    "statistics": ["statistics", "statistical analysis"],
    "probability": ["probability theory"],
    "regression": ["regression", "regression analysis"],
    "data visualization": ["data visualization", "data visualisation"],
    "data mining": ["data mining"],
    "business intelligence": ["business intelligence"],
    "excel": ["excel", "microsoft excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],

    # Machine learning and artificial intelligence
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "natural language processing": [
        "natural language processing",
        "nlp",
    ],
    "computer vision": ["computer vision"],
    "neural networks": ["neural networks", "neural network"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "opencv": ["opencv", "open cv"],
    "transformers": ["transformers", "transformer models"],
    "large language models": [
        "large language models",
        "large language model",
        "llms",
    ],
    "generative ai": ["generative ai", "genai"],
    "feature engineering": ["feature engineering"],
    "model evaluation": ["model evaluation", "model validation"],
    "predictive modeling": ["predictive modeling", "predictive modelling"],

    # Cloud, DevOps, and software tools
    "git": ["git", "version control"],
    "github": ["github"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux"],
    "windows": ["windows operating system"],
    "aws": ["amazon web services", "aws"],
    "azure": ["microsoft azure", "azure cloud"],
    "google cloud": ["google cloud platform", "google cloud", "gcp"],
    "ci/cd": ["ci/cd", "continuous integration", "continuous delivery"],
    "jenkins": ["jenkins"],
    "terraform": ["terraform"],
    "agile": ["agile methodology", "agile"],
    "scrum": ["scrum"],

    # Networking and cybersecurity
    "computer networking": ["computer networking", "networking"],
    "tcp/ip": ["tcp/ip", "tcp ip"],
    "dns": ["dns", "domain name system"],
    "dhcp": ["dhcp"],
    "routing and switching": ["routing and switching"],
    "network security": ["network security"],
    "cybersecurity": ["cybersecurity", "cyber security"],
    "ethical hacking": ["ethical hacking"],
    "penetration testing": ["penetration testing", "pentesting"],
    "cryptography": ["cryptography"],
    "firewalls": ["firewall", "firewalls"],
    "vpn": ["vpn", "virtual private network"],
    "wireshark": ["wireshark"],
    "incident response": ["incident response"],
    "vulnerability assessment": ["vulnerability assessment"],

    # Software engineering and testing
    "data structures": ["data structures", "data structure"],
    "algorithms": ["algorithms", "algorithm design"],
    "object-oriented programming": [
        "object-oriented programming",
        "oop",
    ],
    "software development": ["software development"],
    "software testing": ["software testing"],
    "unit testing": ["unit testing"],
    "pytest": ["pytest"],
    "selenium": ["selenium"],
    "debugging": ["debugging"],
    "system design": ["system design"],
    "microservices": ["microservices", "microservice architecture"],
    "api development": ["api development"],

    # General professional skills
    "communication": ["communication", "communication skills"],
    "problem solving": ["problem solving", "problem-solving"],
    "leadership": ["leadership", "team leadership"],
    "teamwork": ["teamwork", "team work"],
    "collaboration": ["collaboration", "cross-functional collaboration"],
    "project management": ["project management"],
    "critical thinking": ["critical thinking"],
    "analytical thinking": ["analytical thinking"],
    "time management": ["time management"],
    "presentation skills": ["presentation skills"],
    "technical writing": ["technical writing"],
    "research": ["research skills"],
    "handling pressure": ["handling pressure", "working under pressure"],
    "requirements analysis": ["requirements analysis"],
}


def contains_phrase(text: str, phrase: str) -> bool:
    """
    Check for a phrase without matching it inside unrelated words.

    For example, 'java' should not match 'javascript'.
    The boundary handling also supports terms such as C++ and C#.
    """

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(phrase.lower())
        + r"(?![a-z0-9])"
    )

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def extract_skills(text: str) -> set[str]:
    """
    Identify known skills in a resume or job description.

    Returns standardized skill names, regardless of which
    recognized alternative term appeared in the text.
    """

    text = clean_text(text)
    found_skills = set()

    for skill, patterns in SKILL_PATTERNS.items():
        for phrase in patterns:
            if contains_phrase(text, phrase):
                found_skills.add(skill)
                break

    return found_skills


def calculate_similarity(
    resume_text: str,
    job_description: str,
) -> float:
    """
    Calculate TF-IDF cosine similarity as a percentage.

    This measures textual overlap, not hiring probability.
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        raise ValueError(
            "Resume text and job description must not be empty."
        )

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [resume_text, job_description]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2],
    )[0][0]

    return round(float(similarity) * 100, 2)


def analyze_resume(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare a resume with a job description.

    Returns similarity, skill match percentage, detected skills,
    matched skills, and potential skill gaps.
    """

    score = calculate_similarity(
        resume_text,
        job_description,
    )

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched_skills = resume_skills & job_skills
    missing_skills = job_skills - resume_skills

    # Calculate the percentage of recognized job skills
    # that were also detected in the resume.
    if job_skills:
        skill_match_percentage = round(
            len(matched_skills) / len(job_skills) * 100,
            2,
        )
    else:
        skill_match_percentage = 0.0

    return {
        "similarity_score": score,
        "skill_match_percentage": skill_match_percentage,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
    }
