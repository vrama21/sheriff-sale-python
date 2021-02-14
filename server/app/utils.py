import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup


def requests_content(url: str, session: requests.Session = None):
    """ Creates an html request session and returns the BeautifulSoup parse
    :param url: The url to fetch the request from
    :param session: If a session already exists, update the request in the current session
    """
    response = session.get(url) if session else requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")

    return soup


def load_json_data(json_path: str):
    """ Reads and loads a specified json file.
    :param json_path: The path arg follows the format of app/*json_path*
    """
    path = Path(__file__).resolve().parent / json_path

    with open(path, "r") as file:
        json_data = json.load(file)

        return json_data
