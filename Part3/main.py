import logging
import json
from utils import plot_sentiment_counter
from LLM import OllamaLLM
from OutputParser import OutputParser

def main(input_file:str, ollama_address:str, model_name:str, log_level:str="WARNING"):
    # logging
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger("httpx").propagate = False

    # initializatioin
    llm = OllamaLLM(
        host_address=ollama_address,
        model_name=model_name
    )
    parser = OutputParser(
        valid_responses={
            "positive": {"positive", "good", "great", "excellent", "fantastic", "wonderful", "superb", "awesome", "favorable", "happy", "satisfied", "pleased"},
            "negative": {"negative", "bad", "terrible", "awful", "poor", "horrible", "dismal", "unhappy", "dissatisfied", "sad", "miserable", "displeased", "frustrating", "depressing"},
            "neutral": {"neutral", "okay", "average", "mediocre", "indifferent", "fair", "so-so", "unremarkable", "balanced", "nonchalant"}
            }
    )


    # Web scraping
    with open(input_file, 'r') as file:
        data = json.load(file) 
        data = data[:2]
        logging.info(f"{len(data)} Products found")
    
    for product in data:
        # Sentiment Analysis
        prompt_template = 'Analyze the sentiment of the following product review and respond with *only* the word "positive," "neutral," or "negative" based on the overall tone. Do not include any additional text.\n\n{review}'
        responses = llm.do_sentiment_analysis(product["reviews"], prompt_template, verbose=True)
        responses = [response["response"] for response in responses]

        # parsing responses
        parser.parse_responses(responses, product["name"])

    # Displaying Count
    plot_sentiment_counter(parser.get_count())



if __name__ == "__main__":

    main(
        input_file=r"C:\Users\flori\OneDrive\Studium\AI Bachelor\Courses\5.Semester\CS 325 - Software Engineering\Project\Part2\reviews.json",
        ollama_address="http://192.168.100.8:11434",
        model_name="llama3.2:1b",
        log_level="INFO"
    )