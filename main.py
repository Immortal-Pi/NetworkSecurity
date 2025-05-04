from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.exception.exception import NetworkSecurityException
import sys 



STAGE_NAME='DATA INGESTION STAGE'
if __name__=='__main__':
    try:
        logging.info(f'{STAGE_NAME} started')
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        dataingestion=DataIngestion(dataingestionconfig)
        logging.info('INITIATED DATA INGESTION COMPONENT')
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        print(dataingestionartifact)
        logging.info(f'{STAGE_NAME} completed')
    except Exception as e:
        raise NetworkSecurityException(e,sys)