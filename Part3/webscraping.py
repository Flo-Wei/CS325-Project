import re
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import logging

class URL_Ebay:
    """
    This class handles eBay links and can return specific pages of the review page.
    """
    def __init__(self, url):
        logging.debug(f"Initializing URL Handler URL={url}")
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
    

class ReviewScraper:
    def __init__(self, custom_headers:dict=None):
        self.headers = {
                'User-Agent': UserAgent().random,       # generate random useragent to confuse bot protection systems
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',    # also use as many of these headers to seem like a 
                'Accept-Encoding': 'gzip, deflate, br', # real browser instead of a bot.
                'Connection': 'keep-alive',             
                'Referer': 'https://www.ebay.com/',     # Doing scraping without all these headers
                'Upgrade-Insecure-Requests': '1',       # leads to an Error 503 on eBay
                'DNT': '1', 
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            } if not custom_headers else custom_headers
        
        self.all_item_reviews = []
        

    def scrape_reviews(self, item:dict, max_review_pages:int=None):
        if not max_review_pages:                                        # handle not defined max pages
            max_review_pages = float("inf")                             # none = inf

        logging.info(f"Scraping Item: {item['name']}")
        url_handler = URL_Ebay(item["link"])                            # initialize an url handler with the product link
        p = 1                                                           # set starting page number to 1

        reviews_total = []                                              # initialize list of reviews
        while p <= max_review_pages:                                    # go through all review pages
            url = url_handler.get_review_page(p)                        # get url of specific page
            html_response = self._scrape_html(url)                      # scrape html content
            reviews = self._clean_reviews(html_response)                # get review text from html

            if reviews:                                                 # extend total review list if page had reviews
                reviews_total.extend(reviews)
                logging.debug(f"{item['name']} -> Page {p}: {len(reviews)} reviews found")
                p += 1
            else:                                                       # otherwise leave the loop
                logging.debug(f"{item['name']} -> Page {p}: No more reviews found")
                break
        item['reviews'] = reviews_total
        self.all_item_reviews.append(item)
        return reviews_total                                            # add reviews to item dict
    
    def get_all_item_reviews(self):
        return self.all_item_reviews

    def _scrape_html(self, url):
        try:
            response = requests.get(url, headers=self.headers)   # send GET request to url
            logging.debug(f"request status code {response.status_code} for {url}")
            if response.status_code != 200:                 # check if the equest was successful
                logging.error(f"Failed to fetch URL: {url} with status code: {response.status_code}")
                return []
            return response
        except requests.RequestException as e:
            logging.error(f"Error occurred while scraping {url}: {str(e)}")
            return []

    def _clean_reviews(self, html_response):
        soup = BeautifulSoup(html_response.content, 'html.parser')                  # initialise parser object with bs4 
        
        if soup.find(string="Sorry, no reviews match your current selections."):    # if there are no more reviews
            return None                                                             # return None because this is the last page
        
        review_sections = soup.find_all('div', {'class': 'ebay-review-section-r'})  # find all review calsses

        reviews = []
        for section in review_sections:                                             # for each review div
            title = section.find('h3', {'class': 'review-item-title'})              # get the title
            review_text = section.find('p', {'class': 'review-item-content'})       # and the review body
            if title and review_text:                                               # and if both are found
                reviews.append(f'{title.text.strip()}: {review_text.text.strip()}') # append their text into a string

        return reviews


if __name__ == "__main__":
    from utils import load_input_file

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    scraper = ReviewScraper()

    items, _ = load_input_file(r"Part3/input_file.json")

    for item in items:
        scraper.scrape_reviews(item, 2)

    print(type(scraper.get_all_item_reviews()))
    print(len(scraper.get_all_item_reviews()))


