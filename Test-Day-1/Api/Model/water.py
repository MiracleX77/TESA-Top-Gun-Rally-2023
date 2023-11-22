from pydantic import BaseModel, Field
from datetime import datetime

class WaterData(BaseModel):
    w_date: datetime 
    w_height: float = Field(..., ge=0.0)
    w_cubic: float = Field(..., ge=0.0)
    
