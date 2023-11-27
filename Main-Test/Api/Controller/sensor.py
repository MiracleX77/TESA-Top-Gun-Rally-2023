from fastapi import APIRouter
from Model.response import ResponseData
from Model.sensor import SensorData,RequestSensorData,UpdateSensorData
from Service.sensor import SensorService

router = APIRouter(
    prefix="/api/sensor",
    tags =["sensor"],
    responses={404:{"description":"Not found"}},
)
@router.get("/get/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def getSensor(id:str):
    res = await SensorService.getSensorById(id=id)
    return ResponseData(detail="Get Sensor Success",result=res)

@router.get("/getAll",response_model=ResponseData,response_model_exclude_none=True)
async def getSensors():
    res = await SensorService.getAllSensor()
    return ResponseData(detail="Get Sensor Success",result=res)

@router.post("/create",response_model=ResponseData,response_model_exclude_none=True)
async def createSensor(data:RequestSensorData):
    await SensorService.createSensor(data=data)
    return ResponseData(detail="Create Sensor Success")

@router.put("/update/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def updateSensor(id:str,data:UpdateSensorData):
    await SensorService.updateSensor(id=id,data=data)
    return ResponseData(detail="Update Sensor Success")

@router.delete("/delete/{id}",response_model=ResponseData,response_model_exclude_none=True)
async def deleteSensor(id:str):
    await SensorService.deleteSensor(id=id)
    return ResponseData(detail="Delete Sensor Success")