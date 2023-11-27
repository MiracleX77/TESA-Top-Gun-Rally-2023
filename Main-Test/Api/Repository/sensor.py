from datetime import datetime

from Config.Connection import mongo_connected
from bson import ObjectId
from Model.sensor import SensorData,UpdateSensorData

class SensorRepository :
    @staticmethod
    async def getOneById(id:int):
        sensor = mongo_connected.collection("sensor").find_one({"sensor_id": id})
        if sensor:
            return sensor
        return False
    
    @staticmethod
    async def getAll():
        sensor = mongo_connected.collection("sensor").find()
        if sensor:
            return sensor
        return False



    @staticmethod
    async def create(data:SensorData):
        sensor = mongo_connected.collection("sensor").insert_one(data.model_dump())
        if sensor:
            return sensor
        return False
    
    @staticmethod
    async def update(id:int,data:UpdateSensorData):
        sensor = mongo_connected.collection("sensor").update_one({"sensor_id": id},{"$set":data.model_dump()})
        if sensor:
            return sensor
        return False

    @staticmethod
    async def updateTime(id:int):
        sensor = mongo_connected.collection("sensor").update_one({"sensor_id": id},{"$set":{"update_on": datetime.now(),"status":"ONLINE"}})
        if sensor:
            return sensor
        return False
    
    @staticmethod
    async def updateStatus(id:int,status:str):
        sensor = mongo_connected.collection("sensor").update_one({"sensor_id": id},{"$set":{"status":status}})
        if sensor:
            return sensor
        return False
    
    @staticmethod
    async def delete(id:int):
        sensor = mongo_connected.collection("sensor").delete_one({"sensor_id": id})
        if sensor:
            return sensor
        return False