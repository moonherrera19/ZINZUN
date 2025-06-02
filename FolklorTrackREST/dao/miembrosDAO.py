from dao.database import ConexionSupabase
from models.MiembrosModel import MiembroCreate, MiembroUpdate

class MiembrosDAO:
    def __init__(self, client):
        self.client = client

    def crear_miembro(self, miembro: MiembroCreate):
        data = miembro.dict()
        response = self.client.table("miembros").insert(data).execute()
        if response.error:
            raise Exception(f"Error al insertar miembro: {response.error.message}")
        return response.data[0]

    def listar_miembros(self):
        response = self.client.table("miembros").select("*").execute()
        if response.error:
            raise Exception(f"Error al listar miembros: {response.error.message}")
        return response.data

    def obtener_miembro(self, miembro_id: int):
        response = (
            self.client.table("miembros").select("*").eq("id", miembro_id).single().execute()
        )
        if response.error:
            raise Exception(f"Error al obtener miembro: {response.error.message}")
        return response.data

    def actualizar_miembro(self, miembro_id: int, miembro: MiembroUpdate):
        data = miembro.dict(exclude_unset=True)
        response = (
            self.client.table("miembros").update(data).eq("id", miembro_id).execute()
        )
        if response.error:
            raise Exception(f"Error al actualizar miembro: {response.error.message}")
        return response.data

    def eliminar_miembro(self, miembro_id: int):
        response = (
            self.client.table("miembros").delete().eq("id", miembro_id).execute()
        )
        if response.error:
            raise Exception(f"Error al eliminar miembro: {response.error.message}")
        return response.data
