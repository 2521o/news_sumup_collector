import feedparser
import json
from newspaper import Article 
from datetime import datetime

def read_feeds_file(path="feeds/feeds.txt"):
    """
    Reads a file containing RSS feed URLs, one per line.
    Lines starting with '#' are treated as comments and ignored.
    @param path: Path to the feeds file.
    @return: A list of feed URLs.
    """
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

def collect_articles(n=3):
    """
    Collects the latetst articles from the RSS feeds specified in the feeds file.
    @param n: Number of articles to collect from each feed.
    @return: A list of dictionaries containing article details.
    """
    feeds = read_feeds_file()
    articles = []

    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:n]:
            link = entry.get("link")
            
            # Parsing with newspaper3k to extract the article text
            article = Article(link)
            article.download() # required before parsing
            article.parse()
            
            # Add data to the dictionnary for each article
            articles.append({
                "title": entry.get("title"),
                "author": article.authors,
                "link": link,
                "published": entry.get("published"),
                "summary": entry.get("summary", ""),
                "text": article.text,
                "source": feed.feed.get("title"),
                
            })

    return articles
    
def save_articles_to_json(articles, path=None):
    """
    Saves the collected articles to a JSON file.
    """
    if not path:
        today = datetime.now().strftime("%Y-%m-%d")
        path = f"data/articles_{today}.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    articles = collect_articles()
    save_articles_to_json(articles)
    print(f"Collected {len(articles)} articles.")