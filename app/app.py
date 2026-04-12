import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("AI Resume Analyzer")
st.write("Upload your resume and check job match + skill gaps")

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ---------------- FUNCTIONS ---------------- #
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def get_embedding(text):
    return model.encode(text)

def match_jobs(resume_text, jobs):
    resume_emb = get_embedding(resume_text)
    results = []

    for job in jobs:
        job_emb = get_embedding(job)
        score = cosine_similarity([resume_emb], [job_emb])[0][0]
        results.append((job, float(score)))

    return sorted(results, key=lambda x: x[1], reverse=True)

skills_db = [
    "python","java","sql","machine learning","deep learning",
    "html","css","javascript","react","excel"
]

def extract_skills(text):
    text = text.lower()
    return [s for s in skills_db if s in text]

def skill_gap(resume_skills, job_skills):
    return list(set(resume_skills)&set(job_skills)), list(set(job_skills)-set(resume_skills))

# ---------------- JOB DATA ---------------- #
jobs = [
    "Data Scientist Python Machine Learning SQL",
    "Frontend Developer React JavaScript HTML CSS",
    "Backend Developer Java SQL",
    "Data Analyst SQL Excel Python"
]

job_req = {
    jobs[0]: ["python","machine learning","sql"],
    jobs[1]: ["html","css","javascript","react"],
    jobs[2]: ["java","sql"],
    jobs[3]: ["sql","excel","python"]
}

# ---------------- UI ---------------- #
file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if file:
    text = extract_text(file)

    st.subheader("Resume Preview")
    st.write(text[:500])

    # MATCHING
    st.subheader("Top Job Matches")
    results = match_jobs(text, jobs)

    for job, score in results:
        safe_score = (score + 1) / 2   # fix negative issue
        st.write(job)
        st.progress(safe_score)
        st.write(f"{round(safe_score*100,2)}% match")
        st.write("---")

    # SKILLS
    skills = extract_skills(text)
    st.subheader("Extracted Skills")
    st.write(skills)

    # GAP
    st.subheader("Skill Gap Analysis")

    for job,_ in results:
        matched, missing = skill_gap(skills, job_req[job])

        st.write(f"Job: {job}")
        st.write("Matched:", matched)
        st.write("Missing:", missing)
        st.write("---")

else:
    st.info("Upload your resume to begin")