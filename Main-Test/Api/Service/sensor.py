import json
from fastapi import HTTPException
from Repository.sensor import SensorRepository
from Model.sensor import SensorData, RequestSensorData,UpdateSensorData



class SensorService:
    @staticmethod
    async def getSensorById(id:str):
        sensor = await SensorRepository.getOneById(id=int(id))
        if sensor:
            sensor= json.loads(json.dumps(sensor,default=str))
            return sensor
        else:
            raise HTTPException(status_code=400,detail="Sensor Not Found")
    
    @staticmethod
    async def getAllSensor():
        sensors = await SensorRepository.getAll()
        if sensors:
            list_sensor = []
            for sensor in sensors:
                sensor= json.loads(json.dumps(sensor,default=str))
                list_sensor.append(sensor)
            return list_sensor
        else:
            raise HTTPException(status_code=400,detail="Sensor Not Found")
        
        
    @staticmethod
    async def createSensor(data:RequestSensorData):
        check = await SensorRepository.getOneById(id=data.sensor_id)
        if check:
            raise HTTPException(status_code=400,detail="Sensor Already Exist")
        data_insert = SensorData(
            sensor_id = data.sensor_id,
            name = data.name,
            lat = data.lat,
            long = data.long,
        )
        water = await SensorRepository.create(data=data_insert)
        if water:
            return water
        else:
            raise HTTPException(status_code=400,detail="Sensor Not Found")
        
    @staticmethod  
    async def updateSensor(id:str,data:UpdateSensorData):        
        check = await SensorRepository.update(id=int(id),data=data)
        if check:
            return check
        else:
            raise HTTPException(status_code=400,detail="Sensor Not Found")

    @staticmethod
    async def updateTimeSensor(id:int):
        check = await SensorRepository.updateTime(id=id)
        if check:
            return True
        else:
            return False
    @staticmethod
    async def updateStatusSensor(id:int,status:str):
        check = await SensorRepository.updateStatus(id=id,status=status)
        if check:
            return True
        else:
            return False
        
    @staticmethod
    async def deleteSensor(id:str):
        check = await SensorRepository.delete(id=int(id))
        if check:
            return True
        else:
            raise HTTPException(status_code=400,detail="Sensor Not Found")