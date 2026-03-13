from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(resume_text, job_desc_text):
    content = [resume_text, job_desc_text]
    cv = TfidfVectorizer()
    matrix = cv.fit_transform(content)
    similarity_matrix = cosine_similarity(matrix)
    match_percentage = similarity_matrix[0][1] * 100
    return round(match_percentage, 2)