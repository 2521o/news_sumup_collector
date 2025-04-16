import logging

# Log configuration
log_path = "logs/app.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name=None):
    """
    Returns a logger with the specified name.
    """
    return logging.getLogger(name)

