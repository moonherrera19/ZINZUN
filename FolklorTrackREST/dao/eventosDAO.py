from dao.database import ConexionSupabase
from models.EventosModel import EventoCreate, EventoUpdate

class EventosDAO:
    def __init__(self, client):
        self.client = client

    def crear_evento(self, evento: EventoCreate):
        data = evento.dict()
        response = self.client.table("eventos").insert(data).execute()
        if response.error:
            raise Exception(f"Error al insertar evento: {response.error.message}")
        return response.data[0]

    def listar_eventos(self):
        response = self.client.table("eventos").select("*").execute()
        if response.error:
            raise Exception(f"Error al listar eventos: {response.error.message}")
        return response.data

    def obtener_evento(self, evento_id: int):
        response = (
            self.client.table("eventos").select("*").eq("id", evento_id).single().execute()
        )
        if response.error:
            raise Exception(f"Error al obtener evento: {response.error.message}")
        return response.data

    def actualizar_evento(self, evento_id: int, evento: EventoUpdate):
        data = evento.dict(exclude_unset=True)
        response = (
            self.client.table("eventos").update(data).eq("id", evento_id).execute()
        )
        if response.error:
            raise Exception(f"Error al actualizar evento: {response.error.message}")
        return response.data

    def eliminar_evento(self, evento_id: int):
        response = (
            self.client.table("eventos").delete().eq("id", evento_id).execute()
        )
        if response.error:
            raise Exception(f"Error al eliminar evento: {response.error.message}")
        return response.data
