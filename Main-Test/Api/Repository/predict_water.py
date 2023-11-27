from Config.Connection import mongo_connected
from bson import ObjectId
from Model.water import WaterData

class PredictWaterRepository :
    @staticmethod
    async def getOneById(id:str):
        predict_water = mongo_connected.collection("predict_water").find_one({"_id": ObjectId(id)})
        if predict_water:
            return predict_water
        return False
    
    @staticmethod
    async def getAll():
        predict_water = mongo_connected.collection("predict_water").find()
        if predict_water:
            return predict_water
        return False
    
    @staticmethod
    async def getAllBySensorId(id:int):
        predict_water = mongo_connected.collection("predict_water").find({"sensor_id": id})
        if predict_water:
            return predict_water
        return False
    
    @staticmethod
    async def create(data:WaterData):
        predict_water = mongo_connected.collection("predict_water").insert_one(data.model_dump())
        if predict_water:
            return predict_water
        return False