import os
import unittest
import requests
from flask import jsonify


class ChatServiceTest(unittest.TestCase):
    def test_chat_with_valid_prompt(self):
        prompt = "Hello"
        response = requests.get(self.url + f"?prompt={prompt}")
        assert response.status_code == 200
        response_text = response.json().get("response", "")
        assert response_text != ""
        assert "error" not in response_text.lower()
        assert "exception" not in response_text.lower()
        assert "traceback" not in response_text.lower()

    def test_chat_with_missing_prompt(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 400)
        response_text = response.json().get("error", "")
        self.assertIsNotNone(response_text, "Response text is empty")
        self.assertIn("Prompt parameter is missing", response_text, "Error message not found in response text")


    def test_chat_with_invalid_prompt(self):
        prompt = {"prompt": "How are you doing today?"}
        response = requests.get(self.url, params=prompt)
        print(response.status_code)
        assert response.status_code == 500
        response_text = response.json().get("error", "")
        assert response_text != ""


if __name__ == '__main__':
    unittest.main()
