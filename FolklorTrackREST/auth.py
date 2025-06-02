from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dao.database import ConexionSupabase

security = HTTPBearer()

def get_supabase_client():
    return ConexionSupabase().get_client()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    client=Depends(get_supabase_client)
):
    token = credentials.credentials
    try:
        # En supabase-py v1: se usa auth.get_user
        resp = client.auth.get_user(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error al verificar token: {str(e)}")

    # resp es típicamente un dict con keys 'data' y 'error'
    error = resp.get('error') if isinstance(resp, dict) else getattr(resp, 'error', None)
    user = None
    if isinstance(resp, dict):
        user = resp.get('data', {}).get('user')
    else:
        # en caso de respuesta tipo object
        user = getattr(resp, 'user', None)

    if error:
        msg = error.message if hasattr(error, 'message') else str(error)
        raise HTTPException(status_code=401, detail=f"Auth error: {msg}")
    if not user:
        raise HTTPException(status_code=401, detail="El usuario no fue encontrado")

    return user
