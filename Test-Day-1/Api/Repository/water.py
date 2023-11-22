from Config.Connection import mongo_connected
from bson import ObjectId
from Model.water import WaterData

class WaterRepository :
    @staticmethod
    async def getOneById(Id:str):
        water = mongo_connected.collection("water").find_one({"_id": ObjectId(Id)})
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
    async def createWater(data:WaterData):
        water = mongo_connected.collection("water").insert_one(data.model_dump())
        if water:
            return water
        return False
