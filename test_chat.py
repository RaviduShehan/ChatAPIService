from flask import Flask
import pytest

from src.chat import app

import os
import requests

def test_app():
    app_url = "http://34.132.224.27"
    response = requests.get(f'{app_url}/chat')
    assert response.status_code == 200
    assert 'expected-response' in response.text



# def test_chat_valid_prompt(client):
#     response = client.get('/chat?prompt=Hi')
#     assert response.status_code == 200
#     assert 'response' in json.loads(response.get_data(as_text=True))
#
#
# def test_chat_server_error(client, monkeypatch):
#     def mock_create(*args, **kwargs):
#         raise Exception('OpenAI API error')
#
#     monkeypatch.setattr(app.openai.Completion, 'create', mock_create)
#
#     response = client.get('/?prompt=Hello')
#     assert response.status_code == 500
#     assert 'error' in json.loads(response.get_data(as_text=True))


