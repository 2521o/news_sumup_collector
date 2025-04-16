from utils.logger import get_logger
from src.collector import collect_articles, save_articles_to_json

log_handler = get_logger(__name__)

if __name__ == "__main__":
    log_handler.info("Démarrage de l'application...")
    try:
        articles = collect_articles()
        save_articles_to_json(articles)
    except Exception as e:
        log_handler.error("Une erreur est survenue lors de l'exécution de l'application : %s", e)
