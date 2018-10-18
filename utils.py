import requests
from bs4 import BeautifulSoup


def requests_content(url, session=None):
    s = session
    if session is not None:
        html_data = s.get(url)
        content = html_data.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup
    else:
        html_data = requests.get(url)
        content = html_data.content
        soup = BeautifulSoup(content, 'html.parser')
        return soup


