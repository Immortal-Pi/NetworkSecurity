import os 
import sys
import json 
from dotenv import load_dotenv
import certifi
import pandas as pd 
import numpy as np
import pymongo
import pymongo.mongo_client
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

load_dotenv()

MONGODB_URI=os.getenv('MONGODB_URI')
# certify if trusted connection to server 
ca=certifi.where()

class NetoworkDataExtract():
    def __init__(self):
        try:
            pass 
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_mongodb(self,records,database, collection):
        try:
            self.database=database
            self.records=records 
            self.collection=collection

            self.mongo_client=pymongo.MongoClient(MONGODB_URI)
            
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    FILE_PATH='Network_Data\phisingData.csv'
    DATABASE='IMMORTALPI'
    collection='NetworkData'
    netoworkobj=NetoworkDataExtract()
    records=netoworkobj.csv_to_json_convertor(file_path=FILE_PATH)
    no_of_records=netoworkobj.insert_data_mongodb(records,DATABASE, collection)
    print(no_of_records)
