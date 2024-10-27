import os
from fastapi import FastAPI, HTTPException
from joblib import load
from psycopg2 import connect
from supabase import create_client, Client
import pandas as pd
from io import StringIO

# Inicializa a API FastAPI
app = FastAPI()

# Variáveis de ambiente do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL ou SUPABASE_KEY não configuradas corretamente.")

# Inicializa o cliente do Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Conexão ao banco de dados Supabase
conn = connect(
    host=SUPABASE_URL.replace("https://", "").replace(".supabase.co", ""),
    port=5432,
    user="postgres",
    password=SUPABASE_KEY,
    database="postgres"
)

# Carrega o modelo de Machine Learning treinado
modelo = load("models/customer_segments.joblib")

# Função para carregar todas as colunas relevantes do banco de dados
def carregar_dados():
    query = """
        SELECT NumeroFatura, CodigoProduto, Descricao, Quantidade, 
               DataFatura, PrecoUnitario, IDCliente, Pais, 
               CategoriaProduto, CategoriaPreco, Ano, Mes, Dia, 
               DiaSemana, SemanaAno, ValorTotalFatura, FaturaUnica
        FROM transacoes_final;
    """
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar dados: {str(e)}")

# Função para gerar relatório TXT e enviar para o bucket do Supabase
def gerar_relatorio_txt(df, resultados):
    try:
        # Gera o conteúdo do relatório
        buffer = StringIO()
        buffer.write("=== Relatório de Previsão ===\n")
        buffer.write(f"Data: {pd.Timestamp.now()}\n")
        buffer.write("=" * 50 + "\n")
        buffer.write(f"Total de registros processados: {len(df)}\n\n")

        # Adiciona as previsões no relatório
        for i, (index, row) in enumerate(df.iterrows()):
            buffer.write(
                f"Registro {i + 1} | Cliente: {row['IDCliente']} | "
                f"Previsão: {resultados[i]}\n"
            )

        # Envia o relatório para o bucket do Supabase
        bucket_path = f"relatorios/analise_previsao_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.txt"
        buffer.seek(0)
        supabase.storage.from_("documents").upload(bucket_path, buffer.read())

        print(f"Relatório salvo com sucesso em: {bucket_path}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório: {str(e)}")

@app.get("/")
def home():
    return {"mensagem": "API de Previsão Online está ativa!"}

@app.post("/executar_previsao/")
def executar_previsao():
    try:
        # Carrega todos os dados relevantes
        df = carregar_dados()

        # Prepara as features para o modelo (todas as colunas relevantes)
        features = df.drop(columns=["IDCliente", "DataFatura"]).values

        # Executa a previsão
        previsoes = modelo.predict(features)

        # Gera e envia o relatório para o Supabase
        gerar_relatorio_txt(df, previsoes)

        return {"mensagem": "Previsão executada e relatório gerado com sucesso!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a previsão: {str(e)}")
