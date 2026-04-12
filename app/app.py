import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ---------------- #
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #141e30, #243b55);
    color: white;
}

/* Card UI */
.card {
    background: rgba(255, 255, 255, 0.08);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Skill Tags */
.tag {
    display: inline-block;
    background: linear-gradient(45deg, #ff416c, #ff4b2b);
    padding: 6px 12px;
    border-radius: 12px;
    margin: 4px;
    color: white;
    font-size: 14px;
    font-weight: bold;
}

/* Titles */
h1, h2, h3 {
    color: #ffffff;
}

/* Progress bar */
div[data-testid="stProgressBar"] > div > div > div > div {
    background: linear-gradient(90deg, #00ffcc, #00c3ff);
}

/* Upload box */
section[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()

# ---------------- PDF PARSER ---------------- #
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
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
        results.append((job, float(score)))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:5]

# ---------------- SKILL EXTRACTION ---------------- #
skills_db = [
    "python", "java", "sql", "machine learning",
    "deep learning", "nlp", "html", "css",
    "javascript", "react", "node", "spring boot", "excel", "powerbi"
]

def extract_skills(text):
    text = text.lower()
    return [skill for skill in skills_db if skill in text]

# ---------------- SKILL GAP ---------------- #
def skill_gap(resume_skills, job_skills):
    return list(set(resume_skills) & set(job_skills)), list(set(job_skills) - set(resume_skills))

# ---------------- FEEDBACK ---------------- #
def generate_feedback(resume_skills, missing_skills, job):
    feedback = []

    if missing_skills:
        feedback.append(f"❗ Add these skills: {', '.join(missing_skills)}")

    feedback.append("📌 Add 2–3 strong projects related to this role")
    feedback.append("📄 Improve formatting & add measurable achievements")
    feedback.append("🚀 Add internships / real-world experience")

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
    jobs[4]: ["sql", "excel", "python", "powerbi"]
}

# ---------------- HEADER ---------------- #
st.title("🚀 AI Resume Analyzer")
st.caption("✨ Smart Resume → Job Matching + Skill Gap + Suggestions")

# ---------------- UPLOAD ---------------- #
uploaded_file = st.file_uploader("📤 Upload your Resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text(uploaded_file)

    # ---------------- PREVIEW ---------------- #
    st.markdown("## 📄 Resume Preview")
    st.markdown(f'<div class="card">{resume_text[:600]}</div>', unsafe_allow_html=True)

    # ---------------- MATCHING ---------------- #
    results = match_jobs(resume_text, jobs)

    st.markdown("## 🎯 Top Job Matches")

    for job, score in results:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(f"### 🔹 {job}")
        st.progress(score)
        st.markdown(f"**Match Score:** `{round(score * 100, 2)}%`")

        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- SKILLS ---------------- #
    resume_skills = extract_skills(resume_text)

    st.markdown("## 🧠 Extracted Skills")

    if resume_skills:
        tags = "".join([f'<span class="tag">{skill}</span>' for skill in resume_skills])
        st.markdown(tags, unsafe_allow_html=True)
    else:
        st.warning("No skills detected from resume")

    # ---------------- GAP + FEEDBACK ---------------- #
    st.markdown("## 📊 Skill Gap Analysis & Suggestions")

    for job, score in results:
        required = job_requirements.get(job, [])
        matched, missing = skill_gap(resume_skills, required)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(f"### 🔹 {job}")
        st.markdown(f"✅ **Matched Skills:** {matched}")
        st.markdown(f"❌ **Missing Skills:** {missing}")

        feedback = generate_feedback(resume_skills, missing, job)

        st.markdown("### 🤖 Suggestions")
        for f in feedback:
            st.write(f)

        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("👆 Upload your resume to get started")