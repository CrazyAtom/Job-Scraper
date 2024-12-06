from bs4 import BeautifulSoup
from util.common import make_request

def scrape_page(url):
    print("Requesting", url)
    response = make_request(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_rows = soup.find_all("tr", class_="table_row")
    results = []
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
                "link": f"https://web3.career{job_row.a['href']}",
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