from datetime import datetime
import logging
import os

timestamp_format = "%d-%m-%y_%H-%M-%S"

CURR_TIMESTAMP = f"{datetime.now().strftime(timestamp_format)}"
LOGS_DIRECTORY_NAME = "Log_Files"
CWD = os.getcwd()

directory_path = os.path.join(CWD, LOGS_DIRECTORY_NAME)
os.makedirs(directory_path, exist_ok=True)

LOG_FILE_NAME = f"{CURR_TIMESTAMP}.log"
LOG_FILE_PATH = os.path.join(directory_path, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s -%(message)s",
    level=logging.INFO
    )
