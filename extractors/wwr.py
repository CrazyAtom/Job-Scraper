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
        print("Can't request website")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                try:
                    ad = post.find("div", class_="highlight-bar--ad")
                    if ad == None:
                        anchors = post.find_all('a')
                        anchor = anchors[1]
                        link = anchor["href"]
                        company, kind, region = anchor.find_all("span", class_="company")
                        title = anchor.find("span", class_="title")
                        job_data = {
                            "company": company.string.replace(",", " "),
                            "location": region.string.replace(",", " "),
                            "position": title.string.replace(",", " "),
                            "link": f"https://weworkremotely.com{link}",
                        }
                        results.append(job_data)
                except:
                    pass
        return results

def extract_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    return scrape_page(f"{base_url}{keyword}")
