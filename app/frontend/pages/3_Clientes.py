import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import requests

API_BASE_URL = st.secrets["API_BASE_URL"]


# Configuração da página
st.set_page_config(page_title="Análise de Clientes", layout="wide")

# Inicialização do estado da sessão
if 'last_update' not in st.session_state:
    st.session_state['last_update'] = None
if 'summary_data' not in st.session_state:
    st.session_state['summary_data'] = None
if 'category_data' not in st.session_state:
    st.session_state['category_data'] = None
if 'country_data' not in st.session_state:
    st.session_state['country_data'] = None



# Funções para buscar dados da API com cache
@st.cache_data(ttl=3600)
def fetch_transactions_summary(start_date, end_date):
    try:
        response = requests.get(
            f"{API_BASE_URL}/transactions/summary",
            params={"data_inicio": start_date, "data_fim": end_date}
        )
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar sumário de transações: {e}")
        return None

@st.cache_data(ttl=3600)
def fetch_transactions_by_country(start_date, end_date):
    try:
        response = requests.get(
            f"{API_BASE_URL}/transactions/by-country",
            params={"data_inicio": start_date, "data_fim": end_date}
        )
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados por país: {e}")
        return None

def load_data(start_date, end_date):
    """Função para carregar todos os dados necessários"""
    st.session_state['summary_data'] = fetch_transactions_summary(start_date, end_date)
    st.session_state['country_data'] = fetch_transactions_by_country(start_date, end_date)
    st.session_state['last_update'] = datetime.now()

def render_customer_overview():
    """Renderiza a aba de visão geral dos clientes"""
    summary_data = st.session_state['summary_data']
    
    if summary_data:
        # Métricas principais sobre clientes
        st.subheader("Métricas Principais de Clientes")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total de Clientes Únicos",
                f"{summary_data['unique_customers']:,}"
            )
        with col2:
            st.metric(
                "Média de Compras por Cliente",
                f"{summary_data['total_transactions'] / summary_data['unique_customers']:.2f}"
            )
        with col3:
            st.metric(
                "Valor Médio por Cliente",
                f"R$ {float(summary_data['total_value']) / summary_data['unique_customers']:,.2f}"
            )

def render_customer_geographic():
    """Renderiza a aba de distribuição geográfica dos clientes"""
    country_data = st.session_state['country_data']
    
    if country_data:
        df_country = pd.DataFrame(country_data)
        
        # Distribuição de clientes por país
        st.subheader("Distribuição de Clientes por País")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 países por número de clientes
            df_top_customers = df_country.nlargest(10, 'quantidade_clientes')
            fig_customers = px.bar(
                df_top_customers,
                x='pais',
                y='quantidade_clientes',
                title="Top 10 Países por Número de Clientes",
                labels={'pais': 'País', 'quantidade_clientes': 'Número de Clientes'}
            )
            fig_customers.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
            st.plotly_chart(fig_customers, use_container_width=True)
        
        with col2:
            # Gráfico de pizza com distribuição percentual (top 10 países)
            df_pie = df_country.nlargest(10, 'quantidade_clientes').copy()
            outros = pd.DataFrame({
                'pais': ['Outros'],
                'quantidade_clientes': [df_country.nsmallest(len(df_country) - 10, 'quantidade_clientes')['quantidade_clientes'].sum()]
            })
            df_pie = pd.concat([df_pie, outros])
            
            fig_pie = px.pie(
                df_pie,
                values='quantidade_clientes',
                names='pais',
                title="Distribuição Percentual de Clientes (Top 10 Países)",
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        # Tabela detalhada de clientes por país
        st.subheader("Detalhamento de Clientes por País")
        df_display = df_country[['pais', 'quantidade_clientes', 'ticket_medio']].copy()
        df_display['ticket_medio'] = df_display['ticket_medio'].apply(lambda x: f"R$ {x:,.2f}")
        df_display.columns = ['País', 'Quantidade de Clientes', 'Ticket Médio']
        df_display = df_display.sort_values('Quantidade de Clientes', ascending=False)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

def main():
    st.title("👥 Análise de Clientes")

    # Seletor de período
    col1, col2, col3 = st.columns([2, 2, 1])
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
    with col3:
        if st.button("Atualizar Dados"):
            load_data(start_date, end_date)

    # Carregar dados iniciais se necessário
    if st.session_state['last_update'] is None:
        load_data(start_date, end_date)

    # Exibir última atualização
    if st.session_state['last_update']:
        st.sidebar.info(f"Última atualização: {st.session_state['last_update'].strftime('%d/%m/%Y %H:%M:%S')}")

    # Abas
    tab1, tab2 = st.tabs(["Visão Geral dos Clientes", "Distribuição Geográfica"])
    
    with tab1:
        render_customer_overview()
    
    with tab2:
        render_customer_geographic()

if __name__ == "__main__":
    main()
