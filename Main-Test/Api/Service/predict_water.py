import json
from fastapi import HTTPException
from Repository.predict_water import PredictWaterRepository
from Model.water import RequestWaterData,WaterData
from Service.function import FunctionService

class PredictWaterService:
    @staticmethod
    async def getWaterById(id:str):
        water = await PredictWaterRepository.getOneById(id=id)
        if water:
            water= json.loads(json.dumps(water,default=str))
            return water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
    
    @staticmethod
    async def getWaterBySensorId(id:str):
        waters = await PredictWaterRepository.getAllBySensorId(id=int(id))
        if waters:
            list_water = []
            for water in waters:
                water= json.loads(json.dumps(water,default=str))
                list_water.append(water)
            return list_water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
    
    @staticmethod
    async def getAllWater():
        waters = await PredictWaterRepository.getAll()
        if waters:
            list_water = []
            for water in waters:
                water= json.loads(json.dumps(water,default=str))
                list_water.append(water)
            return list_water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
    @staticmethod
    async def createPredictWater(data:RequestWaterData):
        data_insert = WaterData(
            sensor_id = data.sensor_id,
            water_height = data.water_height,
            status = FunctionService.setStatus(data.water_height)
        )
        water = await PredictWaterRepository.create(data=data_insert)
        if water:
            return water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
    

