import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html


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



class TestHTMLChunks(unittest.TestCase):
    # --- Tests for get_urls_from_html ---

    def test_get_urls_from_html_no_links(self):
        input_url = "https://crawler-test.com"
        # Das HTML enthält Text und Überschriften, aber kein <a>-Tag
        input_body = '<html><body><h1>Willkommen</h1><p>Hier gibt es keine Links.</p></body></html>'
        
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_absolute_1(self):
        """Test 1: Erkennt absolute Links korrekt."""
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>About Us</span></a></body></html>'
        
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute_2(self):
        """Test 1: Erkennt absolute Links korrekt."""
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler.com"><span>About Us</span></a></body></html>'
        
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        """Test 2: Wandelt relative Links in absolute Links um."""
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/posts/welcome">Read Post</a></body></html>'
        
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/posts/welcome"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_and_missing(self):
        """Test 3: Findet mehrere Links und ignoriert a-Tags ohne href."""
        input_url = "https://mysite.org"
        input_body = '''
        <div>
            <a href="https://external.com">External</a>
            <a href="../contact">Contact</a>
            <a>Anchor without href</a>
        </div>
        '''
        
        actual = get_urls_from_html(input_body, input_url)
        # ../contact aufgelöst gegen https://mysite.org ergibt https://mysite.org
        expected = ["https://external.com", "https://mysite.org/contact"]
        self.assertEqual(actual, expected)


    # ==========================================
    # TESTS FÜR get_images_from_html
    # ==========================================

    #def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    #def test_get_images_from_html_relative_dir(self):
        """Test 1: Wandelt relative Bildpfade in absolute um."""
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/assets/logo.png" alt="Logo"></body></html>'
        
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/assets/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        """Test 2: Behält bereits absolute Bild-URLs bei."""
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://boot.dev"></body></html>'
        
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        """Test 2: Behält bereits absolute Bild-URLs bei."""
        input_url = "https://shop.boot.dev"
        input_body = '<html><body><img src="https://boot.dev"></body></html>'
        
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://boot.dev"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_missing_src(self):
        """Test 3: Ignoriert img-Tags, bei denen das src-Attribut komplett fehlt."""
        input_url = "https://batman.net"
        input_body = '<html><body><img alt="Broken Image Tag"><img src="pic.jpg"></body></html>'
        
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://batman.net/pic.jpg"]
        self.assertEqual(actual, expected)



if __name__ == "__main__":
    unittest.main()