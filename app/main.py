import os
from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa a API FastAPI
app = FastAPI()

# Carrega as variáveis do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# Verifica se as variáveis foram carregadas corretamente
if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_API_KEY não configuradas corretamente.")

# Inicializa o cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Conexão com o banco de dados
conn = connect(
    host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
    port=5432,
    user="postgres",
    password=SUPABASE_API_KEY,
    database="postgres"
)

# Carrega o modelo treinado
modelo = load("models/customer_segments.joblib")

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/")
async def previsao():
    try:
        # Lógica do modelo e geração de previsões
        resultado = {"mensagem": "Modelo executado com sucesso!"}

        # Salvando o relatório no Supabase
        bucket_name = "documents"
        with open("documents/analise_detalhada_clientes.txt", "rb") as f:
            supabase.storage.from_(bucket_name).upload("analise_detalhada_clientes.txt", f)

        return resultado

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
