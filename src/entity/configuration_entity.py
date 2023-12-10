from collections import namedtuple

DataIngestionConfiguration = namedtuple(
    'DataIngestionConfiguration', [ 'source_data_directory', 'ingested_directory', 'ingested_train_directory','ingested_test_directory'])

DataTransformationConfiguration = namedtuple('DataTransformationConfiguration', [ 'preprocessed_data_directory'])
TrainingPipelineConfiguration = namedtuple('TrainingPipelineConfiguration', ['artifact_directory'])