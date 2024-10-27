import os
from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect
from supabase import create_client, Client

# Inicializa a API FastAPI
app = FastAPI()

# Verifica se as variáveis de ambiente estão disponíveis
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_KEY não configuradas corretamente.")

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Conexão com o banco de dados Supabase
conn = connect(
    host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
    port=5432,
    user="postgres",
    password=SUPABASE_KEY,
    database="postgres"
)

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}
