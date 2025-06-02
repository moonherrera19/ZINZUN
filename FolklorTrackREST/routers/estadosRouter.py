from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.estadosDAO import EstadosDAO
from models.EstadoModel import Estado, EstadoCreate, EstadoUpdate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/estados", tags=["Estados"])

def get_estados_dao():
    client = ConexionSupabase().get_client()
    return EstadosDAO(client)

@router.post("/", response_model=Estado, status_code=status.HTTP_201_CREATED)
def create_estado(e: EstadoCreate, dao: EstadosDAO = Depends(get_estados_dao)):
    try:
        return dao.crear_estado(e)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Estado])
def list_estados(dao: EstadosDAO = Depends(get_estados_dao)):
    try:
        return dao.listar_estados()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{estado_id}", response_model=Estado)
def get_estado(estado_id: int, dao: EstadosDAO = Depends(get_estados_dao)):
    try:
        data = dao.obtener_estado(estado_id)
        if not data:
            raise HTTPException(status_code=404, detail="Estado no encontrado")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{estado_id}", response_model=Estado)
def update_estado(estado_id: int, e: EstadoUpdate, dao: EstadosDAO = Depends(get_estados_dao)):
    try:
        return dao.actualizar_estado(estado_id, e)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{estado_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_estado(estado_id: int, dao: EstadosDAO = Depends(get_estados_dao)):
    try:
        dao.eliminar_estado(estado_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
