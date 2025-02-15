import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
sys.path.append(str(project_root))

from wikipedia_scraper import get_article_page, collect_article_texts, count_words, ArticleTitleNotFoundError

class TestWikipediaScraper(unittest.TestCase):

    def create_magic_mock_page(self, exists=True, title="Dummy Title", text="dummy text", links=[]):
        mock_wiki_page = MagicMock()
        mock_wiki_page.exists.return_value = exists
        mock_wiki_page.title = title
        mock_wiki_page.text = text
        mock_wiki_page.links.keys.return_value = links
        return mock_wiki_page

    @patch("wikipedia_scraper.wikipediaapi.Wikipedia.page")
    def test_get_article_page_valid(self, mock_page):
        mock_wiki_page = self.create_magic_mock_page()
        mock_page.return_value = mock_wiki_page

        result = get_article_page("Dummy Title")

        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Dummy Title")
        self.assertEqual(result.text, "dummy text")

    @patch("wikipedia_scraper.wikipediaapi.Wikipedia.page")
    def test_get_article_page_invalid(self, mock_page):
        mock_wiki_page = self.create_magic_mock_page(exists=False)
        mock_page.return_value = mock_wiki_page

        with self.assertRaises(ArticleTitleNotFoundError):
            get_article_page("Dummy Title")
    
    @patch("wikipedia_scraper.get_article_page")
    def test_collect_article_texts(self, mock_article_page):
        mock_page = self.create_magic_mock_page()
        mock_article_page.return_value = mock_page

        result = collect_article_texts("Dummy Title", 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "dummy text")
        mock_article_page.assert_called_once()

    @patch("wikipedia_scraper.get_article_page")
    def test_collect_article_texts_multiple_depths(self, mock_article_page):
        mock_page_1 = self.create_magic_mock_page(title="Dummy Title 1", text="Dummy Text 1", links=["Dummy Title 2"])
        mock_page_2 = self.create_magic_mock_page(title="Dummy Title 2", text="Dummy Text 2", links=["Dummy Title 3"])

        def side_effect(title):
            if title == "Dummy Title 1":
                return mock_page_1
            else:
                return mock_page_2
            
        mock_article_page.side_effect = side_effect

        result = collect_article_texts("Dummy Title 1", 1)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "Dummy Text 1")
        self.assertEqual(result[1], "Dummy Text 2")
        self.assertEqual(mock_article_page.call_count, 2)

    def test_count_words(self):
        result = count_words(["Dummy text."])
        self.assertEqual({"dummy":(1, 50.0), "text":(1,50.0)}, result)

    def test_count_words_with_ignore_list(self):
        result = count_words(["Dummy text."], "dummy")
        self.assertEqual({"text":(1,100.0)}, result)


if __name__ == "__main__":
    unittest.main()