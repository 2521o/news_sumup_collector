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

    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(os.getenv("SMTP_SERVER"), os.getenv("SMTP_PORT")) as server:
            server.starttls()  # Sécurise la connexion
            server.login(os.getenv("SENDER_EMAIL_ADDRESS"), os.getenv("SENDER_EMAIL_PASSWORD"))
            log_handler.info("Login successful")
            server.send_message(msg)
            log_handler.info(f"Email sent to {to_email}")
            
    except Exception as e:
        log_handler.error(f"Failed to send email: {e}")

def get_summary_from_json_html(path: str)->str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            articles = json.load(f)
            log_handler.info("JSON file loaded successfully")
    except FileNotFoundError as e:
        log_handler.error(f"Error reading JSON file: {e}")
        return "<p>Error loading articles.</p>"

    html = """
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
        <h2 style="color: #2c3e50;">🗞️ Your Weekly Tech Summary</h2>
        <p style="color: #555;">Here are the highlights:</p>
    """

    for article in articles:
        summary = article.get("summary")
        link = article.get("link")
        title = article.get("title")
        source = article.get("source")

        if summary:
            html += f"""
            <div style="background-color: #fff; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <h3 style="margin: 0; color: #34495e;">{title}</h3>
                <p style="font-size: 0.9em; color: #888;">{source}</p>
                <p style="color: #2c3e50;">{summary}</p>
                <a href="{link}" style="color: #3498db;">🔗 Read full article</a>
            </div>
            """

    html += """
        <p style="font-size: 0.8em; color: #aaa;">© 2025 News Sumup Collector</p>
    </body>
    </html>
    """
    log_handler.info("HTML summary generated successfully")
    return html

