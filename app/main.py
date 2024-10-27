import os
from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect, OperationalError
from supabase import create_client, Client

# Inicializa a API FastAPI
app = FastAPI()

# Carrega variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")  # Deve incluir https:// e .supabase.co
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

# Verifica se as variáveis de ambiente foram definidas
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_API_KEY não configuradas corretamente.")

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Carrega o modelo de machine learning
modelo = load("models/customer_segments.joblib")

try:
    # Conecta ao banco de dados do Supabase
    conn = connect(
        host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
        port=5432,
        user="postgres",
        password=SUPABASE_KEY,
        database="postgres"
    )
except OperationalError as e:
    raise HTTPException(status_code=500, detail=f"Erro na conexão com o banco de dados: {str(e)}")

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/")
async def previsao(dados: dict):
    try:
        # Extrai as features necessárias para o modelo
        features = [[
            dados.get("NumeroFatura", 0),
            dados.get("CodigoProduto", 0),
            dados.get("Quantidade", 0),
            dados.get("PrecoUnitario", 0),
            dados.get("Ano", 0),
            dados.get("Mes", 0),
            dados.get("Dia", 0),
            dados.get("SemanaAno", 0),
            dados.get("ValorTotalFatura", 0)
        ]]

        # Faz a previsão com o modelo carregado
        resultado = modelo.predict(features)

        # Cria o relatório em formato TXT
        with open("documents/analise_detalhada_clientes.txt", "w", encoding="utf-8") as f:
            f.write(f"Previsão realizada com sucesso!\nResultado: {int(resultado[0])}\n")

        # Upload do relatório para o Supabase Storage (Bucket: documents)
        with open("documents/analise_detalhada_clientes.txt", "rb") as file:
            supabase.storage.from_('documents').upload(
                "analise_detalhada_clientes.txt", file.read()
            )

        return {"previsao": int(resultado[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao realizar previsão: {str(e)}")
