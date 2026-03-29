import re

SKILL_DB = [
    'python', 'java', 'javascript', 'typescript', 'react', 'node', 'sql', 'mongodb',
    'aws', 'azure', 'docker', 'kubernetes', 'machine learning', 'data science',
    'tableau', 'powerbi', 'excel', 'c++', 'c#', 'php', 'flask', 'django', 'html', 'css'
]

def extract_skills(text):
    text_lower = text.lower()
    found = []
    for skill in SKILL_DB:
        # Use word boundaries to avoid partial matches (e.g., 'c' in 'cat')
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.append(skill.upper())
    return list(set(found))