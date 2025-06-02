from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.eventosDAO import EventosDAO
from models.EventosModel import Evento, EventoCreate, EventoUpdate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/eventos", tags=["Eventos"])

def get_eventos_dao():
    client = ConexionSupabase().get_client()
    return EventosDAO(client)

@router.post("/", response_model=Evento, status_code=status.HTTP_201_CREATED)
def create_event(evento: EventoCreate, dao: EventosDAO = Depends(get_eventos_dao)):
    try:
        return dao.crear_evento(evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Evento])
def list_events(dao: EventosDAO = Depends(get_eventos_dao)):
    try:
        return dao.listar_eventos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{evento_id}", response_model=Evento)
def get_event(evento_id: int, dao: EventosDAO = Depends(get_eventos_dao)):
    try:
        data = dao.obtener_evento(evento_id)
        if not data:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{evento_id}", response_model=Evento)
def update_event(evento_id: int, evento: EventoUpdate, dao: EventosDAO = Depends(get_eventos_dao)):
    try:
        return dao.actualizar_evento(evento_id, evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(evento_id: int, dao: EventosDAO = Depends(get_eventos_dao)):
    try:
        dao.eliminar_evento(evento_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))