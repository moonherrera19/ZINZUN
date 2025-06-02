from dao.database import ConexionSupabase
from models.EstadoModel import EstadoCreate, EstadoUpdate

class EstadosDAO:
    def __init__(self, client):
        self.client = client

    def crear_estado(self, estado: EstadoCreate):
        payload = estado.dict()
        resp = self.client.table("estados").insert(payload).execute()
        # comprueba status_code en lugar de response.error
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al insertar estado: {resp.data}")
        return resp.data[0]

    def listar_estados(self):
        resp = self.client.table("estados").select("*").execute()
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al listar estados: {resp.data}")
        return resp.data

    def obtener_estado(self, estado_id: int):
        resp = (
            self.client.table("estados")
                .select("*")
                .eq("id", estado_id)
                .single()
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al obtener estado: {resp.data}")
        return resp.data

    def actualizar_estado(self, estado_id: int, estado: EstadoUpdate):
        data = estado.dict(exclude_unset=True)
        resp = (
            self.client.table("estados")
                .update(data)
                .eq("id", estado_id)
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al actualizar estado: {resp.data}")
        return resp.data

    def eliminar_estado(self, estado_id: int):
        resp = (
            self.client.table("estados")
                .delete()
                .eq("id", estado_id)
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al eliminar estado: {resp.data}")
        return resp.data
