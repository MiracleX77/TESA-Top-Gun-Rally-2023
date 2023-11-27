from pydantic import BaseModel, Field
from datetime import datetime

class WaterData(BaseModel):
    sensor_id : int = Field(..., ge=0)
    water_height: float = Field(..., ge=0.0)
    create_on: datetime = datetime.now()
    status: str 
    


class RequestWaterData(BaseModel):
    sensor_id : int = Field(..., ge=0)
    water_height: float = Field(..., ge=0.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": 1,
                "water_height": 1.0
            }
        }
class LastWaterData(BaseModel):
    sensor_id : int = Field(..., ge=1)
    count_data: int = Field(..., ge=1)

    class Config:
        json_schema_extra = {
            "example": {
                "sensor_id": 1,
                "count_data": 1,
            }
        }