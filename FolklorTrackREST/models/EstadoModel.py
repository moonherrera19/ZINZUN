from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EstadoBase(BaseModel):
    nombre_estado: str = Field(..., example="Michoacán")
    img_estado_url: Optional[str] = Field(None, example="https://tusitio.com/imagenes/michoacan.png")

class EstadoCreate(EstadoBase):
    pass

class EstadoUpdate(BaseModel):
    nombre_estado: Optional[str] = Field(None, example="Michoacán")
    img_estado_url: Optional[str] = Field(None, example="https://tusitio.com/imagenes/michoacan.png")

class Estado(EstadoBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
