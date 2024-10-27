from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect
from supabase import create_client, Client
import os
import pandas as pd

# Inicializa a API FastAPI
app = FastAPI()

# Carrega o modelo de ML
modelo = load("models/customer_segments.joblib")

# Conexão com o Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Conexão com o banco de dados Postgres no Supabase
conn = connect(
    host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
    port=5432,
    user="postgres",
    password=SUPABASE_KEY,
    database="postgres"
)

# Função para carregar todas as tabelas como um DataFrame único
def carregar_dados():
    query = """
    SELECT NumeroFatura, CodigoProduto, Descricao, Quantidade, DataFatura,
           PrecoUnitario, IDCliente, Pais, CategoriaProduto, CategoriaPreco,
           Ano, Mes, Dia, DiaSemana, SemanaAno, ValorTotalFatura, FaturaUnica
    FROM transacoes;
    """  # Ajuste se necessário para diferentes tabelas
    df = pd.read_sql(query, conn)
    return df

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.get("/executar_modelo/")
def executar_modelo():
    try:
        # Carrega os dados consolidados
        dados = carregar_dados()

        # Prepara as features para o modelo
        features = dados[['Quantidade', 'PrecoUnitario', 'ValorTotalFatura']]  # Ajuste conforme necessário
        previsoes = modelo.predict(features)

        # Adiciona as previsões aos dados originais
        dados["Previsao"] = previsoes

        # Gera o relatório de insights
        relatorio_path = "analise_detalhada_clientes.txt"
        with open(relatorio_path, "w", encoding="utf-8") as f:
            f.write("=== RELATÓRIO COMPLETO DE INSIGHTS ===\n\n")
            f.write(f"Total de registros: {len(dados)}\n")
            f.write("Resumo das Previsões:\n")
            f.write(dados["Previsao"].value_counts().to_string())

        # Faz o upload do relatório para o bucket 'documents'
        with open(relatorio_path, "rb") as f:
            res = supabase.storage().from_("documents").upload(
                relatorio_path, f
            )

        if res.get("error"):
            raise Exception(f"Erro ao enviar o arquivo: {res['error']}")

        return {
            "mensagem": "Modelo executado e relatório enviado com sucesso!",
            "arquivo": relatorio_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
