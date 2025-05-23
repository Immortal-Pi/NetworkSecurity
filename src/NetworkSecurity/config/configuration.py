from datetime import datetime
import os 
from NetworkSecurity.constants import training_pipeline 

class TrainingPipelineConfig:
    def __init__(self, timestamp=datetime.now()):
        timestamp=timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        self.timestamp: str=timestamp
        

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME
        )
        self.training_file_path: str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.training_file_path: str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )
        self.test_file_path: str=os.path.join(
            self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESION_TAIN_TEST_SPLIT_RATIO
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                                     training_pipeline.TRAIN_FILE_NAME.replace('csv','npy'),)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,
                                                            training_pipeline.TEST_FILE_NAME.replace('csv','npy'),)
        self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                                                            training_pipeline.PREPROCESSING_OBJECT_FILE_NAME,)
        