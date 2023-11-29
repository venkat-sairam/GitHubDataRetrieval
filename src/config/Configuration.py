from src.constants import *
from src.utils.util import read_yaml_file
from src.entity.configuration_entity import DataIngestionConfiguration, TrainingPipelineConfiguration
from src.exceptions.CustomException import CustomException
from src.logger.logger import logging


class Configuration(object):

    def __init__(self, configuration_file_path = CONFIG_FILE_PATH, current_time_stamp = CURRENT_TIME_STAMP ) -> None:
        try:
            self.configuration_info = read_yaml_file(file_path=configuration_file_path)
            self.training_pipeline_configuration = self.get_training_pipeline_configuration_details()
            self.time_stamp = current_time_stamp
        except Exception as e:
            raise CustomException(e, sys)
            
    def get_training_pipeline_configuration_details(self) -> TrainingPipelineConfiguration:

        try:
            training_pipeline_configuration = self.configuration_info[TRAINING_PIPELINE_CONFIGURATION_KEY]
            artifact_directory = os.path.join(
                ROOT_DIR,
                training_pipeline_configuration[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_configuration[TRAINING_PIPELINE_ARTIFACT_DIRECTORY_KEY]
            )            
            training_pipeline_config  =TrainingPipelineConfiguration(artifact_directory= artifact_directory)           
            logging.info(f"Training pipeline configuration Details are: {training_pipeline_configuration}")
            return training_pipeline_config        
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_ingestion_configuration(self) -> DataIngestionConfiguration:
        try:
            artifact_directory_location = self.training_pipeline_configuration.artifact_directory
            data_ingestion_information = self.configuration_info[DATA_INGESTION_CONFIGURATION_KEY]
            
            data_ingestion_artifact_location = os.path.join(artifact_directory_location, data_ingestion_information[DATA_INGESTION_ARTIFACT_DIRECTORY_KEY], self.time_stamp)

            source_data_directory = os.path.join(data_ingestion_artifact_location, data_ingestion_information[DATA_INGESTION_SOURCE_DATA_DIRECTORY_KEY])

            ingested_data_directory = os.path.join(data_ingestion_artifact_location, data_ingestion_information[DATA_INGESTION_INGESTED_DIRECTORY_NAME_KEY])

            ingested_train_directory = os.path.join(ingested_data_directory, data_ingestion_information[DATA_INGESTION_TRAIN_DIRECTORY_KEY])

            ingested_test_directory = os.path.join(ingested_data_directory, data_ingestion_information[DATA_INGESTION_TEST_DIRECTORY_KEY])

            data_ingestion_configuration_details = DataIngestionConfiguration(
                source_data_directory = source_data_directory,
                ingested_directory = ingested_data_directory,
                ingested_train_directory = ingested_train_directory,
                ingested_test_directory = ingested_test_directory
                
            )

            logging.info(f"Data ingestion configuration Details are: {data_ingestion_configuration_details}")
            return data_ingestion_configuration_details
        
        except Exception as e:
            raise CustomException(e, sys)

