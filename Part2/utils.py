import re
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


class URL_Ebay:
    """
    This class handles eBay links and can return specific pages of the review page.
    """
    def __init__(self, url):
        self.url = url
        self.product_name = None
        self.offer_code = None
        self.parse_url()

    def parse_url(self):
        # URL Format:
        # https://www.ebay.com/urw/<product_name>/product-reviews/<offer_code>?pgn=<page>
        pattern = r"https://www\.ebay\.com/urw/(?P<product_name>[^/]+)/product-reviews/(?P<offer_code>[^/]+)"
        match = re.match(pattern, self.url)     # use regex to find variable parts of the url
        if match:
            self.product_name = match.group('product_name')
            self.offer_code = match.group('offer_code')
    
    def get_review_page(self, page_number:int):
        # return the link to the review page at a speciefied page number
        return f"https://www.ebay.com/urw/{self.product_name}/product-reviews/{self.offer_code}?pgn={page_number}"


def load_items(file_path:str):
    # loads item names and links from json file 
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data["items"]    
    
def save_data(data, file_path):
    # saves item names, links and reviews to json file
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def scrape_reviews(url: str):
    """
    This function takes the URL of a eBay review Page and 
    scrapes the title and text for each review on the page.
    """
    try:
        ua = UserAgent()                            # user agent object
        headers = {
            'User-Agent': ua.random,                # generate random useragent to cofuse bot protection systems
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',    # also use as many of these headers to seem like a 
            'Accept-Encoding': 'gzip, deflate, br', # real browser instead of a bot.
            'Connection': 'keep-alive',             
            'Referer': 'https://www.ebay.com/',     # Doing scraping without all these headers
            'Upgrade-Insecure-Requests': '1',       # leads to an Error 503 on eBay
            'DNT': '1', 
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        response = requests.get(url, headers=headers)   # send GET request to url
        if response.status_code != 200:                 # check if the equest was successful
            print(f"Failed to fetch URL: {url} with status code: {response.status_code}")
            return response

        soup = BeautifulSoup(response.content, 'html.parser')       # initialise parser object with bs4 
        review_sections = soup.find_all('div', {'class': 'ebay-review-section-r'})  # find all review calsses

        reviews = []
        for section in review_sections:                                             # for each review div
            title = section.find('h3', {'class': 'review-item-title'})              # get the title
            review_text = section.find('p', {'class': 'review-item-content'})       # and the review body
            if title and review_text:                                               # and if both are found
                reviews.append(f'{title.text.strip()}: {review_text.text.strip()}') # append their text into a string

        if soup.find(string="Sorry, no reviews match your current selections."):    # if there are no more reviews
            raise IndexError("This page has no reviews.")                           # raise error because this is the last page
        
        return reviews
    
    except requests.RequestException as e:                          # except all errers from the requests
        print(f"Error occurred while scraping {url}: {str(e)}")
        return []

