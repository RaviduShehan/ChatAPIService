import os
import tempfile
import pytest
import json
import config
import sys
sys.path.append('../src')
from src.chat import app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])



def test_chat_invalid_prompt(client):
    response = client.get('/')
    assert response.status_code == 400


def test_chat_valid_prompt(client):
    response = client.get('/chat?prompt=Hi')
    assert response.status_code == 200
    assert 'response' in json.loads(response.get_data(as_text=True))


def test_chat_server_error(client, monkeypatch):
    def mock_create(*args, **kwargs):
        raise Exception('OpenAI API error')

    monkeypatch.setattr(app.openai.Completion, 'create', mock_create)

    response = client.get('/?prompt=Hello')
    assert response.status_code == 500
    assert 'error' in json.loads(response.get_data(as_text=True))


