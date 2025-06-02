from dao.database import ConexionSupabase
from models.EventoAsignacionesModel import EventoAsignacionCreate

class EventoAsignacionesDAO:
    def __init__(self, client):
        self.client = client

    def asignar_evento(self, ea: EventoAsignacionCreate):
        data = ea.dict()
        response = self.client.table("evento_asignaciones").insert(data).execute()
        if response.error:
            raise Exception(f"Error al asignar evento: {response.error.message}")
        return response.data[0]

    def listar_asignaciones(self):
        response = self.client.table("evento_asignaciones").select("*").execute()
        if response.error:
            raise Exception(f"Error al listar asignaciones: {response.error.message}")
        return response.data

    def eliminar_asignacion(self, evento_id: int, alumno_id: int):
        response = (
            self.client.table("evento_asignaciones").delete()
            .eq("evento_id", evento_id)
            .eq("alumno_id", alumno_id)
            .execute()
        )
        if response.error:
            raise Exception(f"Error al eliminar asignación: {response.error.message}")
        return response.data
