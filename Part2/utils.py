import re
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


class URL_Ebay:
    def __init__(self, url):
        self.url = url
        self.product_name = None
        self.offer_code = None
        self.parse_url()

    def parse_url(self):
        # URL Format:
        # https://www.ebay.com/urw/<product_name>/product-reviews/<offer_code>?pgn=<page>
        pattern = r"https://www\.ebay\.com/urw/(?P<product_name>[^/]+)/product-reviews/(?P<offer_code>[^/]+)"
        match = re.match(pattern, self.url)
        if match:
            self.product_name = match.group('product_name')
            self.offer_code = match.group('offer_code')
    
    def get_review_page(self, page_number:int):
        return f"https://www.ebay.com/urw/{self.product_name}/product-reviews/{self.offer_code}?pgn={page_number}"


def load_items(file_path:str):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data["items"]    


def scrape_reviews(url):
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.ebay.com/',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch URL: {url} with status code: {response.status_code}")
            return response

        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 'ebay-review-section-r'})

        if soup.find(string="Sorry, no reviews match your current selections."):
            raise IndexError("This page has no reviews.")
        
        return [review.get_text(strip=True) for review in reviews]
    
    except requests.RequestException as e:
        print(f"Error occurred while scraping {url}: {str(e)}")
        return []











if __name__ == "__main__":
    # url = "https://www.amazon.com/MSI-GeForce-RTX-3060-12G/product-reviews/B08WPRMVWB/"
    # url_parser = URL_Amazon(url)
    # print(url)
    # print("Product Name:", url_parser.product_name)
    # print("Offer Code:", url_parser.offer_code)
    # print(url_parser.get_review_page(3))

    path = r"Part2\prodcts.json"

    data = load_items(path)
