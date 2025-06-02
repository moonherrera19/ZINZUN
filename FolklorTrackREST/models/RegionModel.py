from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class RegionBase(BaseModel):
    nombre_region: str
    img_region_url: Optional[str] = None
    estado_id: int

class RegionCreate(RegionBase):
    pass

class RegionUpdate(BaseModel):
    nombre_region: Optional[str] = None
    img_region_url: Optional[HttpUrl] = None
    estado_id: Optional[int] = None

class Region(RegionBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
