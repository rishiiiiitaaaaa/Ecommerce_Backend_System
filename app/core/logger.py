import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode='a'),  # Append mode
        logging.StreamHandler()  # Also output to console
    ]
)

logger = logging.getLogger("app")
