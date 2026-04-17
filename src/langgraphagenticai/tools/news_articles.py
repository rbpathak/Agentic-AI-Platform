import requests
from bs4 import BeautifulSoup

class Tools:
    def __init__(self,url):
        self.url=url

#    def fetch_article_from_url(self) -> str:
#        try:
#            resp = requests.get(self.url, timeout=10)
#            soup = BeautifulSoup(resp.text, "html.parser")
#            paragraphs = [p.get_text() for p in soup.find_all("p")]
#            return "\n".join(paragraphs[:20])  # take first 20 paragraphs
#        except Exception as e:
#            return f"Error fetching article from URL: {e}"
