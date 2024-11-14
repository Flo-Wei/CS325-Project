import logging
from LLM import OllamaLLM
from OutputParser import OutputParser

def main(ollama_address:str, model_name:str, log_level:str="WARNING"):
    # logging
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    


    llm = OllamaLLM(
        host_address=ollama_address,
        model_name=model_name
    )


    parser = OutputParser(
        valid_responses={
            "positive": {"positive", "good", "great", "excellent", "fantastic", "wonderful", "superb", "awesome", "favorable", "happy", "satisfied", "pleased"},
            "negative": {"negative", "bad", "terrible", "awful", "poor", "horrible", "dismal", "unhappy", "dissatisfied", "sad", "miserable", "displeased", "frustrating", "depressing"},
            "neutral": {"neutral", "okay", "average", "mediocre", "indifferent", "fair", "so-so", "unremarkable", "balanced", "nonchalant"}
            },
        debug=True
    )


if __name__ == "__main__":

    main(
        ollama_address="http://192.168.100.8:11434",
        model_name="llama3.2:1b",
        log_level="INFO"
    )