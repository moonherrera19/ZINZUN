from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.regionesDAO import RegionesDAO
from models.RegionModel import Region, RegionCreate, RegionUpdate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/regiones", tags=["Regiones"])

def get_regiones_dao():
    client = ConexionSupabase().get_client()
    return RegionesDAO(client)

@router.post("/", response_model=Region, status_code=status.HTTP_201_CREATED)
def create_region(r: RegionCreate, dao: RegionesDAO = Depends(get_regiones_dao)):
    try:
        return dao.crear_region(r)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Region])
def list_regiones(dao: RegionesDAO = Depends(get_regiones_dao)):
    try:
        return dao.listar_regiones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{region_id}", response_model=Region)
def get_region(region_id: int, dao: RegionesDAO = Depends(get_regiones_dao)):
    try:
        data = dao.obtener_region(region_id)
        if not data:
            raise HTTPException(status_code=404, detail="Región no encontrada")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{region_id}", response_model=Region)
def update_region(region_id: int, r: RegionUpdate, dao: RegionesDAO = Depends(get_regiones_dao)):
    try:
        return dao.actualizar_region(region_id, r)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_region(region_id: int, dao: RegionesDAO = Depends(get_regiones_dao)):
    try:
        dao.eliminar_region(region_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

