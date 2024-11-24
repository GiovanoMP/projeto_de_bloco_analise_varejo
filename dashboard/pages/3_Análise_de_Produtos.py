# pages/3_analise_produtos.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api import APIClient
from utils.helpers import format_currency, format_large_number
from components.filters import category_filter

st.set_page_config(
    page_title="Análise de Produtos | Dashboard de Vendas",
    page_icon="📦",
    layout="wide"
)

if 'dados_produtos' not in st.session_state:
    st.session_state.dados_produtos = None

@st.cache_data(ttl=3600)
def carregar_dados_produtos():
    client = APIClient()
    return client.get_analise_produtos()

st.title("📦 Análise de Produtos")

try:
    if st.session_state.dados_produtos is None:
        st.session_state.dados_produtos = carregar_dados_produtos()
    
    dados = st.session_state.dados_produtos

    # KPIs Principais
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de Top Produtos
        st.subheader("Top 10 Produtos Mais Vendidos")
        fig_top = px.bar(
            dados['top_produtos'],
            x='codigo',
            y='valor_total',
            title="Top 10 Produtos por Valor Total",
            hover_data=['descricao', 'quantidade_vendida', 'ticket_medio']
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        # Gráfico de Categorias
        st.subheader("Vendas por Categoria")
        fig_cat = px.pie(
            dados['categorias'],
            values='valor_total',
            names='categoria',
            title="Distribuição de Vendas por Categoria"
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Distribuição de Preço
    st.subheader("Distribuição por Faixa de Preço")
    fig_preco = px.pie(
        pd.DataFrame(list(dados['distribuicao_preco'].items()), 
                    columns=['faixa_preco', 'valor']),
        values='valor',
        names='faixa_preco',
        title="Distribuição por Faixa de Preço"
    )
    st.plotly_chart(fig_preco, use_container_width=True)

    # Tabelas Detalhadas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Detalhamento dos Top Produtos")
        df_top = pd.DataFrame(dados['top_produtos'])
        st.dataframe(
            df_top,
            column_config={
                'codigo': 'Código',
                'descricao': 'Descrição',
                'quantidade_vendida': 'Qtd. Vendida',
                'valor_total': 'Valor Total',
                'ticket_medio': 'Ticket Médio'
            },
            hide_index=True
        )

    with col2:
        st.subheader("Detalhamento por Categoria")
        df_cat = pd.DataFrame(dados['categorias'])
        st.dataframe(
            df_cat,
            column_config={
                'categoria': 'Categoria',
                'valor_total': 'Valor Total',
                'quantidade_vendida': 'Qtd. Vendida',
                'ticket_medio': 'Ticket Médio'
            },
            hide_index=True
        )

except Exception as e:
    st.error("Erro ao carregar dados da API")
    st.exception(e)
