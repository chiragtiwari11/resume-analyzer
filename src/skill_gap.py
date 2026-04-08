def skill_gap(resume_skills, job_skills):
    resume_set = set(resume_skills)
    job_set = set(job_skills)

    matched = list(resume_set & job_set)
    missing = list(job_set - resume_set)

    return matched, missing