import requests
from bs4 import BeautifulSoup


class WebScrape:
    def trigger_error(self, error_message):
        self.has_error = True
        self.error_message = error_message

    def __init__(self, url):
        self.error_message = ""
        self.has_error = False
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, "html.parser")
