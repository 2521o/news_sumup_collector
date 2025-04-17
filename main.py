import os
from dotenv import load_dotenv
from utils.logger import get_logger
from src.collector import collect_articles, save_articles_to_json
from src.email_sender import send_email, get_summary_from_json

load_dotenv()
log_handler = get_logger(__name__)

if __name__ == "__main__":
    log_handler.info("Démarrage de l'application...")
    try:
        articles = collect_articles(5)
        save_articles_to_json(articles, "data/article_test.json")
        body = get_summary_from_json("data/article_test.json")
        send_email(body, "floriandlg@protonmail.com")
        log_handler.info("Fin d'exécution.")
    except Exception as e:
        log_handler.error("Une erreur est survenue lors de l'exécution de l'application : %s", e)
