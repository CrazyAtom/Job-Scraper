from bs4 import BeautifulSoup
from util.common import make_request

def scrape_page(url):
    print("Requesting", url)
    response = make_request(url)
    if not response:
      return []

    soup = BeautifulSoup(response.content, "html.parser")
    jobs_list = soup.find("ul", class_="jobs-list-items")
    if not jobs_list:
        print(f"No jobs list found on the page: {url}")
        return []

    jobs = jobs_list.find_all("li")
    results = []
    for job in jobs:
        try:
          meta = job.find("div", class_="bjs-jlid__meta")
          if not meta:
            continue
          links = meta.find_all("a")
          if len(links) < 2:
            continue
          title, company = links
          job_data = {
              "company": company.string.strip().replace(",", " "),
              "location": "",
              "position": title.string.strip().replace(",", " "),
              "link": title["href"],
          }
          results.append(job_data)
        except Exception as e:
           print(f"Error parsing job: {e}")
    return results

def extract_jobs(keyword):
  base_url = "https://berlinstartupjobs.com/skill-areas/"
  return scrape_page(f"{base_url}{keyword}")