from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.eventoAsignacionesDAO import EventoAsignacionesDAO
from models.EventoAsignacionesModel import EventoAsignacion, EventoAsignacionCreate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/evento_asignaciones", tags=["EventoAsignaciones"])

def get_ea_dao():
    client = ConexionSupabase().get_client()
    return EventoAsignacionesDAO(client)

@router.post("/", response_model=EventoAsignacion, status_code=status.HTTP_201_CREATED)
def assign_event(ea: EventoAsignacionCreate, dao: EventoAsignacionesDAO = Depends(get_ea_dao)):
    try:
        return dao.asignar_evento(ea)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[EventoAsignacion])
def list_ea(dao: EventoAsignacionesDAO = Depends(get_ea_dao)):
    try:
        return dao.listar_asignaciones()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{evento_id}/{alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ea(evento_id: int, alumno_id: int, dao: EventoAsignacionesDAO = Depends(get_ea_dao)):
    try:
        dao.eliminar_asignacion(evento_id, alumno_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))