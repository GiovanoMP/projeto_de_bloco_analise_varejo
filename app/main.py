import os
from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect, OperationalError
from supabase import create_client, Client

app = FastAPI()

# Variáveis de ambiente
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
PORT = int(os.getenv("PORT", 8000))  # Pega a porta da variável de ambiente

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_API_KEY não configuradas corretamente.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    conn = connect(
        host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
        port=5432,
        user="postgres",
        password=SUPABASE_KEY,
        database="postgres"
    )
except OperationalError as e:
    raise HTTPException(status_code=500, detail=f"Erro na conexão: {str(e)}")

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/previsao/")
async def previsao(dados: dict):
    try:
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
        resultado = modelo.predict(features)

        with open("documents/analise_detalhada_clientes.txt", "w", encoding="utf-8") as f:
            f.write(f"Previsão realizada: {int(resultado[0])}\n")

        with open("documents/analise_detalhada_clientes.txt", "rb") as file:
            supabase.storage.from_('documents').upload(
                "analise_detalhada_clientes.txt", file.read()
            )

        return {"previsao": int(resultado[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na previsão: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
