from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class EventoBase(BaseModel):
    titulo: str
    descripcion: str
    fecha_inicio: datetime
    fecha_fin: datetime
    lugar_nombre: str
    lugar_url: Optional[HttpUrl] = None

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    lugar_nombre: Optional[str] = None
    lugar_url: Optional[HttpUrl] = None

class Evento(EventoBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
