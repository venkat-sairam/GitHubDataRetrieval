import os
import sys
from datetime import datetime


ROOT_DIR = os.getcwd()

CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR,  CONFIG_FILE_NAME)
timestamp_format = "%d-%m-%y_%H-%M-%S"


CURRENT_TIME_STAMP = f"{datetime.now().strftime(timestamp_format)}"
# Training pipeline constants WITH KEY and VALUES
TRAINING_PIPELINE_CONFIGURATION_KEY = "artifacts_directory"
TRAINING_PIPELINE_ARTIFACT_DIRECTORY_KEY = "artifact_directory"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# Data Ingestion configuration constants
DATA_INGESTION_CONFIGURATION_KEY = "data_ingestion_configuration"
DATA_INGESTION_ARTIFACT_DIRECTORY_KEY = "data_ingestion_artifact_directory_name"
DATA_INGESTION_SOURCE_DATA_DIRECTORY_KEY = "source_data_directory"
DATA_INGESTION_INGESTED_DIRECTORY_NAME_KEY = "ingested_data_directory"
DATA_INGESTION_TRAIN_DIRECTORY_KEY = "ingested_train_directory"
DATA_INGESTION_TEST_DIRECTORY_KEY = "ingested_test_directory"

