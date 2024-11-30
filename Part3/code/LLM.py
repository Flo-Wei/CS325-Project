# CS325 Project - Part 3
# by Florian Weigelt
#
#   LLM code file
#
# This is the LLM handler for an Ollama instance. 
# It can interact with ollama models and download them if nessecary.

import ollama
import logging
from httpx import ConnectError
from tqdm import tqdm


class OllamaLLM():
    """
    A class to handle a ollama instance and do sentiment analysis.
    """
    def __init__(self, host_address:str=None, model_name:str="phi3:3.8b") -> None:
        logging.info("Initializing LLM...")
        # checking augments
        assert isinstance(host_address, str)
        assert isinstance(model_name, str)

        self.host = host_address
        self.model = model_name

        # initializing ollama connection
        self.client = ollama.Client(host=self.host)
        
        # check if model is avaible in ollama
        self._check_model()


    def _check_model(self):
        """
        This method checks if a model is present in ollama by trying to view data about the model.
        """
        try:
            # tries showing model info
            model_data = self.client.show(self.model)
        except ConnectError as e:
            # if connection error is thrown
            # means that the ollama host is not reachable
            logging.error(f"Could not connect to Ollama host: {e}")
            raise ConnectionError(f"Could not connect to Ollama host: {e}")
        except ollama.ResponseError as e:
            # if ResponseError is thrown
            # ollama could not find info about the model
            print(e)
            logging.warning(f"{self.model} could not be found.")
            if e.status_code == 404:
                # status code 404 means that ollama does not have the model downloaded
                user_input = input(f"Do you want to download {self.model} from the repository? (Y/n)").lower()
                if user_input == "yes" or user_input == "y":
                    logging.info(f"Pulling {self.model}...")
                    self.download_model(self.model, verbose=True)


    def download_model(self, model_name, verbose=False):
        """
        This method downloads a model from the online ollama library to the ollama instance.
        """
        assert isinstance(model_name, str)
        assert isinstance(verbose, bool)

        if verbose: # verbose mode creates a progress bar
            current_digest, bars = '', {}
            for progress in self.client.pull(self.model, stream=True):  # sends pull as stream
                digest = progress.get('digest', '')
                if digest != current_digest and current_digest in bars:
                    bars[current_digest].close()
                if not digest:
                    print(progress.get('status'))
                    continue
                if digest not in bars and (total := progress.get('total')):
                    bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)
                if completed := progress.get('completed'):
                    bars[digest].update(completed - bars[digest].n)
                current_digest = digest
        else:   # non-verbose mode just sends a pull command to ollama
            self.client.pull(model_name)


    def do_sentiment_analysis(self, reviews:list, prompt_template:str, verbose=True, max_reviews:int=None):
        """
        This method does sentiment analysis for a list of reviews and returns a list of unprocessed sentiments
        """
        logging.debug(f"doing sentiment analysis on {len(reviews)} reviews")
        assert isinstance(reviews, list)
        assert isinstance(prompt_template, str)

        sentiments = []
        if max_reviews: # adds the ability to limit the maximum number of reviews to process
            assert isinstance(max_reviews, int)
            if max_reviews < len(reviews):
                reviews = reviews[:max_reviews]

        # use chat completoin with the prompt template for every review
        for review in tqdm(reviews, disable=not verbose, desc="progress"):
            result = self.client.generate(
                model=self.model,
                prompt=prompt_template.format(review=review)
            )
            sentiments.append(result)

        return sentiments



        




if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    llm = OllamaLLM(
    host_address="http://192.168.100.8:11434",
    model_name="llama3.2:1b"
    )

    import json
    from Part3.code.utils import plot_response_durations
    
    with open(r"C:\Users\flori\OneDrive\Studium\AI Bachelor\Courses\5.Semester\CS 325 - Software Engineering\Project\Part2\reviews.json", 'r') as file:
        data = json.load(file) 


    prompt_template = 'Analyze the sentiment of the following product review and respond with *only* the word "positive," "neutral," or "negative" based on the overall tone. Do not include any additional text.\n\n{review}'

    res = llm.do_sentiment_analysis(data[0]["reviews"], prompt_template, verbose=True)

    plot_response_durations(res)
    