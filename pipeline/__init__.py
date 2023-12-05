from src.exceptions.CustomException import CustomException
import sys
from src.logger.logger import logging
from src.config.Configuration import Configuration
from src.components.DataIngestionComponent import DataIngestionComponent
from src.entity.configuration_entity import DataIngestionConfiguration
from src.entity.DeliverableArtifacts_entity import DataIngestionArtifact

class PipelineConfiguration(object):
    
    def __init__(self, configuration = Configuration()) -> None:
        try:
            self.configuration = configuration    
        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(f"Initiating data ingestion")
            print(f"Initiating data ingestion")
            data_ingestion_configuration = self.configuration.get_data_ingestion_configuration()
            print(f"Data ingestion configuration completed successfully........!")
            data_ingestion_component = DataIngestionComponent(data_ingestion_configuration)
            data_ingestion_component.github_users_data_extraction_and_writing_to_csv()
            print(f"Data ingestion completed successfully")
            logging.info(f"Data ingestion completed successfully")
        except Exception as e:
            raise CustomException(e, sys)