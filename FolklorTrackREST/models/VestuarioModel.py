from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class VestuarioBase(BaseModel):
    folio: str
    nombre: str
    tipo: str
    talla: str
    genero: str
    disponibilidad: bool
    region_id: int
    img_vestuario_url: Optional[HttpUrl] = None

class VestuarioCreate(VestuarioBase):
    pass

class VestuarioUpdate(BaseModel):
    folio: Optional[str] = None
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    talla: Optional[str] = None
    genero: Optional[str] = None
    disponibilidad: Optional[bool] = None
    region_id: Optional[int] = None
    img_vestuario_url: Optional[HttpUrl] = None

class Vestuario(VestuarioBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
