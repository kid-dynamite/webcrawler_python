import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html


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

    def test_get_heading_html_h1(self):
        html =  """<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
    """
        self.assertEqual(get_heading_from_html(html), "Welcome to Boot.dev")

    def test_get_heading_html_h2(self):
        html =  """<html>
  <body>
    <h2>Welcome to Boot.dev</h2>
    <main>
      <p>Learn to code by building real projects.</p>
    """
        self.assertEqual(get_heading_from_html(html), "Welcome to Boot.dev")

    def test_get_heading_html_empty(self):
        html =  """<html>
  <body>
    <p>Welcome to Boot.dev</p>
    <main>
      <p>Learn to code by building real projects.</p>
    """
        self.assertEqual(get_heading_from_html(html), "")

    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)


    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_multi(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
                <p>Main paragraph.-1</p>
                <p>Main paragraph.-2</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                Main paragraph.
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty(self):
        input_body = """<html><body>
            Outside paragraph.
            <main>
                Main paragraph.
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    

    

if __name__ == "__main__":
    unittest.main()