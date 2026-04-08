def generate_feedback(resume_skills, missing_skills, job):
    feedback = []

    if missing_skills:
        feedback.append(f"❗ Add these skills for {job}: {', '.join(missing_skills)}")

    if "projects" not in resume_skills:
        feedback.append("📌 Add more projects related to your target role")

    feedback.append("📄 Improve resume formatting and add measurable achievements")

    feedback.append("🚀 Include internships or real-world experience if possible")

    return feedback