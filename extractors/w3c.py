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
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        job_rows = soup.find("tbody", class_="tbody").find_all('tr', class_='table_row')
        for job_row in job_rows:
            try:
                position_tag = job_row.find('h2', class_='fs-6')
                position = position_tag.text.strip() if position_tag else "N/A"
                company_tag = job_row.find('h3')
                company = company_tag.text.strip() if company_tag else "N/A"
                location_cells = job_row.find_all('td', class_='job-location-mobile')
                location = "N/A"
                for cell in location_cells:
                    location_links = cell.find_all('a')
                    if location_links:
                        location = ", ".join([link.text.strip() for link in location_links])
                    else:
                        location_text = cell.get_text(strip=True)
                        if location_text:
                            location = location_text
                            break

                job_data = {
                    "company": company,
                    "location": location,
                    "position": position,
                    "link": f"https://web3.career{job_row.a["href"]}",
                }
                results.append(job_data)
            except Exception as e:
                print(f"Error parsing job row: {e}")
        return results

def extract_jobs(keyword):
    base_url = "https://web3.career/"
    results = []
    for page in range(1, 6):
        results.extend(scrape_page(f"{base_url}{keyword}-jobs?page/{page}"))
    return results