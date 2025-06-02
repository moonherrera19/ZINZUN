from dao.database import ConexionSupabase
from models.VestuarioModel import VestuarioCreate, VestuarioUpdate

class VestuariosDAO:
    def __init__(self, client):
        self.client = client

    def crear_vestuario(self, vestuario: VestuarioCreate):
        data = vestuario.dict()
        response = self.client.table("vestuarios").insert(data).execute()
        if response.error:
            raise Exception(f"Error al insertar vestuario: {response.error.message}")
        return response.data[0]

    def listar_vestuarios(self):
        response = self.client.table("vestuarios").select("*").execute()
        if response.error:
            raise Exception(f"Error al listar vestuarios: {response.error.message}")
        return response.data

    def obtener_vestuario(self, vestuario_id: int):
        response = (
            self.client.table("vestuarios").select("*").eq("id", vestuario_id).single().execute()
        )
        if response.error:
            raise Exception(f"Error al obtener vestuario: {response.error.message}")
        return response.data

    def actualizar_vestuario(self, vestuario_id: int, vestuario: VestuarioUpdate):
        data = vestuario.dict(exclude_unset=True)
        response = (
            self.client.table("vestuarios").update(data).eq("id", vestuario_id).execute()
        )
        if response.error:
            raise Exception(f"Error al actualizar vestuario: {response.error.message}")
        return response.data

    def eliminar_vestuario(self, vestuario_id: int):
        response = (
            self.client.table("vestuarios").delete().eq("id", vestuario_id).execute()
        )
        if response.error:
            raise Exception(f"Error al eliminar vestuario: {response.error.message}")
        return response.data
