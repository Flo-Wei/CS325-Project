from utils import URL_Ebay, load_items, scrape_reviews, save_data
import os


def main(input_file, output_file, max_review_pages=None, verbose=False):
    


    items = load_items(os.path.abspath(input_file))
    if verbose: print(f"Reading list... {len(items)} items found.") 

    if not max_review_pages:
        max_review_pages = float("inf")

    for item in items:
        if verbose: print(f"Scraping Item: {item['name']}")
        p = 1

        url_handler = URL_Ebay(item["link"])
        reviews_total = []
        while p <= max_review_pages:
            try:
                reviews = scrape_reviews(url_handler.get_review_page(p))
                if verbose: print(f"  Page {p}: {len(reviews)} reviews found")
            except IndexError:
                break
            reviews_total.extend(reviews)
            p += 1
        item["reviews"] = reviews_total
        if verbose: print()
    
    save_data(items, output_file)


if __name__ == "__main__":
    main(
        input_file = r"Part2/prodcts.json",
        output_file = r"Part2/reviews.json",
        max_review_pages = 2,
        verbose = True,
    )
    
