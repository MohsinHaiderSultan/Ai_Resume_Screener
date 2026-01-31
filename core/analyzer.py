from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.utils import clean_text
import re

def rank_candidates(resume_text, job_desc, weights=(50, 30, 20)):
    """
    Enhanced ranking engine with weighted scoring and gap analysis.
    weights: (Skills Weight, Experience Weight, Education Weight)
    """
    clean_resume = clean_text(resume_text)
    clean_jd = clean_text(job_desc)

    # 1. Semantic Similarity (Skills Weight)
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform([clean_jd, clean_resume])
    sim_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    # 2. Key Term Extraction & Gap Analysis
    jd_keywords = extract_skills_v2(clean_jd)
    resume_keywords = extract_skills_v2(clean_resume)
    
    matched = jd_keywords.intersection(resume_keywords)
    missing = jd_keywords.difference(resume_keywords)
    
    # 3. Seniority & Experience Analysis
    exp_info = detect_experience(resume_text)
    jd_exp_info = detect_experience(job_desc)
    
    # Simple experience score: if candidate years >= JD years
    exp_score = 1.0 if exp_info['years'] >= jd_exp_info['years'] else (exp_info['years'] / max(1, jd_exp_info['years']))

    # 4. Final Weighted Calculation
    w1, w2, w3 = weights
    # Normalize weights to ensure total score is 0-100
    total_weight = w1 + w2 + w3
    final_score = (
        ((sim_score * w1) + 
         (exp_score * w2) + 
         (0.8 * w3)) / total_weight
    ) * 100

    return {
        "score": round(final_score, 1),
        "skills": list(matched)[:15],
        "missing_skills": list(missing)[:10],
        "experience_match": f"{exp_info['years']} Years Found",
        "seniority_level": exp_info['level'],
        "summary": generate_summary(matched, exp_info['years'], exp_info['level'])
    }

def extract_skills_v2(text):
    """Simple skill extractor using regex for tech-heavy terms."""
    common_tech = r'\b(python|java|javascript|react|aws|azure|sql|node|docker|kubernetes|typescript|c\+\+|linux|machine learning|data science|flutter|kotlin|swift|agile|scrum|devops|rest api|mongodb|postgresql|spark|hadoop)\b'
    matches = re.findall(common_tech, text.lower())
    return set(matches)

def detect_experience(text):
    """Heuristic to detect years of experience and seniority."""
    exp_patterns = [
        r'(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?'
    ]
    years = 0
    for p in exp_patterns:
        matches = re.findall(p, text.lower())
        if matches:
            years = max([int(m) for m in matches])
    
    level = "Junior"
    if years > 8: level = "Architect/Principal"
    elif years > 5: level = "Senior"
    elif years > 2: level = "Intermediate"
    
    return {"years": years, "level": level}

def generate_summary(skills, years, level):
    if not skills:
        return "Generic profile with low semantic match to core tech requirements."
    return f"A {level} professional with {years} years of experience. Demonstrated strength in {', '.join(list(skills)[:3])}. Developed by Mohsin Haider Sultan."