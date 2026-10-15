import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_teacher(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_strip_query(self):
        self.assertEqual(
            normalize_url("https://boot.dev/blog/path?search=python&page=2"),
            "boot.dev/blog/path"
        )

    def test_normalize_url_sub(self):
        self.assertEqual(
            normalize_url("https://sub.domain.boot.dev/courses/"),
            "sub.domain.boot.dev/courses"
        )

    

if __name__ == "__main__":
    unittest.main()