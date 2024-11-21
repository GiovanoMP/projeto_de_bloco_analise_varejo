import streamlit as st
import pandas as pd
import requests
from datetime import date

# Configuração da página
st.set_page_config(page_title="Download de Dados", layout="wide")

# Constantes
API_BASE_URL = "http://localhost:8000/api/v1"

# Dicionário com descrição dos campos
FIELD_DESCRIPTIONS = {
    "id": "Identificador único da transação",
    "created_at": "Data de criação do registro",
    "NumeroFatura": "Número identificador da fatura",
    "CodigoProduto": "Código único do produto",
    "Descricao": "Descrição do produto",
    "Quantidade": "Quantidade de itens vendidos",
    "DataFatura": "Data em que a fatura foi emitida",
    "PrecoUnitario": "Preço unitário do produto",
    "IDCliente": "Identificador único do cliente",
    "Pais": "País onde a venda foi realizada",
    "CategoriaProduto": "Categoria do produto",
    "CategoriaPreco": "Categoria de preço",
    "ValorTotalFatura": "Valor total da fatura",
    "FaturaUnica": "Indica se é uma fatura única",
    "Ano": "Ano da venda",
    "Mes": "Mês da venda",
    "Dia": "Dia da venda",
    "DiaSemana": "Dia da semana (0-6)"
}

# Função para buscar dados
@st.cache_data(ttl=3600)
def fetch_transactions(start_date, end_date):
    try:
        params = {
            "data_inicio": start_date,
            "data_fim": end_date,
            "skip": 0,
            "limit": 10000  # Ajuste conforme necessário
        }

        response = requests.get(
            f"{API_BASE_URL}/transactions/",
            params=params
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def main():
    st.title("📥 Download de Dados")
    
    # Descrição da página
    st.markdown("""
    Esta página permite o download dos dados de transações do banco de dados.
    Selecione o período desejado e os campos que deseja incluir no arquivo CSV.
    """)

    # Seletor de período
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Data Inicial",
            value=date(2011, 1, 4),
            min_value=date(2011, 1, 4),
            max_value=date(2011, 12, 31)
        )
    with col2:
        end_date = st.date_input(
            "Data Final",
            value=date(2011, 12, 31),
            min_value=date(2011, 1, 4),
            max_value=date(2011, 12, 31)
        )

    # Descrição dos campos disponíveis
    with st.expander("Ver descrição dos campos"):
        for field, description in FIELD_DESCRIPTIONS.items():
            st.markdown(f"**{field}**: {description}")

    # Seleção de campos
    st.subheader("Selecione os campos para download")
    
    # Checkbox para selecionar todos
    all_fields = list(FIELD_DESCRIPTIONS.keys())
    if st.checkbox("Selecionar todos os campos", value=True):
        selected_fields = all_fields
    else:
        # Criar múltiplas colunas para os checkboxes
        num_cols = 3
        cols = st.columns(num_cols)
        field_chunks = [all_fields[i::num_cols] for i in range(num_cols)]
        
        selected_fields = []
        for i, col in enumerate(cols):
            with col:
                for field in field_chunks[i]:
                    if st.checkbox(field, key=field):
                        selected_fields.append(field)

    # Botão de download
    if st.button("Gerar CSV"):
        if selected_fields:
            with st.spinner('Carregando dados...'):
                df = fetch_transactions(start_date, end_date)
                
                if df is not None:
                    # Selecionar apenas as colunas escolhidas
                    df = df[selected_fields]
                    
                    # Converter para CSV
                    csv = df.to_csv(index=False)
                    
                    # Botão de download
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"transacoes_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
                    
                    # Mostrar preview dos dados
                    st.subheader("Preview dos dados")
                    st.dataframe(df.head())
                    st.info(f"Total de registros: {len(df)}")
        else:
            st.warning("Selecione pelo menos um campo para download.")

if __name__ == "__main__":
    main()
