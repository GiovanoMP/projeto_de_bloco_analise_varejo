from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Configurações da API
API_VERSION = "1.0.0"
API_TITLE = "Analytics Dashboard API"
API_DESCRIPTION = "API para fornecer dados analíticos ao dashboard"
