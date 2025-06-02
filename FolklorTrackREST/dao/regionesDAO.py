from dao.database import ConexionSupabase
from models.RegionModel import RegionCreate, RegionUpdate

class RegionesDAO:
    def __init__(self, client):
        self.client = client

    def crear_region(self, region: RegionCreate):
        data = region.dict()
        resp = self.client.table("regiones").insert(data).execute()
        # supabase-py ya no expone response.error: usamos status_code
        if getattr(resp, "status_code", 0) >= 400:
            # resp.data contendrá el detalle de error
            raise Exception(f"Error al insertar región: {resp.data}")
        return resp.data[0]

    def listar_regiones(self):
        resp = self.client.table("regiones").select("*").execute()
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al listar regiones: {resp.data}")
        return resp.data

    def obtener_region(self, region_id: int):
        resp = (
            self.client.table("regiones")
                .select("*")
                .eq("id", region_id)
                .single()
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al obtener región: {resp.data}")
        return resp.data

    def actualizar_region(self, region_id: int, region: RegionUpdate):
        data = region.dict(exclude_unset=True)
        resp = (
            self.client.table("regiones")
                .update(data)
                .eq("id", region_id)
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al actualizar región: {resp.data}")
        return resp.data

    def eliminar_region(self, region_id: int):
        resp = (
            self.client.table("regiones")
                .delete()
                .eq("id", region_id)
                .execute()
        )
        if getattr(resp, "status_code", 0) >= 400:
            raise Exception(f"Error al eliminar región: {resp.data}")
        return resp.data
