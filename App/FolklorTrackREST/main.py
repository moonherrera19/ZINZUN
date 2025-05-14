import uvicorn
from fastapi import FastAPI

from dao.database import ConexionSupabase

app = FastAPI(
    title="FolklorTrack API"
)

@app.get("/")
async def home():
    salida={"mensaje": "Bienvenido a FolklorTrack"}
    return salida

@app.on_event("startup")
async def startup():
    print("INFO:     Iniciando aplicación FolklorTrack API...")
    print("INFO:     Inicializando conexión con Supabase...")

    conexion_supabase_instance = ConexionSupabase()
    app.state.supabase_client = conexion_supabase_instance.get_client()

    if app.state.supabase_client is None:
        print("ERROR:    No se pudo inicializar el cliente de Supabase. "
              "Verifique las variables de entorno SUPABASE_URL y SUPABASE_SERVICE_KEY.")
    else:
        print("INFO: Cliente de Supabase inicializado y disponible en app.state.supabase_client")

@app.on_event("shutdown")
async def shutdown():
    print("INFO: Cerrando la aplicación FolklorTrack API...")
    print("INFO: Conexión con Supabase (simbólicamente) finalizada.")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )