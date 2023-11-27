from Config.Connection import mongo_connected
from bson import ObjectId
from Model.water import WaterData,LastWaterData

class WaterRepository :
    @staticmethod
    async def getOneById(id:str):
        water = mongo_connected.collection("water").find_one({"_id": ObjectId(id)})
        if water:
            return water
        return False
    
    @staticmethod
    async def getAll():
        water = mongo_connected.collection("water").find()
        if water:
            return water
        return False
    
    @staticmethod
    async def getAllBySensorId(id:int):
        water = mongo_connected.collection("water").find({"sensor_id": id})
        if water:
            return water
        return False
    
    @staticmethod
    async def getLastBySensorId(data:LastWaterData):
        water = mongo_connected.collection("water").find({"sensor_id": data.sensor_id}).sort("create_on",-1).limit(data.count_data)
        if water:
            return water
        return False


    @staticmethod
    async def create(data:WaterData):
        water = mongo_connected.collection("water").insert_one(data.model_dump())
        if water:
            return water
        return False
