import json
import os

def load_skills():
    path = os.path.join(os.path.dirname(__file__), '../data/skills.json')
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    return data['skills']

def extract_skills(text):
    skills_db = load_skills()
    text = text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill)

    return found_skills