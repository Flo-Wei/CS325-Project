import re


class URL_Amazon:
    def __init__(self, url):
        self.url = url
        self.product_name = None
        self.offer_code = None
        self.parse_url()

    def parse_url(self):
        # URL Format:
        # https://www.amazon.com/<product_name>/<page_view>/<offer_code>/?pageNumber=<page>
        # product name: name of the product search e.g RTX 2060
        # page_view: "dp" (actual product page), "product-reviews" (review page)
        # offer_code: individual ID of the offer
        # page: number of review page
        pattern = r"https://www\.amazon\.com/(?P<product_name>[^/]+)/[^/]+/(?P<offer_code>[^/]+)/?"
        match = re.match(pattern, self.url)
        if match:
            self.product_name = match.group('product_name')
            self.offer_code = match.group('offer_code')
    
    def get_review_page(self, page_number:int):
        return f"https://www.amazon.com/{self.product_name}/product-reviews/{self.offer_code}/?pageNumber={page_number}"













if __name__ == "__main__":
    url = "https://www.amazon.com/MSI-GeForce-RTX-3060-12G/product-reviews/B08WPRMVWB/"
    url_parser = URL_Amazon(url)
    print(url)
    print("Product Name:", url_parser.product_name)
    print("Offer Code:", url_parser.offer_code)
    print(url_parser.get_review_page(3))
