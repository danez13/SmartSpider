import pytest
from SmartSpider.core import Page, Scope, Scheduler
from SmartSpider import crawler  # import the module, not the class
from SmartSpider.crawler import Crawler

@pytest.fixture
def mock_fetch(monkeypatch):
    def _mock_page(url):
        html = f"<a href='{url}/next'>Next</a>"  # url is string, no .href
        return Page(url, html)

    # Patch the fetch_page **inside the crawler module**
    monkeypatch.setattr(crawler, "fetch_page", _mock_page)
    return _mock_page


def test_crawler_iterates(mock_fetch):
    crawler_instance = Crawler(
        url="https://example.com",
        scheduler=Scheduler(mode="once"),  # ensure should_crawl always True
        scope=Scope.Unrestricted()
    )

    url, html = next(crawler_instance)
    assert url == "https://example.com"
    assert "<a href='https://example.com/next'>Next</a>" in html
