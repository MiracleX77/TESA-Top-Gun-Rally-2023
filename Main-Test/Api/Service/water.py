import json
from fastapi import HTTPException
from Repository.water import WaterRepository
from Model.water import RequestWaterData, WaterData,LastWaterData
from Service.function import FunctionService
from Service.sensor import SensorService


class WaterService:
    @staticmethod
    async def getWaterById(id:str):
        water = await WaterRepository.getOneById(id=id)
        if water:
            water= json.loads(json.dumps(water,default=str))
            return water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
    
    @staticmethod
    async def getWaterBySensorId(id:str):
        waters = await WaterRepository.getAllBySensorId(id=int(id))
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
        waters = await WaterRepository.getAll()
        if waters:
            list_water = []
            for water in waters:
                water= json.loads(json.dumps(water,default=str))
                list_water.append(water)
            return list_water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
        
    @staticmethod
    async def getLastBySensorId(data:LastWaterData):
        waters = await WaterRepository.getLastBySensorId(data)
        if waters:
            list_water = []
            for water in waters:
                water= json.loads(json.dumps(water,default=str))
                list_water.append(water)
            return list_water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
        
    @staticmethod
    async def createWater(data:RequestWaterData):
        data_insert = WaterData(
            sensor_id = data.sensor_id,
            water_height = data.water_height,
            status = FunctionService.setStatus(data.water_height)
        )
        water = await WaterRepository.create(data=data_insert)
        if water:
            await SensorService.updateTimeSensor(id=data.sensor_id)
            return water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
        
    
    
