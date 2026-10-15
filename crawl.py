from urllib.parse import urlsplit

def normalize_url(url: str) -> str:
    
    parsed = urlsplit(url)
    
    full_path = f"{parsed.netloc}{parsed.path}"
    
    if full_path.endswith("/"):
        full_path = full_path[:-1]

    return full_path
    

