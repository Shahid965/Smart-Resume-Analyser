import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. ATS ANALYSIS ENGINE
def get_ai_analysis(resume_text, jd_text, role):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        prompt = f"""
        Act as a {role}. Analyze this resume. 
        RESUME: {resume_text[:2500]}
        JD: {jd_text if jd_text else 'General Career Optimization'}
        
        Return ONLY a JSON object with these EXACT keys:
        {{
            "strengths": ["list of 3 strings"],
            "feedback": "string of 2 sentences",
            "qualifications": ["list of degrees"],
            "skills": ["list of technical skills"],
            "projects": ["list of projects"],
            "missing_skills": ["list of skills needed for JD"],
            "suggested_projects": ["2 new project ideas"],
            "experience_summary": ["List Roles @ Companies (Dates)"],
            "suggested_roles": ["Top 3 job titles"]
        }}
        """
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"AI ERROR: {e}")
        return {
            "strengths": ["AI currently processing"], "feedback": "Synthesis in progress...",
            "qualifications": [], "skills": [], "projects": [], "missing_skills": [],
            "suggested_projects": [], "experience_summary": [], "suggested_roles": []
        }
# 2. STRATEGIC ROADMAP ENGINE
def get_career_roadmap(resume_text):
    client = get_client()
    prompt = f"""
    Analyze this resume and build a 10-year Strategic Career Roadmap.
    RESUME: {resume_text[:3000]}
    
    Return ONLY a JSON object:
    {{
        "current_standing": "Professional summary of current level",
        "phases": [
            {{"period": "0-1 Year", "title": "Foundation", "actions": ["list"], "skills_to_acquire": ["list"]}},
            {{"period": "2-5 Years", "title": "Acceleration", "actions": ["list"], "skills_to_acquire": ["list"]}},
            {{"period": "5-10 Years", "title": "Apex Level", "actions": ["list"], "skills_to_acquire": ["list"]}}
        ],
        "salary_trajectory": "Analysis of earning potential",
        "ultimate_goal": "A visionary career destination"
    }}
    """
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# 3. LINKEDIN NEURAL AUDIT ENGINE
def get_linkedin_audit(profile_url):
    client = get_client()
    prompt = f"""
    Act as a Branding Architect. Perform a neural audit for this LinkedIn handle: {profile_url}.
    Generate high-end branding strategies based on current global networking algorithms.
    
    Return ONLY a JSON object:
    {{
        "profile_score": 82,
        "headline_strategies": ["3 formulaic headlines"],
        "summary_template": "A powerful bio template",
        "visual_branding": "Banner and photo recommendations",
        "content_roadmap": ["5 trending topics to post about"],
        "profile_gaps": ["common missing LinkedIn sections"],
        "status": "Ready for upscale"
    }}
    """
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)