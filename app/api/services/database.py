from supabase import create_client
from ..config.settings import SUPABASE_URL, SUPABASE_API_KEY

def get_supabase_client():
    """Retorna uma instância do cliente Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_API_KEY)
