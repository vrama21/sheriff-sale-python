import requests
from bs4 import BeautifulSoup


def requests_content(url, session=None):
    s = session
    while session:
        response = s.get(url)
        # print(response.url)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup

