from supabase import create_client, Client

SUPABASE_URL = "https://yclpghrhxzbdbszvvnnq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InljbHBnaHJoeHpiZGJzenZ2bm5xIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NzE2MzQ0OCwiZXhwIjoyMDYyNzM5NDQ4fQ.SfzfzJEhrSzp840PyFeEN4Ub61BOVQyqCO3xlaY1dQs"

class ConexionSupabase:
    def __init__(self):
        self.client: Client | None = None
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("Error Crítico: Las variables SUPABASE_URL y SUPABASE_KEY no pueden estar vacías en database.py.")
            return
        try:
            self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("Cliente de Supabase API inicializado correctamente (con credenciales directas).")
        except Exception as e:
            print(f"Error Crítico al inicializar el cliente de Supabase: {e}")
            self.client = None

    def get_client(self) -> Client | None:
        return self.client

    def cerrar(self):
        if self.client:
            print("Cliente de Supabase API 'cerrado' (referencia eliminada).")
        self.client = None