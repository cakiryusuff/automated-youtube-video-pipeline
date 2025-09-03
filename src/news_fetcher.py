from bs4 import BeautifulSoup
import requests
from src.logger import get_logger

logger = get_logger(__name__)

class NewsFetcher:
    def __init__(self):
        pass
    
    def fetch_news_list(self, url = "https://www.donanimhaber.com") -> list:
        try:
            logger.info("Fetching news list...")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', class_='NewsDetailOpenWindow')
            href_list= [url + a.get("href") for a in links if a.get("href")]
            logger.info(f"Fetched {len(href_list)} news links.")
        except Exception as e:
            logger.error(f"Error while fetching news list: {e}")
            raise e
        
        return list(set(href_list))
    
    def fetch_news_content(self, news_count: int = 1) -> str:
        try:
            news = []
            logger.info("Fetching news content...")
            href_list = self.fetch_news_list()
            for href in href_list[:news_count]:
                response = requests.get(href)
                soup = BeautifulSoup(response.content, 'html.parser')
                section = soup.find("section")
                if section:
                    icerik = []
                    for elem in section.children:
                        if elem.name == "script":
                            break
                        if elem.get_text(strip=True):
                            icerik.append(elem.get_text(" ", strip=True))
                    news.append(" ".join(icerik))
            logger.info("Fetched news content successfully.")
        except Exception as e:
            logger.error(f"Error while fetching news content: {e}")
            raise e
        
        return news

if __name__ == "__main__":
    news_fetcher = NewsFetcher()
    news_list = news_fetcher.fetch_news_list()
    news = news_fetcher.fetch_news_content([])

    print(news)

