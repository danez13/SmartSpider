import pytest
from SmartSpider.core import Page, Scope, Scheduler
from SmartSpider import crawler
from SmartSpider.crawler import Crawler

@pytest.fixture
def mock_fetch(monkeypatch):
    def _mock_page(url):
        html = f"<a href='{url}/next'>Next</a>" 
        return Page(url, html)

    monkeypatch.setattr(crawler, "fetch_page", _mock_page)
    return _mock_page


def test_crawler_iterates(mock_fetch):  # 👈 add mock_fetch here
    crawler_instance = Crawler(
        url="https://example.com",
        scheduler=Scheduler(mode="once"),
        scope=Scope.Unrestricted()
    )

    url, html = next(crawler_instance)
    assert url == "https://example.com"
    assert "<a href='https://example.com/next'>Next</a>" in html

