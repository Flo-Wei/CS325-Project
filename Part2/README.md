# CS325 Project - Part 2 Web Scraping

The second part of the CS325 Poject fonuses on web scraping. I used python's `requests` library to ge the pure html data from the eBay review pages and then filterd for the review text using `Beautiful Soup`.

## Installation
1. **Clone the repository:**  
    ```bash 
    git clone https://github.com/Flo-Wei/CS325-Project.git
    cd CS325-Project/Part2
    ```
2. **Install dependencies:**  
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Prepare the Product list:**  
    Edit the `products.json` file and add the products names and URLs to the review pages for all the products you want to scrape.

    ```json
    {
        "items": [
            {
                "name": "Product Name",
                "link": "https://www.ebay.com/urw/..."
            },
        ]
    }

    ```
2. **Modify parameters:**  
    By default the cript uses the following default parameters:
    - `input_file`: Path to the JSON file containing product names and links.
    - `output_file`: Path where the scraped data will be saved.
    - `max_review_pages`(default:`None`): Maximum number of review pages to scrape per product.
    - `verbose`(default:`False`): If set to True, the script will print detailed logs.
    
    These parameters can be modifies within the `main.py` file.

3. **Run the script:**  
    You can execute the script by running the `main.py` file.
    ```python
    python main.py
    ```  


## Example Output  
The script ouputs the scraped reviews in json format to the speciefied file. Here is an Example of the structure:
```json
[
    {
        "name": "Product Name",
        "link": "https://www.ebay.com/urw/...",
        "reviews": [
            "Title 1: Review text 1...",
            "Title 2: Review text 2..."
        ]
    }
]
```