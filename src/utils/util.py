import yaml
import os, sys
from src.exceptions.CustomException import CustomException
from src.logger.logger import logging
from os import getenv
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from pprint import pprint
import json
import requests
from datetime import datetime
import glob
from inspect import currentframe
timestamp_format = "%d-%m-%y_%H-%M-%S"

def get_current_time_stamp() -> str:    
    return datetime.now().strftime(timestamp_format)

def read_yaml_file(file_path: str)-> dict:

    try:
        with open(file = file_path) as file:
            logging.info(f"reading yaml file at: {file_path}")
            data = yaml.safe_load(file)
            logging.info(f"Finished reading yaml file at: {file_path}")
            return data
        
    except Exception as e:
        raise CustomException(e, sys)

def create_directories(directories_path: str, is_logging_enabled=True) -> None:
    try:
        logging.info(f"creating directory at: {directories_path}")
        os.makedirs(directories_path, exist_ok=True)
        if is_logging_enabled:
            logging.info(f"successfully created directory at: {directories_path}")
    except Exception as e:
        raise CustomException(e, sys)

def load_and_fetch_access_token() -> str:
    try:
        # logging.info(f"Loading access token")
        load_dotenv()
        accessToken = getenv("ACCESS_TOKEN")    
        # logging.info(f"Finished reading access token")
        return accessToken
    except Exception as e:
        raise CustomException(e, sys)
    
def read_from_url(url: str) -> json:
    try:
        # logging.info(f"reading url at: {url}")
        headers = {'Authorization': f'token {load_and_fetch_access_token()}'}
        response = requests.get(url, headers= headers)
        # logging.info(f"Finished reading url at: {url}")
        return response
    except Exception as e:
        raise CustomException(e, sys)
    
def read_from_csv(file_path: str) -> pd.DataFrame:
    try:
        logging.info(f"reading csv file at: {file_path}")
        df = pd.read_csv(file_path)
        logging.info(f"Finished reading csv file at: {file_path}")
        return df
    except Exception as e:
        raise CustomException(e, sys)
    
def write_to_csv(df: pd.DataFrame, file_path: str) -> None:
    try:
        logging.info(f"writing csv file at: {file_path}")
        df.to_csv(file_path, index=False)
        logging.info(f"Finished writing csv file at: {file_path}")
    except Exception as e:
        raise CustomException(e, sys)
    
def create_data_frame(input):
    try:
        logging.info(f"converting input to dataframe")
        if input:
            df = pd.DataFrame(input)
        else:
            df = pd.DataFrame()
        logging.info(f"Finished converting input to dataframe")
        return df
    except Exception as e:
        raise CustomException(e, sys)
    
def join_paths(path1: str, path2: str) -> str:
    
    if path1 and path2:
        return os.path.join(path1, path2)
    # temp_path = ""
    # try:
    #     if path1 and path2:
    #         for path in path2:
    #             temp_path = os.path.join(temp_path, path)
    #         print(f"second path = {temp_path} ")
    #         return os.path.join(path1, temp_path)
    #     else: raise FileNotFoundError 
    # except Exception as e:
    #     raise CustomException(e, sys)