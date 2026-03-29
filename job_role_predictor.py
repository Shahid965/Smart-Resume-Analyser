def predict_role(skills):
    skills_str = " ".join(skills).lower()
    if any(s in skills_str for s in ['tensorflow', 'pytorch', 'machine learning', 'nlp']):
        return "AI/ML Engineer"
    if any(s in skills_str for s in ['react', 'vue', 'angular', 'next.js']):
        return "Frontend Developer"
    if any(s in skills_str for s in ['node', 'django', 'flask', 'spring']):
        return "Backend Developer"
    if any(s in skills_str for s in ['aws', 'docker', 'kubernetes', 'jenkins']):
        return "DevOps Engineer"
    if any(s in skills_str for s in ['tableau', 'powerbi', 'pandas', 'spark']):
        return "Data Analyst"
    return "Software Engineer"