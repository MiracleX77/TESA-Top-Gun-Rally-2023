from typing import List
from fastapi import APIRouter
from Model.response import ResponseData
from Model.water import WaterData
from Service.water import WaterService

router = APIRouter(
    prefix="/api/water",
    tags =["water"],
    responses={404:{"description":"Not found"}},
)

@router.get("/getWaterByID/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getWater(id:str):
    res = await WaterService.getWaterByID(id=id)
    return ResponseData(detail="Get Water Success",result=res)

@router.get("/getWaters",response_model=ResponseData,response_model_exclude_none=True)
async def getWaters():
    res = await WaterService.getAllWater()
    return ResponseData(detail="Get Water Success",result=res)

@router.post("/createWater",response_model=ResponseData,response_model_exclude_none=True)
async def createWater(data:WaterData):
    await WaterService.createWater(data=data)
    return ResponseData(detail="Create Water Success")

@router.get("/saveWaterById/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def saveWater(id:str):
    data = await WaterService.getWaterForApiByID(id=id)
    await WaterService.createWater(data=data)
    return ResponseData(detail="Save Water Success")