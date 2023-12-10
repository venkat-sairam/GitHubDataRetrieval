from src.constants.github_data_constants import *
from src.entity.configuration_entity import DataTransformationConfiguration
from src.exceptions import CustomException
from src.logger.logger import logging
from src.utils.util import *

class DataTransformationComponent:

    def __init__(self, data_transformation_configuration: DataTransformationConfiguration):
        try:
            self.data_transformation_configuration = data_transformation_configuration
        except CustomException as e:
            raise CustomException(e, sys)

    def initiate_data_preprocessing(self, data_file:str =join_paths(INTEGRATED_DATASET_LOCATION,INTEGRATED_DATA_FILE_NAME) ):
        preprocessed_data_directory  =self.data_transformation_configuration.preprocessed_data_directory
        create_directories(preprocessed_data_directory)

        df = read_from_csv(file_path=data_file)
        # Removing the duplicate entries from the dataframe.
        logging.info(f"Removing the duplicate entries from the dataframe.")
        print(f"Removing the duplicate entries from the dataframe.")
        df.drop_duplicates(inplace=True)
        
        
        logging.info(f"remvoing the white spaces from column names in the dataset")
        print(f"remvoing the white spaces from column names in the dataset")
        df.columns = [col.replace(" ", "_") for col in df.columns]
        
        logging.info(f"Dropping the unnecessary columns from the dataframe")
        print(f"Dropping the unnecessary columns from the dataframe")
        df.drop(columns=['visibility', 'contributors_url', 'languages_url', 'description', 'name', 'default_branch','full_repository_name'], inplace=True)


        logging.info(f"Dropping the duplicated columns in the dataset")
        print(f"Dropping the duplicated columns in the dataset")
        df.drop(columns=['watchers', 'open_issues'],inplace=True)

        logging.info(f"Filtering the numeric columns present in the dataframe....")
        print(f"Filtering the numeric columns present in the dataframe....")
        numeric_columns = df.select_dtypes(include=['number']).columns

        logging.info(f"Filtering the date-time columns in the dataset")
        print(f"Filtering the date-time columns in the dataset")
        date_columns = ['created_at', 'pushed_at','updated_at' ]

        logging.info(f"Converting created_At, pushed_at, updated_At column values to data-time format")
        print(f"Converting created_At, pushed_at, updated_At column values to date-time format")
        # Coverting the created_At, pushed_at, updated_At to data-time format.
        for col in date_columns:
            df[col] = pd.to_datetime(df[col]) 
        
        logging.info(f"Filterin the categorical columns present in the dataframe")
        print(f"Filterin the categorical columns present in the dataframe")
        # Filtering the categorical columns.
        categorical_columns = [col for col in df.columns if (col  not in numeric_columns) and (col not in date_columns)]
        
        
        print(f"{'='*20}Handling Null values{'='*20}")
        logging.info(f"{'='*20}Handling Null values{'='*20}")

        logging.info(f" Replacing all the null values in numeric columns with ZERO's")
        print(f" Replacing all the null values in numeric columns with ZERO's")
        [df[col].fillna(0, inplace=True) for col in df.columns if col in numeric_columns]
        try:
            [df[col].isnull().any() for col in numeric_columns]
        except ValueError:
            raise CustomException("Null Values exists in the dataframe", sys)
        
        print(f"Handling Null values in the date time columns")
        logging.info(f"{'='*20}Handling Null values in the date time columns{'='*20}")

        for col in date_columns:
            df[col].fillna(method='bfill', inplace=True)

        if not df.isnull().any().any():
            logging.info("Successfully handled all the Null values present in the dataframe... ")
            print(f"{'='*20} >> Successfully handled all the Null values preseent in the dataframe << {'='*20} ")
            # preprocessed_data_directory = join_paths(PREPROCESSED_DATASET_DIRECTORY_LOCATION, CURRENT_TIME_STAMP)
            # create_directories(directories_path=preprocessed_data_directory)
            preprocessed_data_file_path = join_paths(preprocessed_data_directory,PREPROCESSED_DATA_FILE_NAME)
            write_to_csv(df=df, file_path=preprocessed_data_file_path)
            final_dataset_location= join_paths(FINAL_DATASET_DIRECTORY_LOCATION, PREPROCESSED_DATA_FILE_NAME)
            print(f"Writing the preprocessed dataset to {final_dataset_location}")
            write_to_csv(df=df, file_path=final_dataset_location)
        else:
            logging.error("Null values were not handled successfully...")
            print("Null values were not handled successfully...")
