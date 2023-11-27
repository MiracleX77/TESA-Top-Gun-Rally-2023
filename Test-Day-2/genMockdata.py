from pymongo import MongoClient
import random

class MongoDB(object):
    def __init__(self, host='localhost', port=27017, database_name="mockupdata", collection_name="waterdata"):
        try:
            self._connection = MongoClient(username="", password="", host=host, port=port, maxPoolSize=200)
        except Exception as error:
            raise Exception(error)
        self._database = None
        self._collection = None
        if database_name:
            self._database = self._connection[database_name]
        if collection_name:
            self._collection = self._database[collection_name]

    def insert(self, post):
        # add/append/new single record
        post_id = self._collection.insert_one(post).inserted_id
        return post_id

print('[*] Pushing data to MongoDB ')
mongo_db = MongoDB()

# total days in every month during non leap years
M_DAYS = [0, 32, 29, 32, 31, 32, 31, 32, 32, 31, 32, 31, 32]

def isleap(year):
    """Return True for leap years, False for non-leap years."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
data_list = list()
for year in range(2016,2024,1):
    for month in range(1,13,1):
        for date in range(1,M_DAYS[month],1):
            data_list.append({'Name':'Huana','Date':date,'Month':month,'Year':year,'WaterDataFront':random.randrange(100,200,1),'WaterDataBack':random.randrange(90,180,1),'WaterDrainRate':random.randrange(90,150,2)})
        if month==2 and isleap(year):
            data_list.append({'Name':'Huana','Date':29,'Month':month,'Year':year,'WaterDataFront':random.randrange(100,200,1),'WaterDataBack':random.randrange(90,180,1),'WaterDrainRate':random.randrange(90,150,2)})
        break
for collection in data_list:
    print('[!] Inserting - ', collection)
    mongo_db.insert(collection)