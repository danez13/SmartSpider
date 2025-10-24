from SmartSpider.core import CrawlerScraper, Page, Url

def test_extract_links_from_page():
    html = """
    <html><body>
        <a href="/about">About</a>
        <a href="https://example.com/contact">Contact</a>
        <a>No href</a>
    </body></html>
    """
    page = Page("https://example.com", html)
    scraper = CrawlerScraper(page)
    links = scraper()
    hrefs = [link.href for link in links]
    assert "https://example.com/about" in hrefs
    assert "https://example.com/contact" in hrefs
    assert len(hrefs) == 2
