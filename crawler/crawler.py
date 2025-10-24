from typing import Callable
import time

from core.models import *
from core.queue import CrawlQueue
from core.fetcher import fetch_page
from core.scheduler import Scheduler
from core.change_detector import ChangeDetector
from core.scraper import CrawlerScraper
import core.scope as Scope

class Crawler:
    def __init__(self, url:str,
                 queue:CrawlQueue = CrawlQueue(), scope:Scope.Scope = Scope.Unrestricted(), 
                 scraper:CrawlerScraper = CrawlerScraper(),scheduler:Scheduler=Scheduler()):
        
        self.init_url = Url(url)
        self.queue = queue
        self.scraper = scraper
        self.scheduler = scheduler
        self.scope = scope
        
        self.queue.add_url(self.init_url,0)

    def __iter__(self):
        return self
    
    def __next__(self):
        while (item := self.queue.next_link()) is not None:
            url, depth = item

            if item is None:
                if self.scheduler.mode == "continuous":
                    time.sleep(1)
                    continue
                else:
                    break

            if self.scheduler.should_crawl(url):
                self.queue.add_url(url,depth)
                continue
            
            page = fetch_page(url)
            if page is None: continue

            if self.scheduler.process(page):
                self.scraper = self.scraper.step(page)
                new_links = [link for link in self.scraper() if self.scope(link)]
            else:
                continue

            self.queue.add_new_links(new_links,depth)

            if self.scheduler.mode in ("incremental", "continuous"):
                self.queue.add_url(url, depth)

            return page.url, page.html
        raise StopIteration
    
url = "https://books.toscrape.com/"
crawler = Crawler(url,)

for url, html in crawler:
    print(url)

