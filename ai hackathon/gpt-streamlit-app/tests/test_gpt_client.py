import pytest
from src.api.gpt_client import GPTClient

def test_set_api_key():
    client = GPTClient()
    client.set_api_key("test_api_key")
    assert client.api_key == "test_api_key"

def test_get_response(mocker):
    client = GPTClient()
    client.set_api_key("test_api_key")
    
    mock_response = {"choices": [{"text": "Hello, world!"}]}
    mocker.patch('src.api.gpt_client.requests.post', return_value=mock_response)
    
    response = client.get_response("Hello")
    assert response == "Hello, world!"

def test_get_response_no_api_key():
    client = GPTClient()
    response = client.get_response("Hello")
    assert response == "API key is not set."