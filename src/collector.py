import feedparser
import json
import src.cleaner as cleaner
from newspaper import Article 
from datetime import datetime
from utils.logger import get_logger
import src.summarizer as summarizer



# Setup logging
log_handler = get_logger(__name__)

def read_feeds_file(path="feeds/feeds.txt"):
    """
    Reads a file containing RSS feed URLs, one per line.
    Lines starting with '#' are treated as comments and ignored.
    @param path: Path to the feeds file.
    @return: A list of feed URLs.
    """
    log_handler.info("Reading feed file from %s", path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            feeds = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        log_handler.info("Successfully read %d feeds.", len(feeds))
        return feeds
    except Exception as e:
        log_handler.error("Error reading the feed file: %s", str(e))
        raise

def collect_articles(n=3):
    """
    Collects the latetst articles from the RSS feeds specified in the feeds file.
    @param n: Number of articles to collect from each feed.
    @return: A list of dictionaries containing article details.
    """
    assert n > 0, "n must be between 1 and the number of articles in the feed."
    feeds = read_feeds_file()
        
    # List of dictionaries to store articles
    articles = []
    
    for url in feeds:
        try:
            log_handler.info("Processing feed from %s", url)
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:n]:
                link = entry.get("link")
                source = feed.feed.get("title")
                log_handler.info("Processing article from %s", source)
                
                # Parsing with newspaper3k to extract the article text
                article = Article(link)
                article.download() # required before parsing
                article.parse()
                text = article.text
                
                # Clean the text using the cleaner module
                cleaned_text = cleaner.clean_text(text, source)
                
                # Summarize the article text
                summary = summarizer.summarize_article(cleaned_text)
                
                # Add data to the dictionnary for each article
                articles.append({
                    "source": source,
                    "title": entry.get("title"),
                    "author": article.authors[0],
                    "link": link,
                    "published": entry.get("published"),
                    "text": cleaned_text,
                    "summary": summary
                })
                
                log_handler.info("Article from %s processed successfully", source)
        except Exception as e:
            log_handler.error("Error processing feed %s: %s", url, str(e))

    log_handler.info("Collected %d articles successfully", len(articles))
    return articles
    
def save_articles_to_json(articles, path=None):
    """
    Saves the collected articles to a JSON file.
    """
    if not path:
        today = datetime.now().strftime("%Y-%m-%d")
        path = f"data/articles_{today}.json"

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        log_handler.info("Successfully saved %d articles", len(articles))
    except Exception as e:
        log_handler.error("Error saving articles to JSON: %s", str(e))
        raise
