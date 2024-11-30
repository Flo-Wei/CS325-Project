import pytest
from OutputParser import OutputParser

# Test if init works
def test_init_valid():
    parser = OutputParser(valid_responses={"positive":"good", "negative":"bad", "neutral":"so-so"}, threshold=80)
    assert parser.threshold == 80
    assert parser.valid_responses == {"positive":"good", "negative":"bad", "neutral":"so-so"}
    assert parser.global_counter == {}

# test invalid thresholds
def test_init_invalid_threshold():
    with pytest.raises(ValueError):
        OutputParser(threshold=120)
    with pytest.raises(ValueError):
        OutputParser(threshold=-10)

# test word normalization
def test_normalize_response():
    parser = OutputParser()
    assert parser._normalize_response(" Positive ") == "positive"
    assert parser._normalize_response("NEUTRAL") == "neutral"
    assert parser._normalize_response("   Negative   ") == "negative"

# test match finding function
def test_find_matches():
    parser = OutputParser()
    matches = parser._find_matches("positive")
    assert matches == ["positive"]
    matches = parser._find_matches("negativ")   # typo here
    assert matches == ["negative"]
    matches = parser._find_matches("unknown")
    assert matches == []

# test counter update
def test_update_counter():
    parser = OutputParser()
    local_counter = {"positive": 0, "negative": 0, "neutral": 0, "other": 0}
    parser.update_counter(local_counter, "Positive", "positive", "exact match")
    assert local_counter["positive"] == 1
    parser.update_counter(local_counter, "unknown", "other", "no match")
    assert local_counter["other"] == 1

# test respones parsing
def test_parse_responses():
    parser = OutputParser()

    responses = ["Positive", "negative", "neutral", "bad feedback", "Great", "Unknown response"]
    count = parser.parse_responses(responses)
    assert count["positive"] == 2
    assert count["negative"] == 2
    assert count["neutral"] == 1
    assert count["other"] == 1

# test product name inclution
def test_parse_responses_with_product_name():
    parser = OutputParser()

    responses = ["Positive", "neutral", "bad feedback", "something else"]
    count = parser.parse_responses(responses, product_name="TestProduct")
    assert parser.global_counter["TestProduct"] == count
    assert count["positive"] == 1
    assert count["negative"] == 1
    assert count["neutral"] == 1
    assert count["other"] == 1

