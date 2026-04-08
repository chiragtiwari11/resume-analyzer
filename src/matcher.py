from sklearn.metrics.pairwise import cosine_similarity
from src.embedder import get_embedding

def match_jobs(resume_text, jobs):
    resume_emb = get_embedding(resume_text)

    results = []

    for job in jobs:
        job_emb = get_embedding(job)
        score = cosine_similarity([resume_emb], [job_emb])[0][0]
        results.append((job, score))

    # sort by best match
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:5]