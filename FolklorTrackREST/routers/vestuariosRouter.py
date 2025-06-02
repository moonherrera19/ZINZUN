from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.vestuariosDAO import VestuariosDAO
from models.VestuarioModel import Vestuario, VestuarioCreate, VestuarioUpdate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/vestuarios", tags=["Vestuarios"])

def get_vestuarios_dao():
    client = ConexionSupabase().get_client()
    return VestuariosDAO(client)

@router.post("/", response_model=Vestuario, status_code=status.HTTP_201_CREATED)
def create_vestuario(v: VestuarioCreate, dao: VestuariosDAO = Depends(get_vestuarios_dao)):
    try:
        return dao.crear_vestuario(v)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Vestuario])
def list_vestuarios(dao: VestuariosDAO = Depends(get_vestuarios_dao)):
    try:
        return dao.listar_vestuarios()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{vestuario_id}", response_model=Vestuario)
def get_vestuario(vestuario_id: int, dao: VestuariosDAO = Depends(get_vestuarios_dao)):
    try:
        data = dao.obtener_vestuario(vestuario_id)
        if not data:
            raise HTTPException(status_code=404, detail="Vestuario no encontrado")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{vestuario_id}", response_model=Vestuario)
def update_vestuario(vestuario_id: int, v: VestuarioUpdate, dao: VestuariosDAO = Depends(get_vestuarios_dao)):
    try:
        return dao.actualizar_vestuario(vestuario_id, v)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{vestuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vestuario(vestuario_id: int, dao: VestuariosDAO = Depends(get_vestuarios_dao)):
    try:
        dao.eliminar_vestuario(vestuario_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
