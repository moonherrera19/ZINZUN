from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventoRegionBase(BaseModel):
    evento_id: int
    region_id: int

class EventoRegionCreate(EventoRegionBase):
    pass

class EventoRegion(EventoRegionBase):
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
