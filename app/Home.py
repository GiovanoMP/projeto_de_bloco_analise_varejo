import streamlit as st
from sqlalchemy import create_engine
import pandas as pd

def init_connection():
    try:
        connection_string = f"postgresql://{st.secrets['db_credentials']['user']}:{st.secrets['db_credentials']['password']}@{st.secrets['db_credentials']['host']}:{st.secrets['db_credentials']['port']}/{st.secrets['db_credentials']['database']}"
        return create_engine(connection_string)
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def test_connection():
    engine = init_connection()
    if engine:
        try:
            # Tenta fazer uma consulta simples
            query = "SELECT NOW();"
            with engine.connect() as conn:
                result = pd.read_sql(query, conn)
            st.success("Conexão estabelecida com sucesso!")
            st.write("Timestamp do servidor:", result.iloc[0,0])
        except Exception as e:
            st.error(f"Erro ao executar query: {e}")
    else:
        st.error("Não foi possível estabelecer conexão com o banco de dados")

st.title("Teste de Conexão com Banco de Dados")
test_connection()
