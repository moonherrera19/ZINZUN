from pydantic import BaseModel, EmailStr
from typing import Optional

class MiembroBase(BaseModel):
    correo: EmailStr
    nombre: str
    rol: str

class MiembroCreate(MiembroBase):
    contrasena: str

class MiembroUpdate(BaseModel):
    correo: Optional[EmailStr] = None
    nombre: Optional[str] = None
    rol: Optional[str] = None
    contrasena: Optional[str] = None

class Miembro(MiembroBase):
    id: int

    class Config:
        orm_mode = True