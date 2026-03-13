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

def get_matching_skills(resume_text, job_text):
    # Process both texts with spaCy
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_text)
    
    resume_skills = {token.lemma_.lower() for token in resume_doc 
                     if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2}
    
    job_skills = {token.lemma_.lower() for token in job_doc 
                  if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and len(token.text) > 2}
    
    # Find the intersection (words in both)
    matching = list(resume_skills.intersection(job_skills))
    
    return sorted(matching)

def get_missing_skills(resume_text, job_desc_text):
    """Finds words in the JD that are NOT in the resume."""
    resume_words = set(resume_text.split())
    job_words = set(job_desc_text.split())
    
    missing = job_words - resume_words
    return list(missing)
