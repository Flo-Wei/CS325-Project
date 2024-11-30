import pytest
from unittest.mock import patch, MagicMock
from LLM import OllamaLLM
from httpx import ConnectError
from ollama import ResponseError

# ----------------- Test Initialization ------------------------- #
def test_init_success():
    with patch("LLM.ollama.Client") as mock_client:
        mock_client.return_value = MagicMock()
        llm = OllamaLLM(host_address="localhost", model_name="phi3:3.8b")
        assert llm.host == "localhost"
        assert llm.model == "phi3:3.8b"
        assert llm.client == mock_client.return_value

def test_init_invalid_arguments():
    # check if host address is string
    with pytest.raises(AssertionError):
        OllamaLLM(host_address=1234, model_name="phi3:3.8b")
    # check if model name is string
    with pytest.raises(AssertionError):
        OllamaLLM(host_address="localhost", model_name=1234)


# --------------- Test Function _check_model -------------------- #
# Test `_check_model`
@patch("LLM.ollama.Client")
def test_check_model_exists(mock_client):
    # make ollama.show() output that the model exists
    mock_client.return_value.show.return_value = {"name": "phi3:3.8b"}  

    # assert that ollama.show() was called with the correct model
    llm = OllamaLLM(host_address="localhost", model_name="phi3:3.8b")
    mock_client.return_value.show.assert_called_with("phi3:3.8b") 

@patch("LLM.input", return_value="y")   # user input = "y"
@patch("LLM.ollama.Client")
@patch("LLM.OllamaLLM.download_model")
def test_check_model_download(mock_download_model, mock_client, mock_input):
    # mock a not found model
    mock_client.return_value.show.side_effect = MagicMock(side_effect=ResponseError("Not Found", status_code=404))
    llm = OllamaLLM(host_address="localhost", model_name="phi3:3.8b")
    # assert that download was correctly called
    mock_download_model.assert_called_once_with("phi3:3.8b", verbose=True)

@patch("LLM.ollama.Client")
def test_check_model_connection_error(mock_client):
    # simulate an unreachable host
    mock_client.return_value.show.side_effect = MagicMock(side_effect=ConnectError("Connection failed"))
    with pytest.raises(ConnectionError):
        OllamaLLM(host_address="localhost", model_name="phi3:3.8b")


# --------------- Test Function download_model -------------------- #
@patch("LLM.ollama.Client")
def test_download_model(mock_client):
    llm = OllamaLLM(host_address="localhost", model_name="phi3:3.8b")
    llm.download_model("phi3:3.8b", verbose=False)
    # assert that download_model() was called correctly
    mock_client.return_value.pull.assert_called_once_with("phi3:3.8b")


# --------------- Test Function do_sentiment_analysis -------------------- #
@patch("LLM.ollama.Client")
def test_do_sentiment_analysis(mock_client):
    # mock an api response
    mock_client.return_value.generate.side_effect = ["Positive", "Negative"]
    # initialize llm and review list
    llm = OllamaLLM(host_address="localhost", model_name="phi3:3.8b")
    reviews = ["Review 1", "Review 2"]
    result = llm.do_sentiment_analysis(reviews, "Analyze: {review}", verbose=False)

    assert result == ["Positive", "Negative"]                           # assert correct outputs
    assert mock_client.return_value.generate.call_count == len(reviews) # assert correct output length
