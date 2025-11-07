import logging, sys, os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger

def setup_json_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("pdc")
    logger.setLevel(logging.INFO)

    # Console
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    # File (rotating)
    fh = RotatingFileHandler("logs/app.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    if not logger.handlers:
        logger.addHandler(sh)
        logger.addHandler(fh)

    return logger
