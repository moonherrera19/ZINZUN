from dao.database import ConexionSupabase
from models.EventoRegionesModel import EventoRegionCreate

class EventoRegionesDAO:
    def __init__(self, client):
        self.client = client

    def asignar_region(self, er: EventoRegionCreate):
        data = er.dict()
        response = self.client.table("evento_regiones").insert(data).execute()
        if response.error:
            raise Exception(f"Error al asignar región a evento: {response.error.message}")
        return response.data[0]

    def listar_asignaciones(self):
        response = self.client.table("evento_regiones").select("*").execute()
        if response.error:
            raise Exception(f"Error al listar asignaciones: {response.error.message}")
        return response.data

    def eliminar_asignacion(self, evento_id: int, region_id: int):
        response = (
            self.client.table("evento_regiones").delete()
            .eq("evento_id", evento_id)
            .eq("region_id", region_id)
            .execute()
        )
        if response.error:
            raise Exception(f"Error al eliminar asignación: {response.error.message}")
        return response.data
