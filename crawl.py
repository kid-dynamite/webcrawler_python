from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag

def normalize_url(url: str) -> str:
    
    parsed = urlsplit(url)
    
    full_path = f"{parsed.netloc}{parsed.path}"
    
    if full_path.endswith("/"):
        full_path = full_path[:-1]

    return full_path


def get_heading_from_html(html: str) -> str:

    soup = BeautifulSoup(html, "html.parser")
        
    find_h1 = soup.find("h1")
    if find_h1:        
        return find_h1.get_text(strip=True) 

    find_h2 = soup.find("h2")
    if find_h2:       
        return find_h2.get_text(strip=True)
    
    return ""

def get_first_paragraph_from_html(html: str) -> str:

    soup = BeautifulSoup(html, "html.parser")

    find_main = soup.find("main")
    if find_main:        
        find_p_tag = find_main.find("p")
        if find_p_tag:
            return find_p_tag.get_text(strip=True)
    
    find_p_tag = soup.find("p")
    if find_p_tag:
        return find_p_tag.get_text(strip=True)
    else:
        return ""

def get_urls_from_html(html, base_url):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for a_tag in soup.find_all("a"):
        #print(a_tag)
        href = a_tag.get("href")
        if href:
            #print(href)
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls

def get_images_from_html(html, base_url):
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    for img_tag in soup.find_all("img"):
        src = img_tag.get("src")
        if src:
            absolute_url = urljoin(base_url, src)
            urls.append(absolute_url)
    return urls
    



    



