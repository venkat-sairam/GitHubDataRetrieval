
from pipeline import PipelineConfiguration

class main:

    def run_pipeline(self) -> None:
        pipeline = PipelineConfiguration()
        pipeline.initiate_data_ingestion()



if __name__ == '__main__':
    t = main()
    t.run_pipeline()
