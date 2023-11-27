from typing import List
from fastapi import APIRouter
from Model.response import ResponseData
from Model.water import WaterData,LastWaterData,RequestWaterData
from Service.water import WaterService

router = APIRouter(
    prefix="/api/water",
    tags =["water"],
    responses={404:{"description":"Not found"}},
)

@router.get("/get/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getWater(id:str):
    res = await WaterService.getWaterById(id=id)
    return ResponseData(detail="Get Water Success",result=res)

@router.get("/getAll",response_model=ResponseData,response_model_exclude_none=True)
async def getWaters():
    res = await WaterService.getAllWater()
    return ResponseData(detail="Get Water Success",result=res)

@router.get("/getBySensorId/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getWatersBySensor(sensor_id:str):
    res = await WaterService.getWaterBySensorId(sensor_id)
    return ResponseData(detail="Get Water Success",result=res)

@router.post("/getLastBySensorId",response_model=ResponseData,response_model_exclude_none=True)
async def getLastBySensorId(data:LastWaterData):
    res = await WaterService.getLastBySensorId(data=data)
    return ResponseData(detail="Get Last Water Success",result=res)

@router.post("/create",response_model=ResponseData,response_model_exclude_none=True)
async def createWater(data:RequestWaterData):
    await WaterService.createWater(data=data)
    return ResponseData(detail="Create Water Success")
