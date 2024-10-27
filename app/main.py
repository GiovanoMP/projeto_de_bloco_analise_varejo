from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel
import psycopg2
import pandas as pd
import os

# Inicializa a API FastAPI
app = FastAPI()

# Carrega o modelo de ML (joblib)
modelo = load("models/customer_segments.joblib")

# Conexão com o Supabase usando variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL").replace("https://", "").replace(".supabase.co", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

conn = psycopg2.connect(
    host=SUPABASE_URL,
    port=5432,
    user="postgres",
    password=SUPABASE_KEY,
    database="postgres"
)

# Definindo o modelo de dados esperado para a API
class InputData(BaseModel):
    feature1: float
    feature2: float
    feature3: float

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/")
def previsao(dados: InputData):
    try:
        # Prepara os dados de entrada para o modelo
        entrada = [[dados.feature1, dados.feature2, dados.feature3]]
        resultado = modelo.predict(entrada)

        # Armazena a previsão no banco de dados do Supabase
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO previsoes (feature1, feature2, feature3, previsao) VALUES (%s, %s, %s, %s)",
            (dados.feature1, dados.feature2, dados.feature3, resultado[0])
        )
        conn.commit()
        cursor.close()

        return {"previsao": int(resultado[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
