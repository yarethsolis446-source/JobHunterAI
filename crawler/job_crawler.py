from bs4 import BeautifulSoup

from network.http_client import HttpClient


class JobCrawler:

    def __init__(self):

        self.client = HttpClient()

    def descargar_html(self, url):

        return self.client.get_text(url)

    def obtener_soup(self, url):

        html = self.descargar_html(url)

        if html is None:

            return None

        return BeautifulSoup(html, "html.parser")