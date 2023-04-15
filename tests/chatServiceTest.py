import unittest
import requests
from flask import jsonify


class ChatServiceTest(unittest.TestCase):
    def setUp(self):
        self.url = "http://localhost:5001/chat"

    def test_chat_without_prompt(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_chat_with_prompt(self):
        prompt = "generic prompt text"
        expected_answer = ""
        response = requests.get(self.url + f"?prompt={prompt}")
        self.assertEqual(response.status_code, 200)
        response_text = response.json().get("text", "")
        self.assertIsNotNone(response_text, "Response text is empty")
        self.assertNotIn("error", response_text.lower(), "Error in response text")
        self.assertNotIn("exception", response_text.lower(), "Exception in response text")
        self.assertNotIn("traceback", response_text.lower(), "Traceback in response text")
        self.assertIn(expected_answer, response_text, "Expected answer not found in response text")


if __name__ == '__main__':
    unittest.main()
