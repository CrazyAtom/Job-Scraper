from requests import get

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

def make_request(url):
    try:
        response = get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error occurred while making request to {url}: {e}")
        return None