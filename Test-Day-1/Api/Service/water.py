import json
from typing import List
from fastapi import HTTPException
from Repository.water import WaterRepository
from Model.water import WaterData   
import requests


class WaterService:
    @staticmethod
    async def getWaterById(Id:str):
        water = await WaterRepository.getOneById(Id=Id)
        if water:
            water= json.loads(json.dumps(water,default=str))
            return water
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
    async def createWater(data:WaterData):
        water = await WaterRepository.createWater(data=data)
        if water:
            return water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")
        
    @staticmethod
    async def getWaterForApiByID(id:str):
        if int(id) <500 or int(id) > 1000:
            raise HTTPException(status_code=400,detail="Please Enter ID between 500-1000")
        url = 'http://192.168.1.3:7078/'+str(id)
        mockup = requests.get(url)
        if mockup:
            mockup=json.loads(mockup.text)
            data_water =WaterData(
                w_date = mockup[0]['w_date'],
                w_height = mockup[0]['w_height'],
                w_cubic = mockup[0]['w_cubic']
            )
            return data_water
        else:
            raise HTTPException(status_code=400,detail="Water Not Found")