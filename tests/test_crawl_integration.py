import pytest
from SmartSpider.core import Page, Scope, Scheduler
from SmartSpider.crawler import Crawler

@pytest.fixture
def mock_fetch(monkeypatch):
    def _mock_page(url):
        html = f"<a href='{url.href}/next'>Next</a>"
        return Page(url, html)
    # patch where Crawler actually uses it
    monkeypatch.setattr("crawler.crawler.fetch_page", _mock_page)
    return _mock_page


def test_crawler_iterates(mock_fetch):
    crawler = Crawler(
        url="https://example.com",
        scheduler=Scheduler(mode="once"),  # ensure should_crawl always True
        scope=Scope.Unrestricted()
    )

    url, html = next(crawler)
    assert url == "https://example.com"
    assert "<a href='https://example.com/next'>Next</a>" in html
