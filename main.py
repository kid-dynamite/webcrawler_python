from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

def main():
    html = """<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
            <p>Main paragraph._1</p>
            <p>Main paragraph._2</p>
        </main>
    </body></html>"""
    print(get_first_paragraph_from_html(html))


if __name__ == "__main__":
    main()
