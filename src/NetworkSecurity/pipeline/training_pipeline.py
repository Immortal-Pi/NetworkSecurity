import os 
import sys 

from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.model_trainer import ModelTrainer

from NetworkSecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelTraninerConfig
)

from NetworkSecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataTransformationArtifact,
    DataValidationAritifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Start data Ingestion')
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info('Data Ingestion Completed')
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
         try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Start Data Validation Config')
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            logging.info('Data Validation Completed')
            return data_validation_artifact
         except Exception as e:
             raise NetworkSecurityException(e,sys)
         
    def start_data_transformation(self,data_validation_artifact:DataValidationAritifact):
        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Start Data Transformation Started')
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info('Data Transformation Completed')
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTraninerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info('Model Trainer Started')
            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_trainer_config)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info('Model Trainer ended')
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
         
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
