# 🚀 AI Resume Analyzer & Job Matcher

## 📌 Overview
AI-powered Resume Analyzer that evaluates resumes, extracts skills, matches them with relevant job roles, and provides improvement suggestions using NLP and Machine Learning.

---

## 🧠 Features

- 📄 Resume Upload (PDF)
- 🤖 BERT-based Semantic Job Matching
- 🧠 Skill Extraction from Resume
- 📊 Skill Gap Analysis (Matched vs Missing Skills)
- 🤖 AI-based Resume Improvement Suggestions
- 📈 Match Score Visualization
- 🌐 Real-world Job Role Simulation

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers (BERT)
- Scikit-learn
- PyPDF2

---

## ⚙️ How It Works

1. Upload resume (PDF)
2. Extract text using PDF parser
3. Generate embeddings using BERT
4. Compare with job descriptions using cosine similarity
5. Extract skills from resume
6. Identify missing skills for each job role
7. Provide suggestions to improve resume

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app/app.py 