from fastapi import APIRouter, Depends, HTTPException, status, Response
from dao.alumnosDAO import AlumnosDAO
from models.AlumnoModel import Alumno, AlumnoCreate, AlumnoUpdate
from dao.database import ConexionSupabase
from typing import List

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

def get_alumnos_dao():
    client = ConexionSupabase().get_client()
    return AlumnosDAO(client)

@router.post("/", response_model=Alumno, status_code=status.HTTP_201_CREATED)
def create_alumno(a: AlumnoCreate, dao: AlumnosDAO = Depends(get_alumnos_dao)):
    try:
        return dao.crear_alumno(a)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[Alumno])
def list_alumnos(dao: AlumnosDAO = Depends(get_alumnos_dao)):
    try:
        return dao.listar_alumnos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{alumno_id}", response_model=Alumno)
def get_alumno(alumno_id: int, dao: AlumnosDAO = Depends(get_alumnos_dao)):
    try:
        data = dao.obtener_alumno(alumno_id)
        if not data:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")
        return data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{alumno_id}", response_model=Alumno)
def update_alumno(alumno_id: int, a: AlumnoUpdate, dao: AlumnosDAO = Depends(get_alumnos_dao)):
    try:
        return dao.actualizar_alumno(alumno_id, a)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_alumno(alumno_id: int, dao: AlumnosDAO = Depends(get_alumnos_dao)):
    try:
        dao.eliminar_alumno(alumno_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))