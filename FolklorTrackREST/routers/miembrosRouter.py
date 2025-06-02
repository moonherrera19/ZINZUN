# App/FolklorTrackREST/routers/miembrosRouter.py

from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List

from auth import get_current_user
from dao.database import ConexionSupabase
from dao.miembrosDAO import MiembrosDAO
from models.MiembrosModel import Miembro, MiembroCreate, MiembroUpdate

router = APIRouter(
    prefix="/miembros",
    tags=["Miembros"],
    dependencies=[Depends(get_current_user)],
)

def get_miembros_dao():
    client = ConexionSupabase().get_client()
    return MiembrosDAO(client)

@router.post("/", response_model=Miembro, status_code=status.HTTP_201_CREATED)
def create_member(
    miembro: MiembroCreate,
    dao: MiembrosDAO = Depends(get_miembros_dao),
):
    try:
        return dao.crear_miembro(miembro)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Miembro])
def list_members(dao: MiembrosDAO = Depends(get_miembros_dao)):
    try:
        return dao.listar_miembros()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{miembro_id}", response_model=Miembro)
def get_member(
    miembro_id: int,
    dao: MiembrosDAO = Depends(get_miembros_dao),
):
    try:
        data = dao.obtener_miembro(miembro_id)
        if not data:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{miembro_id}", response_model=Miembro)
def update_member(
    miembro_id: int,
    miembro: MiembroUpdate,
    dao: MiembrosDAO = Depends(get_miembros_dao),
):
    try:
        return dao.actualizar_miembro(miembro_id, miembro)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{miembro_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(
    miembro_id: int,
    dao: MiembrosDAO = Depends(get_miembros_dao),
):
    try:
        dao.eliminar_miembro(miembro_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
