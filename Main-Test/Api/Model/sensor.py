from pydantic import BaseModel, Field
from datetime import datetime

class SensorData(BaseModel):
    sensor_id : int = Field(..., ge=0)
    name : str
    lat: str
    long: str 
    create_on : datetime = datetime.now()
    update_on : datetime = datetime.now()
    status: str = "ACTIVE" 


    


class RequestSensorData(BaseModel):
    sensor_id : int = Field(..., ge=0)
    name : str
    lat: str
    long: str 
    
    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": 1,
                "name": "sensor1",
                "lat": "13.123456",
                "long": "100.123456",
            }
        }
    

class UpdateSensorData(BaseModel):
    name : str
    lat: str | None
    long: str | None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "sensor1",
                "lat": "13.123456",
                "long": "100.123456",
            }
        }