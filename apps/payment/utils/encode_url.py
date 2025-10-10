from urllib.parse import quote

def encode_url(url):
    encoded_url = quote(url, safe='')
    return encoded_url