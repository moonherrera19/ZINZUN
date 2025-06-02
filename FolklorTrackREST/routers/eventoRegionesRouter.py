# === File: App/FolklorTrackREST/routers/eventoRegionesRouter.py ===
from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.eventoRegionesDAO import EventoRegionesDAO
from models.EventoRegionesModel import EventoRegion, EventoRegionCreate
from dao.database import ConexionSupabase
from typing import List
from auth import get_current_user

router = APIRouter(
    prefix="/evento_regiones",
    tags=["EventoRegiones"],
    dependencies=[Depends(get_current_user)]
)

def get_er_dao():
    client = ConexionSupabase().get_client()
    return EventoRegionesDAO(client)

@router.post("/", response_model=EventoRegion, status_code=status.HTTP_201_CREATED)
def assign_region(
    er: EventoRegionCreate,
    dao: EventoRegionesDAO = Depends(get_er_dao)
):
    try:
        return dao.asignar_region(er)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[EventoRegion])
def list_er(
    dao: EventoRegionesDAO = Depends(get_er_dao)
):
    try:
        return dao.listar_asignaciones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{evento_id}/{region_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_er(
    evento_id: int,
    region_id: int,
    dao: EventoRegionesDAO = Depends(get_er_dao)
):
    try:
        dao.eliminar_asignacion(evento_id, region_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
