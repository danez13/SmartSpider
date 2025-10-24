from bs4 import BeautifulSoup,Tag
from .models import *

class CrawlerExtractor:
    @staticmethod
    def extract_href(element:Tag):
        if element.has_attr("href"):
            return str(element.get("href"))


class CrawlerScraper:
    def __init__(self,page:Page|None=None):
        self.page = page
        self.soup = BeautifulSoup(page.html if isinstance(page,Page) else "","html.parser")
        self.extractor = CrawlerExtractor()

    def __call__(self) -> list[Url]:
        links = []

        for tag in self.soup.find_all("a", href=True):
            try:
                 relative_url = self.extractor.extract_href(tag)
                 assert relative_url
                 new_url = self.page._url + relative_url
            except ValueError:
                continue

            if new_url.domain == self.page.domain:
                links.append(new_url)
        
        return links
    
    @classmethod
    def step(cls,page:Page):
        return cls(page)
