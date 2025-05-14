from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.exception.exception import NetworkSecurityException
import sys 




if __name__=='__main__':
    try:
        STAGE_NAME='DATA INGESTION STAGE'
        logging.info(f'{STAGE_NAME} started')
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info('INITIATED DATA INGESTION COMPONENT')
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info(f'{STAGE_NAME} completed')
        print(dataingestionartifact)

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info('Initiate the data validation')
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info('Data validation completed')
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)