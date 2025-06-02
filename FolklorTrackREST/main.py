# main.py

import uvicorn
from fastapi import FastAPI, Depends
from dao.database import ConexionSupabase
from auth import get_current_user  # Dependencia para rutas protegidas

# Routers de autenticación y recursos
from auth import router as auth_router
from routers.miembrosRouter import router as miembros_router
from routers.eventosRouter import router as eventos_router
from routers.vestuariosRouter import router as vestuarios_router
from routers.regionesRouter import router as regiones_router
from routers.estadosRouter import router as estados_router
from routers.eventoRegionesRouter import router as evento_regiones_router
from routers.eventoAsignacionesRouter import router as evento_asignaciones_router

# Creamos la aplicación FastAPI sin protección global,
# para que el endpoint /login quede accesible sin token.
app = FastAPI(title="FolklorTrack API")


# ----------------------------------------------------------
# 1) Evento de arranque: inicializar el cliente Supabase
# ----------------------------------------------------------
@app.on_event("startup")
async def startup():
    conexion = ConexionSupabase()
    client = conexion.get_client()
    if not client:
        raise RuntimeError("No se pudo conectar a Supabase")
    # Guardamos el cliente en el state de la app
    app.state.supabase_client = client


# ----------------------------------------------------------
# 2) Evento de apagado: limpiar el cliente Supabase
# ----------------------------------------------------------
@app.on_event("shutdown")
async def shutdown():
    app.state.supabase_client = None


# ----------------------------------------------------------
# 3) Ruta pública: home (requiere autenticación opcionalmente)
# ----------------------------------------------------------
@app.get("/", summary="Página de inicio")
async def home():
    return {"mensaje": "Bienvenido a FolklorTrack API"}


# ----------------------------------------------------------
# 4) Incluir el router de Auth (login) SIN protección
#    Esto permitirá obtener el JWT en /login.
# ----------------------------------------------------------
app.include_router(
    auth_router,
    prefix="",         # Se registrará en la raíz: POST /login
    tags=["Auth"]
)


# ----------------------------------------------------------
# 5) Incluir routers de recursos PROTEGIDOS por JWT
#    Cada router está “montado” con la dependencia get_current_user
#    para exigir token en todas sus rutas internas.
# ----------------------------------------------------------

# Miembros
app.include_router(
    miembros_router,
    prefix="/miembros",
    tags=["Miembros"],
    dependencies=[Depends(get_current_user)]
)

# Eventos
app.include_router(
    eventos_router,
    prefix="/eventos",
    tags=["Eventos"],
    dependencies=[Depends(get_current_user)]
)

# Vestuarios
app.include_router(
    vestuarios_router,
    prefix="/vestuarios",
    tags=["Vestuarios"],
    dependencies=[Depends(get_current_user)]
)

# Regiones
app.include_router(
    regiones_router,
    prefix="/regiones",
    tags=["Regiones"],
    dependencies=[Depends(get_current_user)]
)

# Estados
app.include_router(
    estados_router,
    prefix="/estados",
    tags=["Estados"],
    dependencies=[Depends(get_current_user)]
)

# EventoRegiones
app.include_router(
    evento_regiones_router,
    prefix="/evento_regiones",
    tags=["EventoRegiones"],
    dependencies=[Depends(get_current_user)]
)

# EventoAsignaciones
app.include_router(
    evento_asignaciones_router,
    prefix="/evento_asignaciones",
    tags=["EventoAsignaciones"],
    dependencies=[Depends(get_current_user)]
)


# ----------------------------------------------------------
# 6) Punto de entrada: arrancar Uvicorn
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
