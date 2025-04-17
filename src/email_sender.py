import smtplib
import json
import os
from utils.logger import get_logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

log_handler = get_logger(__name__)
load_dotenv()

def send_email(body:str, to_email:str)->None:
    """
    Send an email with the summary of the news
    @param body: The body of the email
    @param to_email: The recipient's email address
    """
    
    msg = MIMEMultipart()
    msg['From'] = os.getenv("SENDER_EMAIL_ADDRESS")
    msg['To'] = to_email
    msg['Subject'] = "Tech news summary 🗞️"

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
            server.starttls()  # Sécurise la connexion
            server.login(os.getenv("SENDER_EMAIL_ADDRESS"), os.getenv("SENDER_EMAIL_PASSWORD"))
            log_handler.info("Login successful")
            server.send_message(msg)
            log_handler.info(f"Email sent to {to_email}")
            
    except Exception as e:
        log_handler.error(f"Failed to send email: {e}")

def get_summary_from_json(path:str)->str:

    body = "📝 Summary :\n"
    
    # Open JSON file
    try:
        with open(path, "r", encoding="utf-8") as f:
            articles = json.load(f)
            log_handler.info("JSON file loaded successfully")
    except FileNotFoundError as e:
        log_handler.error(f"Error reading JSON file: {e}")
        return ""

    # Add the summary of each article to body text
    for article in articles:
        summary = article.get("summary")
        if summary:
            body += f"- {summary}\n"
            body += f"  [Read the article]({article.get('link')})\n\n"
            body += "------------------------\n\n"
    
    log_handler.info("Summary retrieved successfully")
    
    return body
