from requests import get
from bs4 import BeautifulSoup

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

def scrape_page(url):
  print("Requesting", url)
  response = get(url, headers=headers)
  if response.status_code != 200:
    print(f"Failed to retrieve the page: {response.status_code}")
  else:
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find("ul", class_="jobs-list-items").find_all("li")
    results = []
    for job in jobs:
      meta = job.find("div", class_="bjs-jlid__meta").find_all("a")
      if not meta or len(meta) < 2:
        continue
      title, company = meta
      job_data = {
        "company": company.string.replace(",", " "),
        "location": "",
        "position": title.string.replace(",", " "),
        "link": title["href"],
      }
      results.append(job_data)
    return results

def get_page_count(url):
  response = get(url, headers=headers)
  if response.status_code != 200:
    print(f"Failed to retrieve the page: {response.status_code}")
  else:
    soup = BeautifulSoup(response.content, "html.parser")
    if soup.find("ul", class_="bsj-nav") is None:
      return 0
    else:
      return len(soup.find("ul", class_="bsj-nav").find_all(class_="page-numbers")[0:-1])

def extract_jobs(keyword):
  base_url = "https://berlinstartupjobs.com/skill-areas/"
  pages = get_page_count(f"{base_url}{keyword}")
  results = []
  if pages == 0:
    results.extend(scrape_page(f"{base_url}{keyword}"))
  else:
    print("Found", pages, "pages")
    for x in range(pages):
      results.extend(scrape_page(f"{base_url}{keyword}/page/{x+1}/"))
  return results