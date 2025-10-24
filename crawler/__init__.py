"""
Crawler Package
===============

High-level entrypoint for the web crawler system.

This package combines modular components from `core` to provide:
- Priority-based, adaptive crawling (BFS, DFS, priority)
- Incremental and continuous scheduling
- Domain and subdomain scope control
- Optional content change detection
"""

from .crawler import Crawler
from .core import (
    Url,
    Page,
    CrawlTask,
    CrawlQueue,
    Scheduler,
    Scope,
    CrawlerScraper,
    fetch_page,
    ChangeDetector,
)

__all__ = [
    "Crawler",
    "Url",
    "Page",
    "CrawlTask",
    "CrawlQueue",
    "Scheduler",
    "CrawlMode",
    "Scope",
    "CrawlerScraper",
    "fetch_page",
    "ChangeDetector",
]
