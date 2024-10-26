from fastapi import FastAPI
from joblib import load

app = FastAPI()

# Carregar o modelo de ML
modelo = load("models/customer_segments.joblib")

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/{client_id}")
def previsao(client_id: str):
    previsao = modelo.predict([[5, 10, 100]])
    return {"client_id": client_id, "previsao": int(previsao[0])}
