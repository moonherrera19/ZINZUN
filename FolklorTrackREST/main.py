import uvicorn
from fastapi import FastAPI, Depends
from dao.database import ConexionSupabase
from auth import get_current_user

# Routers
from routers.miembrosRouter import router as miembros_router
from routers.eventosRouter import router as eventos_router
from routers.vestuariosRouter import router as vestuarios_router
from routers.regionesRouter import router as regiones_router
from routers.estadosRouter import router as estados_router
from routers.eventoRegionesRouter import router as evento_regiones_router
from routers.eventoAsignacionesRouter import router as evento_asignaciones_router

app = FastAPI(
    title="FolklorTrack API",
    dependencies=[Depends(get_current_user)]  # Protección global con Supabase Auth
)

@app.get("/", dependencies=[Depends(get_current_user)])
async def home():
    return {"mensaje": "Bienvenido a FolklorTrack"}

@app.on_event("startup")
async def startup():
    conexion = ConexionSupabase()
    client = conexion.get_client()
    if not client:
        raise RuntimeError("No se pudo conectar a Supabase")
    app.state.supabase_client = client

@app.on_event("shutdown")
async def shutdown():
    app.state.supabase_client = None

# Incluir routers protegidos
app.include_router(miembros_router)
app.include_router(eventos_router)
app.include_router(vestuarios_router)
app.include_router(regiones_router)
app.include_router(estados_router)
app.include_router(evento_regiones_router)
app.include_router(evento_asignaciones_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True
    )