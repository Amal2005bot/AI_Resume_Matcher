import PyPDF2
import re
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + " "
    return re.sub(r'\s+', ' ', text).strip()

def clean_text(text):
    doc = nlp(text.lower())
    # Keep only the 'important' root words
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def get_matching_skills(resume_text, job_desc_text):
    """Finds words that appear in both the resume and the job description."""
    # Convert both to sets of words
    resume_words = set(resume_text.split())
    job_words = set(job_desc_text.split())
    
    # Find the intersection (words in both)
    common_skills = resume_words.intersection(job_words)
    return list(common_skills)

def get_missing_skills(resume_text, job_desc_text):
    """Finds words in the JD that are NOT in the resume."""
    resume_words = set(resume_text.split())
    job_words = set(job_desc_text.split())
    
    missing = job_words - resume_words
    return list(missing)