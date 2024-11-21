import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import requests
API_BASE_URL = st.secrets["API_BASE_URL"]


# Configuração da página
st.set_page_config(page_title="Análise de Produtos", layout="wide")



# Funções para buscar dados da API
@st.cache_data(ttl=3600)
def fetch_transactions(start_date, end_date, categoria=None):
    try:
        params = {
            "data_inicio": start_date,
            "data_fim": end_date,
            "categoria": categoria
        }
        response = requests.get(f"{API_BASE_URL}/transactions/", params=params)
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar transações: {e}")
        return []

@st.cache_data(ttl=3600)
def fetch_transactions_by_category(start_date, end_date):
    try:
        response = requests.get(
            f"{API_BASE_URL}/transactions/by-category",
            params={"data_inicio": start_date, "data_fim": end_date}
        )
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados por categoria: {e}")
        return []

def process_product_data(transactions):
    if not transactions:
        return pd.DataFrame()
    
    df = pd.DataFrame(transactions)
    df['PrecoUnitario'] = df['PrecoUnitario'].astype(float)
    df['ValorTotalFatura'] = df['ValorTotalFatura'].astype(float)
    return df

def render_product_overview(df_products):
    st.subheader("Visão Geral dos Produtos")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_products = df_products['CodigoProduto'].nunique()
        st.metric("Total de Produtos Únicos", f"{total_products:,}")
    
    with col2:
        total_quantity = df_products['Quantidade'].sum()
        st.metric("Quantidade Total Vendida", f"{total_quantity:,}")
    
    with col3:
        total_revenue = df_products['ValorTotalFatura'].sum()
        st.metric("Receita Total", f"R$ {total_revenue:,.2f}")
    
    with col4:
        avg_price = df_products['PrecoUnitario'].mean()
        st.metric("Preço Médio", f"R$ {avg_price:.2f}")

    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 produtos mais vendidos
        top_products = df_products.groupby('Descricao')['Quantidade'].sum().nlargest(10)
        fig = px.bar(
            top_products,
            title="Top 10 Produtos Mais Vendidos",
            labels={'Descricao': 'Produto', 'Quantidade': 'Quantidade Vendida'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top 10 produtos por receita
        top_revenue = df_products.groupby('Descricao')['ValorTotalFatura'].sum().nlargest(10)
        fig = px.bar(
            top_revenue,
            title="Top 10 Produtos por Receita",
            labels={'Descricao': 'Produto', 'ValorTotalFatura': 'Receita Total (R$)'}
        )
        st.plotly_chart(fig, use_container_width=True)

def render_category_analysis(df_categories):
    st.subheader("Análise por Categoria")
    
    if not df_categories.empty:
        # Gráficos de categoria
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                df_categories,
                values='total_vendas',
                names='categoria',
                title="Distribuição de Vendas por Categoria"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                df_categories,
                x='categoria',
                y='ticket_medio',
                title="Ticket Médio por Categoria",
                labels={'ticket_medio': 'Ticket Médio (R$)', 'categoria': 'Categoria'}
            )
            st.plotly_chart(fig, use_container_width=True)

        # Tabela detalhada
        st.subheader("Detalhamento por Categoria")
        df_display = df_categories.copy()
        df_display['valor_total'] = df_display['valor_total'].apply(lambda x: f"R$ {float(x):,.2f}")
        df_display['ticket_medio'] = df_display['ticket_medio'].apply(lambda x: f"R$ {x:,.2f}")
        st.dataframe(df_display, use_container_width=True)

def main():
    st.title("📦 Análise de Produtos")

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

    # Carregar dados
    transactions = fetch_transactions(start_date, end_date)
    categories_data = fetch_transactions_by_category(start_date, end_date)
    
    df_products = process_product_data(transactions)
    df_categories = pd.DataFrame(categories_data)

    # Abas
    tab1, tab2 = st.tabs(["Visão Geral dos Produtos", "Análise por Categoria"])
    
    with tab1:
        if not df_products.empty:
            render_product_overview(df_products)
        else:
            st.warning("Nenhum dado de produto disponível para o período selecionado.")
    
    with tab2:
        if not df_categories.empty:
            render_category_analysis(df_categories)
        else:
            st.warning("Nenhum dado de categoria disponível para o período selecionado.")

if __name__ == "__main__":
    main()
