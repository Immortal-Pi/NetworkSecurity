from pymongo.mongo_client import MongoClient
import os 
from dotenv import load_dotenv
load_dotenv()


client=MongoClient(os.getenv('MONGODB_URI'))

try:
    client.admin.command('ping')
    print('Pinged your deployment. You successfully connected to mongoDB')
except Exception as e:
    print(e)
