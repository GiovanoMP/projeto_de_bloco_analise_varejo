from fastapi import FastAPI, HTTPException, Request
from joblib import load
from psycopg2 import connect
import os
import json

# Inicializa a API FastAPI
app = FastAPI()

# Carrega o modelo de ML (joblib)
modelo = load("models/customer_segments.joblib")

# Conexão com o banco de dados Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL").replace("https://", "").replace(".supabase.co", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

conn = connect(
    host=SUPABASE_URL,
    port=5432,
    user="postgres",
    password=SUPABASE_KEY,
    database="postgres"
)

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/")
async def previsao(request: Request):
    try:
        # Recebe os dados dinâmicos enviados pelo cliente
        dados = await request.json()
        
        # Extrai as features para o modelo (ajuste conforme necessário)
        features = [[dados.get("feature1", 0), dados.get("feature2", 0), dados.get("feature3", 0)]]
        resultado = modelo.predict(features)

        # Gera o comando SQL dinamicamente com base nos dados recebidos
        colunas = ', '.join(dados.keys()) + ', previsao'
        valores = ', '.join(['%s'] * (len(dados) + 1))

        # Executa o comando SQL para inserir a previsão e os dados recebidos
        cursor = conn.cursor()
        cursor.execute(
            f"INSERT INTO previsoes ({colunas}) VALUES ({valores})",
            list(dados.values()) + [int(resultado[0])]
        )
        conn.commit()
        cursor.close()

        return {"previsao": int(resultado[0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
