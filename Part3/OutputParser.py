from collections import Counter
from fuzzywuzzy import fuzz
import logging

class OutputParser:
    def __init__(self, valid_responses:set={"positive", "negative", "neutral"}, threshold:int=80, debug:bool=False):
        self.threshold = self._validate_threshold(threshold)
        self.debug = debug
        self.valid_responses = valid_responses

        self.global_counter = Counter({response: 0 for response in self.valid_responses})
        self.global_counter["other"] = 0

        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)
    
    def _validate_threshold(self, threshold):
        if 0 <= threshold <= 100:
            return threshold
        else:
            raise ValueError("Threshold must be between 0 and 100")
        
    def _normalize_response(self, response):
        return response.strip().lower()

    def _find_matches(self, normalized_response):
        return [valid for valid in self.valid_responses if fuzz.partial_ratio(valid, normalized_response) > self.threshold]

    def update_counter(self, counter, original_response, key, match_type):
        counter[key] += 1
        logging.debug(f"{original_response}: {key} ({match_type})")

    def get_count(self):
        return self.global_counter

    def parse_responses(self, responses):
        local_counter = Counter({response: 0 for response in self.valid_responses})
        local_counter["other"] = 0

        for response in responses:
            normalized_response = self._normalize_response(response)

            # Check for exact match first
            for category, synonyms in self.valid_responses.items():
                if normalized_response == category:
                    self.update_counter(local_counter, response, category, "exact match")
                    break
            else:
                # Check for synonym match
                for category, synonyms in self.valid_responses.items():
                    if normalized_response in synonyms:
                        self.update_counter(local_counter, response, category, "synonym match")
                        break
                else:
                    # Check for partial keyword match using fuzzywuzzy
                    matches = self._find_matches(normalized_response)
                    
                    if len(matches) == 1:
                        self.update_counter(local_counter, response, matches[0], "partial keyword match")
                    else:
                        # If no suitable match or multiple matches found, classify as "other"
                        self.update_counter(local_counter, response, "other", "no or multiple matches")

        self.global_counter += local_counter
        return local_counter
    
    

if __name__ == "__main__":

    parser = OutputParser(
        valid_responses={
            "positive": {"positive", "good", "great", "excellent", "fantastic", "wonderful", "superb", "awesome", "favorable", "happy", "satisfied", "pleased"},
            "negative": {"negative", "bad", "terrible", "awful", "poor", "horrible", "dismal", "unhappy", "dissatisfied", "sad", "miserable", "displeased", "frustrating", "depressing"},
            "neutral": {"neutral", "okay", "average", "mediocre", "indifferent", "fair", "so-so", "unremarkable", "balanced", "nonchalant"}
            },
        debug=True
    )

    responses = [
        "Positive", "negative", "Neutral", "PosITIVE",
        "negative feedback", "Absolutely neutral", "NEGATIVE",
        "something else", "positve", "negetive",  # Typos
        "Totally positive", "Very negative experience", "Mildly negative", 
        "Good", "Bad", "Okay", "Super positive", "Neg vibes",
        "Positive and negative at the same time", "neutral but leaning towards negative",
        "Positivo", "Negativ", "Neutre",
        "Banana", "Football game was exciting", "Lorem ipsum dolor sit amet",
        "", "   ", "Negative    ", "   positive   ",
        "Pos", "Neg", "Neut",
        "The battery has a positive terminal.", "This is a negative charge.",
        "Neutral colors are my favorite.", "positive123", "negative456"
    ]


    count = parser.parse_responses(responses)
    print(count)