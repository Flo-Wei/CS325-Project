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
    
def save_data(data, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


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
        review_sections = soup.find_all('div', {'class': 'ebay-review-section-r'})

        reviews = []
        for section in review_sections:
            title = section.find('h3', {'class': 'review-item-title'})
            review_text = section.find('p', {'class': 'review-item-content'})
            if title and review_text:
                reviews.append(f'{title.text.strip()}: {review_text.text.strip()}')

        if soup.find(string="Sorry, no reviews match your current selections."):
            raise IndexError("This page has no reviews.")
        
        return reviews
    
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
