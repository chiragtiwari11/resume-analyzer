import requests
from bs4 import BeautifulSoup

def get_jobs():
    url = "https://in.indeed.com/jobs?q=software+developer"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.find_all("h2"):
        title = job.text.strip()
        if title:
            jobs.append(title)

    return jobs[:10]
