from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import (TrainingPipelineConfig, 
                                                  DataIngestionConfig, 
                                                  DataValidationConfig,
                                                  DataTransformationConfig)
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.exception.exception import NetworkSecurityException
import sys 




if __name__=='__main__':
    try:
        STAGE_NAME='DATA INGESTION STAGE'
        logging.info(f'<==========================={STAGE_NAME} STARTED===========================>')
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info('INITIATED DATA INGESTION COMPONENT')
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info(f'<==========================={STAGE_NAME} COMPLETED===========================>')

        STAGE_NAME='DATA VALIDATION STAGE'
        logging.info(f'<==========================={STAGE_NAME} STARTED===========================>')
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info('INITIATE DATA VALIDATION')
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info(f'<==========================={STAGE_NAME} COMPLETED===========================>')

        STAGE_NAME='DATA TRANSFORMATION STAGE'
        logging.info(f'<==========================={STAGE_NAME} STARTED===========================>')
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info('INITIATE DATA TRANFORMATION')
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(f'<==========================={STAGE_NAME} COMPLETED===========================>')

    except Exception as e:
        raise NetworkSecurityException(e,sys)