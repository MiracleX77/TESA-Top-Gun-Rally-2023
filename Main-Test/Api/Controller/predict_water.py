from fastapi import APIRouter
from Model.response import ResponseData
from Model.water import RequestWaterData
from Service.predict_water import PredictWaterService

router = APIRouter(
    prefix="/api/predictWater",
    tags =["predictWater"],
    responses={404:{"description":"Not found"}},
)
@router.get("/get/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getWater(id:str):
    res = await PredictWaterService.getWaterById(id=id)
    return ResponseData(detail="Get Water Success",result=res)

@router.get("/getAll",response_model=ResponseData,response_model_exclude_none=True)
async def getWaters():
    res = await PredictWaterService.getAllWater()
    return ResponseData(detail="Get Water Success",result=res)

@router.get("/getBySensorId/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getWatersBySensor(sensor_id:str):
    res = await PredictWaterService.getWaterBySensorId(sensor_id)
    return ResponseData(detail="Get Water Success",result=res)

@router.post("/create",response_model=ResponseData,response_model_exclude_none=True)
async def createPredictWater(data:RequestWaterData):
    await PredictWaterService.createPredictWater(data=data)
    return ResponseData(detail="Create PredictWater Success")