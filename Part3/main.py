# CS325 Project - Part 3
# by Florian Weigelt
#
#   main code file
#
# This is the main python file. It combines combines webscraping, sentiment analysis, 
# output parsing and displaying the data.

import logging
from code.LLM import OllamaLLM
from code.OutputParser import OutputParser
from code.webscraping import ReviewScraper
from code.utils import plot_sentiment_counter, load_input_file, save_data

def main(input_file:str, reviews_file:str, ollama_address:str, model_name:str, log_level:str="WARNING", max_review_pages:int=None):
    # logging configuration
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.getLogger("httpx").propagate = False    # disable httpx logging


    # Class initializations
    scraper = ReviewScraper()
    llm = OllamaLLM(host_address=ollama_address, model_name=model_name)
    parser = OutputParser()


    # reading input file
    items, prompt_template = load_input_file(input_file)
    # items = items[:2]
    logging.info(f"{len(items)} Products found")
     

    # Web scraping
    logging.debug("start webscraping...")
    for product in items:   # scrape each item in the input file
        scraper.scrape_reviews(product)
    save_data(scraper.get_all_item_reviews(), reviews_file)     # save reviews to output file
    

    for product in items:
        # Sentiment Analysis
        responses = llm.do_sentiment_analysis(product["reviews"], prompt_template, verbose=True)
        responses = [response["response"] for response in responses]

        # parsing responses
        parser.parse_responses(responses, product["name"])

    # Displaying Count
    plot_sentiment_counter(parser.get_count())



if __name__ == "__main__":

    main(
        input_file=r"Part3\review_files\input_file.json",
        reviews_file=r"Part3\review_files\reviews_file.json",
        ollama_address="http://192.168.100.8:11434",
        model_name="llama3.2:1b",
        log_level="INFO",
        max_review_pages=None
    )