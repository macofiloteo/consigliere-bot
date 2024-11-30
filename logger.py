import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[*] %(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("consigliere-bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logging.basicConfig(
    level=logging.CRITICAL,
    format="[!!!] %(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler("consigliere-bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
_logger = logging.getLogger("consigliere-bot")

def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_unhandled_exception

logger = _logger