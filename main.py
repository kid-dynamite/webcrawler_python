from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html

def main():
    html = """<html><body><img src="https://boot.dev"></body></html>"""
    print(get_images_from_html(html, "https://crawler-test.com"))


if __name__ == "__main__":
    main()
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html

