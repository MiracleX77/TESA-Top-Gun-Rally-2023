import os
from pymongo import MongoClient

class Connection:
    def __init__(self) -> None:
        #dev 
        username = os.environ.get('MONGO_INITDB_ROOT_USERNAME')
        password = os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
        self.mongo  = MongoClient(f"mongodb://{username}:{password}@test-1-mongo-1:27017/")
        # db_url = "mongodb://localhost:27017"
        # self.mongo = MongoClient(db_url)

    def database(self,name_database:str):
        self.mongo = self.mongo[name_database]
    
    def collection(self,name_collection:str):
        collection = self.mongo[name_collection]
        return collection
    
mongo_connected = Connection()