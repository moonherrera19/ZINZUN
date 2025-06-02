# auth.py

from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from dao.database import ConexionSupabase
from dotenv import load_dotenv

# Carga variables de entorno desde .env (SUPABASE_URL, SUPABASE_KEY, etc.)
load_dotenv()

security = HTTPBearer()
router = APIRouter(tags=["Auth"])


# ----------------------------------------
# 1) Modelos Pydantic
# ----------------------------------------

class SignUpModel(BaseModel):
    correo: EmailStr
    contrasena: str


class LoginModel(BaseModel):
    correo: EmailStr
    contrasena: str


# ----------------------------------------
# 2) Función para instanciar el cliente de Supabase
# ----------------------------------------

def get_supabase_client():
    """
    Devuelve una instancia de Supabase client (o None si ocurre algún error).
    """
    try:
        client = ConexionSupabase().get_client()
    except Exception as e:
        print(f"[auth.py] Error al instanciar ConexionSupabase: {e}")
        return None

    return client


# ----------------------------------------
# 3) Endpoint POST /signup
#    Crea un usuario en Supabase con email y contraseña
# ----------------------------------------

@router.post(
    "/signup",
    summary="Registrar un nuevo usuario en Supabase (email + contraseña)",
    response_model=dict
)
def signup(data: SignUpModel, client=Depends(get_supabase_client)):
    """
    Crea un nuevo usuario en Supabase usando correo y contraseña.
    Retorna la info básica del usuario creado o lanza HTTPException en caso de error.
    """
    # 3.1) Verificar que el cliente no sea None
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo inicializar el cliente de Supabase (client es None). Verifica tu configuración en .env"
        )

    # 3.2) Intentar registrar el usuario en Supabase
    try:
        # Método v1.x de supabase-py:
        res = client.auth.sign_up({
            "email": data.correo,
            "password": data.contrasena
        })
    except Exception as e:
        # Si ocurre cualquier error durante la llamada a Supabase
        raise HTTPException(
            status_code=400,
            detail=f"Error al crear usuario en Supabase: {str(e)}"
        )

    # 3.3) Verificar si Supabase devolvió error de validación
    error = getattr(res, "error", None)
    if error:
        # error puede ser un dict con mensaje y status
        mensaje = error.get("message") if isinstance(error, dict) else str(error)
        raise HTTPException(
            status_code=400,
            detail=f"No se pudo crear el usuario: {mensaje}"
        )

    # 3.4) Extraer la data del usuario recién creado
    user_data = getattr(res, "data", None)
    if user_data is None:
        raise HTTPException(
            status_code=500,
            detail="No se recibió respuesta de Supabase al crear el usuario"
        )

    # 3.5) Retornar la info del usuario (puede incluir id, email, etc.)
    # Nota: Supabase devuelve en user_data un dict con keys como "user" y "session",
    # pero aquí devolvemos toda la data para que veas qué campos hay.
    return user_data


# ----------------------------------------
# 4) Endpoint POST /login
#    Autentica un usuario y devuelve un JWT
# ----------------------------------------

@router.post(
    "/login",
    summary="Autenticar usuario en Supabase y devolver access_token",
    response_model=dict
)
def login(data: LoginModel, client=Depends(get_supabase_client)):
    """
    Autentica en Supabase usando correo y contraseña.
    - Si client es None -> 500
    - Llama a sign_in_with_password (o sign_in si v0.x)
    - Si res.error existe -> 401
    - Si res.data es None -> 401 (credenciales inválidas o no confirmado)
    - Si res.data.access_token existe -> devuelve el token
    """
    # 4.1) Verificar que el cliente no sea None
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo inicializar el cliente de Supabase (client es None). Verifica tu configuración en .env"
        )

    # 4.2) Intentar iniciar sesión en Supabase
    try:
        # Método para supabase-py v1.x:
        res = client.auth.sign_in_with_password({
            "email": data.correo,
            "password": data.contrasena
        })
    except AttributeError:
        # Si sign_in_with_password no existe, probamos con la API antigua (v0.x):
        try:
            res = client.auth.sign_in(email=data.correo, password=data.contrasena)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error al comunicarse con Supabase usando sign_in: {str(e)}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al comunicarse con Supabase: {str(e)}"
        )

    # 4.3) DEBUG: imprime el objeto completo para validar qué contiene
    print(">> DEBUG login: objeto 'res' retornado por supabase:", res)

    # 4.4) Manejar posibles errores devueltos por Supabase
    error = getattr(res, "error", None)
    if error:
        mensaje = error.get("message") if isinstance(error, dict) else str(error)
        raise HTTPException(
            status_code=401,
            detail=f"Credenciales inválidas: {mensaje}"
        )

    # 4.5) Extraer la 'sesión' (res.data). Si es None, credenciales inválidas o no confirmado
    session = getattr(res, "data", None)
    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas o usuario no confirmado (res.data es None)"
        )

    # 4.6) Obtener el access_token dentro de session (en v1.x, session es un dict con "access_token")
    if isinstance(session, dict):
        access_token = session.get("access_token")
    else:
        access_token = None

    if not access_token:
        raise HTTPException(
            status_code=500,
            detail="No se obtuvo access_token desde Supabase (session['access_token'] es None)"
        )

    # 4.7) Retornar el token al cliente
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ----------------------------------------
# 5) Dependencia get_current_user para rutas protegidas
# ----------------------------------------

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    client=Depends(get_supabase_client)
):
    """
    Extrae el JWT del encabezado Authorization y lo verifica contra Supabase.
    - Si client es None -> 500
    - Llama a get_user(token). Si error o user es None -> 401.
    - Devuelve el objeto user.
    """
    # 5.1) Verificar que el cliente no sea None
    if client is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo inicializar el cliente de Supabase para verificar token"
        )

    token = credentials.credentials  # Extraer la cadena del JWT (sin "Bearer ")

    try:
        resp = client.auth.get_user(token)
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Error al verificar token en Supabase: {str(e)}"
        )

    # 5.2) Extraer error y user_data de la respuesta
    error = getattr(resp, "error", None)
    user_data = None

    if isinstance(resp, dict):
        # En algunas versiones resp puede ser un dict con 'data' y 'error'
        error = resp.get("error")
        user_data = resp.get("data", {}).get("user")
    else:
        # Más común en v1: resp es un objeto con atributos .error y .user
        user_data = getattr(resp, "user", None)

    if error:
        mensaje = error.get("message") if isinstance(error, dict) else str(error)
        raise HTTPException(status_code=401, detail=f"Auth error: {mensaje}")

    if user_data is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o token inválido")

    # Retornar el usuario autorizado (puede ser un dict con id, email, roles, etc.)
    return user_data
