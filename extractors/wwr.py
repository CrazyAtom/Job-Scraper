from bs4 import BeautifulSoup
from util.common import make_request

def scrape_page(url):
    print("Requesting", url)
    response = make_request(url)
    if not response: return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs_list = soup.find_all('section', class_="jobs")
    if not jobs_list:
        print(f"No jobs list found on the page: {url}")
        return []

    results = []
    for job_section in jobs_list:
        job_posts = job_section.find_all('li')
        job_posts.pop(-1)
        for post in job_posts:
            try:
                ad = post.find("div", class_="highlight-bar--ad")
                if ad is None:
                    anchors = post.find_all('a')
                    if len(anchors) < 2:
                        continue
                    anchor = anchors[1]
                    link = anchor["href"]
                    company, kind, region = anchor.find_all("span", class_="company")
                    title = anchor.find("span", class_="title")
                    job_data = {
                        "company": company.string.strip().replace(",", " "),
                        "location": region.string.strip().replace(",", " "),
                        "position": title.string.strip().replace(",", " "),
                        "link": f"https://weworkremotely.com{link}",
                    }
                    results.append(job_data)
            except Exception as e:
                print(f"Error parsing job post: {e}")
                continue
    return results

def extract_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    return scrape_page(f"{base_url}{keyword}")
