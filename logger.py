# utils/logger.py
import logging
from pathlib import Path

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# --- Orders Logger ---
order_logger = logging.getLogger("order_logger")
order_logger.setLevel(logging.INFO)
if not order_logger.handlers:
    fh = logging.FileHandler("logs/orders.log", encoding="utf-8")
    fh.setFormatter(formatter)
    order_logger.addHandler(fh)

# --- Errors Logger ---
error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)
if not error_logger.handlers:
    fh = logging.FileHandler("logs/errors.log", encoding="utf-8")
    fh.setFormatter(formatter)
    error_logger.addHandler(fh)

def log_info(message: str):
    order_logger.info(message)

def log_error(message: str):
    error_logger.error(message)

log_info("Test INFO message")
log_error("Test ERROR message")
