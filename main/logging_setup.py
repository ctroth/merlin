# main/logging_setup.py

import logging
import os
from datetime import datetime
import time

def configure_daily_logging(
    log_directory: str = "logs",
    fmt: str = "{asctime} - {levelname} - {name} - {message}",
    datefmt: str = "%Y-%m-%d %H:%M:%S"
):
    """
    Ensure the folder `log_directory` exists, then route all root‐logger
    output into a file named YYYY-MM-DD.log (appending if it exists).
    Safe to call multiple times.
    """
    # 1) Ensure the logs folder exists
    os.makedirs(log_directory, exist_ok=True)

    # 2) Build today's filename
    todays_date = datetime.utcnow().strftime("%Y-%m-%d")
    log_file = os.path.join(log_directory, f"{todays_date}.log")

    # 3) Only configure once
    root = logging.getLogger()
    if not root.handlers:
        logging.Formatter.converter = time.gmtime
        logging.basicConfig(
            level=logging.INFO,
            filename=log_file,
            filemode="a",         
            format=fmt,
            datefmt=datefmt,
            style='{',            
        )
