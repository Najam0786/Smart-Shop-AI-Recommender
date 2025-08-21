import logging
import os
import sys
from datetime import datetime

def setup_logger(name: str = "ShopSmartLogger"):
    """
    Sets up a configured logger instance.

    This logger writes to both a daily log file and the console.
    It's designed to prevent duplicate handlers if called multiple times.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: A configured logger instance.
    """
    # 1. Create the logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # 2. Create a log file name based on the current date
    log_file = f"log_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_filepath = os.path.join(logs_dir, log_file)

    # 3. Create a more detailed and structured log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # 4. Get the logger instance and set its base level
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all messages from DEBUG level and up

    # 5. Avoid adding duplicate handlers if the logger is already configured
    if not logger.handlers:
        # Handler for writing logs to a file
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.INFO)  # Only INFO and higher levels go to the file
        logger.addHandler(file_handler)

        # Handler for printing logs to the console
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(log_format)
        stream_handler.setLevel(logging.INFO)  # Only INFO and higher levels appear in the console
        logger.addHandler(stream_handler)

    return logger