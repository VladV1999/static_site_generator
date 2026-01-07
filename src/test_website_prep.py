import unittest

from website_prep import extract_title

class TestWebsitePrep(unittest.TestCase):
    def test_extract_title(self):
        title = "# Hello"
        self.assertEqual(
            extract_title(title),
            "Hello"
        )
    def test_extract_title_spaces(self):
        title = "#    Hello   "
        self.assertEqual(
            extract_title(title),
            "Hello"
        )