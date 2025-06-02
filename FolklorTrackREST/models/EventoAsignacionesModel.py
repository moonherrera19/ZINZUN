from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventoAsignacionBase(BaseModel):
    evento_id: int
    alumno_id: int
    vestuario_id: int
    estado_participacion: str

class EventoAsignacionCreate(EventoAsignacionBase):
    pass

class EventoAsignacion(EventoAsignacionBase):
    created_at: Optional[datetime]

    class Config:
        orm_mode = True