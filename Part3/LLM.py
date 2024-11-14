import ollama
import logging
from httpx import ConnectError
from tqdm import tqdm


class OllamaLLM():
    def __init__(self, host_address:str=None, model_name:str="phi3:3.8b") -> None:
        logging.info("Initializing LLM...")
        assert isinstance(host_address, str)
        assert isinstance(model_name, str)

        self.host = host_address
        self.model = model_name

        self.client = ollama.Client(host=self.host)
        
        self._check_model()


    def _check_model(self):
        try:
            model_data = self.client.show(self.model)
        except ConnectError as e:
            logging.error(f"Could not connect to Ollama host: {e}")
            raise ConnectionError(f"Could not connect to Ollama host: {e}")
        except ollama.ResponseError as e:
            print(e)
            logging.warning(f"{self.model} could not be found.")
            if e.status_code == 404:
                user_input = input(f"Do you want to download {self.model} from the repository? (Y/n)").lower()
                if user_input == "yes" or user_input == "y":
                    logging.info(f"Pulling {self.model}...")
                    self.download_model(self.model, verbose=True)


    def download_model(self, model_name, verbose=False):
        assert isinstance(model_name, str)
        assert isinstance(verbose, bool)

        if verbose:
            current_digest, bars = '', {}
            for progress in self.client.pull(self.model, stream=True):
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
        else:
            self.client.pull(model_name)


    def do_sentiment_analysis(self, reviews:list, prompt_template:str, verbose=True):
        logging.debug(f"doing sentiment analysis on {len(reviews)} reviews")
        assert isinstance(reviews, list)
        assert isinstance(prompt_template, str)

        sentiments = []
        reviews = reviews[:15]

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
    from utils import plot_response_durations
    
    with open(r"C:\Users\flori\OneDrive\Studium\AI Bachelor\Courses\5.Semester\CS 325 - Software Engineering\Project\Part2\reviews.json", 'r') as file:
        data = json.load(file) 


    prompt_template = 'Analyze the sentiment of the following product review and respond with *only* the word "positive," "neutral," or "negative" based on the overall tone. Do not include any additional text.\n\n{review}'

    res = llm.do_sentiment_analysis(data[0]["reviews"], prompt_template, verbose=True)

    plot_response_durations(res)
    