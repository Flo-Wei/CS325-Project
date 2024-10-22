from utils import URL_Ebay, load_items, scrape_reviews, save_data
import os


def main(input_file: str, output_file: str, max_review_pages:int=None, verbose:bool=False):
    
    items = load_items(os.path.abspath(input_file))                     # load the items and links from input file
    if verbose: print(f"Reading list... {len(items)} items found.")     # print number of items to scrape

    if not max_review_pages:                                            # handle not defined max pages
        max_review_pages = float("inf")                                 # none = inf

    for item in items:                                                  # iterate through every item in the list
        if verbose: print(f"Scraping Item: {item['name']}")
        p = 1                                                           # set starting page number to 1

        url_handler = URL_Ebay(item["link"])                            # initialize an url handler with the product link
        reviews_total = []                                              # initialize list of reviews
        while p <= max_review_pages:                                    # go through all review pages
            try:
                reviews = scrape_reviews(url_handler.get_review_page(p))    # scrape reviews
                if verbose: print(f"  Page {p}: {len(reviews)} reviews found")  # print number of reviews found on page
            except IndexError:                                          # if there are no reviews on the page
                break                                                   # leave the loop 
            reviews_total.extend(reviews)                               # append page reviews to total review list
            p += 1                                                      # go to the next page
        item["reviews"] = reviews_total                                 # add reviews to item dict
        if verbose: print()
    
    save_data(items, output_file)                                       # save updated item dict as json to file


if __name__ == "__main__":
    main(
        input_file = r"Part2/prodcts.json",
        output_file = r"Part2/reviews.json",
        max_review_pages = 2,
        verbose = True,
    )
    
