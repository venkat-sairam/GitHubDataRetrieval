from src.constants import ROOT_DIR, CURRENT_TIME_STAMP, os
USERS_URL = "https://api.github.com/users"
STATE_WISE_USERSDATA_FILE_NAME = "statewise_users_data.csv"
STATE_WISE_USERNAMES_FILE_NAME = "state_wise_user_names.csv"
SAMPLE_SIZES_PERCENTAGES = [0.01, 0.03, 0.05, 0.10, 0.15, 0.20]
RANDOM_STATE = 123
TIME_DELAY_SECONDS = 120
NUMBER_OF_SECTIONS = 25

DATASET_LOCATION = "data"
EXTERNAL_DATASET_DIRECTORY_NAME = "external"
PROCESSED_DATASET_DIRECTORY_NAME = "processed"
RAW_DATASET_DIRECTORY_NAME = "raw"

SAMPLED_USERS_DIRECTORY_NAME = "sampled_user_names_files"
REPOSITORY_DATA_DIRECTORY_NAME = "user_repository_data"
REPOSITORY_DATA_FILE_NAME = "GitHub_user_repository_data.csv"

PROCESSED_DATASET_LOCATION = os.path.join(ROOT_DIR, DATASET_LOCATION, PROCESSED_DATASET_DIRECTORY_NAME)

SAMPLED_USERS_DATASET_FILE_PATH = os.path.join(PROCESSED_DATASET_LOCATION,SAMPLED_USERS_DIRECTORY_NAME)
REPOSITORY_DATA_FILE_DIRECTORY_NAME = os.path.join(PROCESSED_DATASET_LOCATION, REPOSITORY_DATA_DIRECTORY_NAME, CURRENT_TIME_STAMP)
REPOSITORY_DATA_FILE_PATH = os.path.join(REPOSITORY_DATA_FILE_DIRECTORY_NAME, REPOSITORY_DATA_FILE_NAME)
