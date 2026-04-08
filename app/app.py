import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- LOAD MODEL ---------------- #
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------- PDF PARSER ---------------- #
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# ---------------- EMBEDDING ---------------- #
def get_embedding(text):
    return model.encode(text)

# ---------------- MATCHING ---------------- #
def match_jobs(resume_text, jobs):
    resume_emb = get_embedding(resume_text)
    results = []

    for job in jobs:
        job_emb = get_embedding(job)
        score = cosine_similarity([resume_emb], [job_emb])[0][0]
        results.append((job, float(score)))  # ✅ FIX HERE

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

# ---------------- SKILL EXTRACTION ---------------- #
skills_db = [
    "python", "java", "sql", "machine learning",
    "deep learning", "nlp", "html", "css",
    "javascript", "react", "node", "spring boot", "excel"
]

def extract_skills(text):
    text = text.lower()
    return [skill for skill in skills_db if skill in text]

# ---------------- SKILL GAP ---------------- #
def skill_gap(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    return matched, missing

# ---------------- AI FEEDBACK ---------------- #
def generate_feedback(resume_skills, missing_skills, job):
    feedback = []

    if missing_skills:
        feedback.append(f"❗ Add these skills for {job}: {', '.join(missing_skills)}")

    if "projects" not in resume_skills:
        feedback.append("📌 Add more projects related to your target role")

    feedback.append("📄 Improve resume formatting and add measurable achievements")
    feedback.append("🚀 Include internships or real-world experience")

    return feedback

# ---------------- JOB DATA ---------------- #
jobs = [
    "Data Scientist Python Machine Learning SQL",
    "Frontend Developer React JavaScript HTML CSS",
    "Backend Developer Java Spring Boot SQL",
    "AI Engineer Deep Learning NLP Python",
    "Data Analyst SQL Excel Python PowerBI"
]

job_requirements = {
    jobs[0]: ["python", "machine learning", "sql"],
    jobs[1]: ["html", "css", "javascript", "react"],
    jobs[2]: ["java", "spring boot", "sql"],
    jobs[3]: ["python", "deep learning", "nlp"],
    jobs[4]: ["sql", "excel", "python"]
}

# ---------------- UI ---------------- #
st.title("🚀 AI Resume Analyzer (Final Version)")

uploaded_file = st.file_uploader("Upload Resume", type="pdf")

if uploaded_file:
    resume_text = extract_text(uploaded_file)

    st.subheader("📄 Resume Preview")
    st.write(resume_text[:300])

    # ---------------- MATCH ---------------- #
    results = match_jobs(resume_text, jobs)

    st.markdown("## 🎯 Top Job Matches")

    for job, score in results:
        score = max(0.0, min(1.0, score))  # safety clamp

        st.write(f"🔹 {job}")
        st.progress(score)  # ✅ no error now
        st.write(f"Match Score: {round(score * 100, 2)}%")
        st.write("---")

    # ---------------- SKILLS ---------------- #
    resume_skills = extract_skills(resume_text)

    st.markdown("## 🧠 Extracted Skills")
    st.write(resume_skills)

    # ---------------- GAP + FEEDBACK ---------------- #
    st.markdown("## 📊 Skill Gap & Suggestions")

    for job, score in results:
        required = job_requirements.get(job, [])

        matched, missing = skill_gap(resume_skills, required)

        st.write(f"🔹 {job}")
        st.write(f"✅ Matched: {matched}")
        st.write(f"❌ Missing: {missing}")

        feedback = generate_feedback(resume_skills, missing, job)

        st.write("🤖 Suggestions:")
        for f in feedback:
            st.write(f)

        st.write("---")