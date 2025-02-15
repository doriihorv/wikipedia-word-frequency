import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from main import app


class TestFastAPIEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch("main.collect_article_texts")
    def test_word_frequency_endpoint(self, mock_collect_texts):
        mock_collect_texts.return_value = ["Dummy text."]

        response = self.client.get("/word-frequency", params={"article": "Python", "depth": 0})

        expected_response = {'dummy': [1, 50.0], 'text': [1, 50.0]}
        self.assertEqual(response.json(), expected_response)

    @patch("main.collect_article_texts")
    def test_keyword_frequency_endpoint(self, mock_collect_texts):
        mock_collect_texts.return_value = ["Dummy text."]

        request_data = {
            "article": "Python",
            "depth": 1,
            "ignore_list": ["this"],
            "percentile": 40
        }

        response = self.client.post("/keywords", json=request_data)

        expected_response = {'dummy': [1, 50.0], 'text': [1, 50.0]}
        self.assertEqual(response.json(), expected_response)

if __name__ == "__main__":
    unittest.main()
