import sys 
import os 
import pymongo
import certifi
from dotenv import load_dotenv
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run 
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
from NetworkSecurity.utils.main_utils.utils import load_object
from NetworkSecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from NetworkSecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

ca=certifi.where()
load_dotenv()

mongo_db_url=os.getenv('MONGODB_URI')
print(mongo_db_url)

client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=database[DATA_INGESTION_COLLECTION_NAME]

