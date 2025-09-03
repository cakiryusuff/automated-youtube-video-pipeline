import pytest
from src.news_fetcher import NewsFetcher

def test_fetch_news_content():
    news_fetcher = NewsFetcher()
    news = news_fetcher.fetch_news_content(news_count=1)
    assert isinstance(news, list)
    assert len(news) > 0