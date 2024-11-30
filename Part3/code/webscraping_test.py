import pytest
from unittest.mock import patch, MagicMock
from webscraping import URL_Ebay, ReviewScraper
from requests import RequestException



# ----------------- Test Class URL_Ebay ------------------------- #
def test_parse_url_valid():
    url = "https://www.ebay.com/urw/sample-product/product-reviews/12345"
    handler = URL_Ebay(url)
    assert handler.product_name == "sample-product"
    assert handler.offer_code == "12345"

def test_parse_url_invalid():
    url = "https://www.example.com/some/other/url"
    handler = URL_Ebay(url)
    assert handler.product_name is None
    assert handler.offer_code is None

def test_get_review_page():
    url = "https://www.ebay.com/urw/sample-product/product-reviews/12345"
    handler = URL_Ebay(url)
    review_page_url = handler.get_review_page(2)
    expected_url = "https://www.ebay.com/urw/sample-product/product-reviews/12345?pgn=2"
    assert review_page_url == expected_url

def test_get_review_page_no_product_name_or_offer_code():
    url = "https://www.example.com/some/other/url"
    handler = URL_Ebay(url)
    review_page_url = handler.get_review_page(1)
    expected_url = "https://www.ebay.com/urw/None/product-reviews/None?pgn=1"
    assert review_page_url == expected_url


# ----------------- Test Class ReviewScraper -------------------- #
def test_init_custom_headers():
    custom_headers = {'User-Agent': 'custom-agent'}
    scraper = ReviewScraper(custom_headers=custom_headers)
    assert scraper.headers == custom_headers


@patch('webscraping.URL_Ebay')
@patch('webscraping.ReviewScraper._scrape_html')
@patch('webscraping.ReviewScraper._clean_reviews')
def test_scrape_reviews(mock_clean_reviews, mock_scrape_html, mock_url_ebay):
    # mock all the helper functions so no actual requests are sent
    mock_url_ebay.return_value.get_review_page.side_effect = lambda p: f"https://www.ebay.com/page/{p}"
    mock_scrape_html.return_value = MagicMock()
    mock_clean_reviews.side_effect = [["Review 1", "Review 2"], ["Review 3"], None]

    # initialize url and scraper
    item = {'name': 'Test Product', 'link': 'https://www.ebay.com/test'}
    scraper = ReviewScraper()
    reviews = scraper.scrape_reviews(item, max_review_pages=3)

    assert len(reviews) == 3                # 3 reviews expected in list
    assert "Review 1" in reviews            # correct review text expected in list
    assert item['reviews'] == reviews       # reviews are in item dictionary
    assert item in scraper.all_item_reviews # item is in global reviews list

@patch('webscraping.ReviewScraper._scrape_html')
@patch('webscraping.ReviewScraper._clean_reviews')
def test_scrape_reviews_no_reviews(mock_clean_reviews, mock_scrape_html):
    # mock all the helper functions so no actual requests are sent
    mock_scrape_html.return_value = MagicMock()
    mock_clean_reviews.return_value = None

    # initialize url and scraper
    item = {'name': 'Test Product', 'link': 'https://www.ebay.com/test'}
    scraper = ReviewScraper()
    reviews = scraper.scrape_reviews(item, max_review_pages=1)

    assert reviews == []            # review list is empty
    assert item['reviews'] == []    # no reviews in item dict

def test_get_all_item_reviews():
    scraper = ReviewScraper()
    scraper.all_item_reviews = [{'name': 'Test Product 1'}, {'name': 'Test Product 2'}]
    assert scraper.get_all_item_reviews() == [{'name': 'Test Product 1'}, {'name': 'Test Product 2'}]

@patch('webscraping.requests.get')
def test_scrape_html(mock_get):
    # mock a successful http GET request
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'<html></html>'
    mock_get.return_value = mock_response

    # initialize scraper
    scraper = ReviewScraper()
    response = scraper._scrape_html("https://www.ebay.com/test")

    assert response.status_code == 200          # correct status code
    assert response.content == b'<html></html>' # correct html content

@patch('webscraping.requests.get')
def test_scrape_html_error(mock_get):
    # simulate an html error when trying to scrape the html contnet
    mock_get.side_effect = RequestException("Request failed")

    scraper = ReviewScraper()
    response = scraper._scrape_html("https://www.ebay.com/test")
    assert response == []   # expect empty response list

def test_clean_reviews():
    # sample html snippet from ebay
    html_content = """
    <div class="ebay-review-section-r">
        <h3 class="review-item-title">Product 1 Title</h3>
        <p class="review-item-content">Product 1 Works perfectly!</p>
    </div>
    <div class="ebay-review-section-r">
        <h3 class="review-item-title">Product 2 Title</h3>
        <p class="review-item-content">Product 2 Works perfectly!</p>
    </div>
    """
    # mock a response that includes the html snippet
    mock_response = MagicMock()
    mock_response.content = html_content

    # cleans the html
    scraper = ReviewScraper()
    reviews = scraper._clean_reviews(mock_response)

    assert len(reviews) == 2    # expects 2 reviews
    assert reviews == [     	# expects correct format
        "Product 1 Title: Product 1 Works perfectly!",
        "Product 2 Title: Product 2 Works perfectly!"]

def test_clean_reviews_no_reviews():
    # mock a response that includes an empty review page
    html_content = "Sorry, no reviews match your current selections."
    mock_response = MagicMock()
    mock_response.content = html_content 

    scraper = ReviewScraper()
    reviews = scraper._clean_reviews(mock_response)

    assert reviews is None