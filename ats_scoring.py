import re # THIS WAS MISSING

def clean_text(text):
    if not text: return ""
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return " ".join(text.split())

def calculate_ats_score(resume_text, jd_text, sections, skills):
    if not resume_text:
        return 0, "Empty"

    res_clean = clean_text(resume_text)
    
    # 1. SECTION SCORE (30%)
    sec_count = sum(1 for s in sections.values() if s is True)
    sec_score = (sec_count / len(sections)) * 100 if sections else 0

    # 2. SKILL SCORE (30%)
    skill_score = min(100, (len(skills) / 8) * 100)

    # 3. JD MATCH SCORE (40%)
    if jd_text and len(jd_text.strip()) > 5:
        jd_clean = clean_text(jd_text)
        jd_words = [w for w in jd_clean.split() if len(w) > 3]
        matches = sum(1 for w in jd_words if w in res_clean)
        jd_match = (matches / len(jd_words)) * 100 if jd_words else 0
    else:
        # If no JD, we treat the remaining 40% as a bonus for profile length
        jd_match = min(100, (len(res_clean) / 500) * 100)

    final_score = (jd_match * 0.4) + (sec_score * 0.3) + (skill_score * 0.3)
    final_score = round(min(100, final_score), 2)

    if final_score > 80: rating = "Excellent"
    elif final_score > 60: rating = "Good"
    elif final_score > 35: rating = "Average"
    else: rating = "Poor"

    return final_score, rating