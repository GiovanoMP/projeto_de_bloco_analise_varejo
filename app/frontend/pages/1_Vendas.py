import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import requests
from datetime import timedelta

API_BASE_URL = st.secrets["API_BASE_URL"]

# Configuração da página
st.set_page_config(page_title="Análise de Vendas", layout="wide")

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
@st.cache_data(ttl=3600)  # Cache por 1 hora
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
def fetch_transactions_by_category(start_date, end_date):
    try:
        response = requests.get(
            f"{API_BASE_URL}/transactions/by-category",
            params={"data_inicio": start_date, "data_fim": end_date}
        )
        return response.json()
    except Exception as e:
        st.error(f"Erro ao carregar dados por categoria: {e}")
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
    st.session_state['category_data'] = fetch_transactions_by_category(start_date, end_date)
    st.session_state['country_data'] = fetch_transactions_by_country(start_date, end_date)
    st.session_state['last_update'] = datetime.now()

def render_overview_tab():
    """Renderiza a aba de visão geral"""
    summary_data = st.session_state['summary_data']
    category_data = st.session_state['category_data']
    
    if summary_data:
        # Métricas principais com estilo melhorado
        st.markdown("""
        <style>
        .metric-row {
            display: flex;
            justify-content: space-between;
            padding: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total de Vendas", 
                f"R$ {float(summary_data['total_value']):,.2f}",
                delta=None
            )
        with col2:
            st.metric(
                "Total de Transações", 
                f"{summary_data['total_transactions']:,}",
                delta=None
            )
        with col3:
            st.metric(
                "Clientes Únicos", 
                f"{summary_data['unique_customers']:,}",
                delta=None
            )
        with col4:
            st.metric(
                "Ticket Médio", 
                f"R$ {float(summary_data['average_unit_price']):,.2f}",
                delta=None
            )

    if category_data:
        # Gráficos de categoria
        col1, col2 = st.columns(2)
        with col1:
            fig_category = px.bar(
                category_data,
                x="categoria",
                y="valor_total",
                title="Vendas por Categoria",
                labels={"categoria": "Categoria", "valor_total": "Valor Total (R$)"}
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            fig_ticket = px.scatter(
                category_data,
                x="categoria",
                y="ticket_medio",
                size="total_vendas",
                title="Ticket Médio por Categoria",
                labels={"categoria": "Categoria", "ticket_medio": "Ticket Médio (R$)"}
            )
            st.plotly_chart(fig_ticket, use_container_width=True)

def render_geographic_tab():
    """Renderiza a aba de análise geográfica"""
    country_data = st.session_state['country_data']
    
    if country_data:
        df_country = pd.DataFrame(country_data)
        df_country['valor_total'] = df_country['valor_total'].astype(float)
        
        # Mapa de árvore
        fig_treemap = px.treemap(
            df_country,
            path=['pais'],
            values='valor_total',
            title="Distribuição de Vendas por País"
        )
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Análise detalhada dos países
        col1, col2 = st.columns(2)
        
        with col1:
            # Top 10 países por valor
            st.subheader("Top 10 Países por Valor de Vendas")
            df_top_value = df_country.nlargest(10, 'valor_total')
            fig_top_value = px.bar(
                df_top_value,
                x='pais',
                y='valor_total',
                title="Top 10 Países por Valor Total"
            )
            st.plotly_chart(fig_top_value, use_container_width=True)
        
        with col2:
            # Top 10 países por ticket médio
            st.subheader("Top 10 Países por Ticket Médio")
            df_top_ticket = df_country.nlargest(10, 'ticket_medio')
            fig_top_ticket = px.bar(
                df_top_ticket,
                x='pais',
                y='ticket_medio',
                title="Top 10 Países por Ticket Médio"
            )
            st.plotly_chart(fig_top_ticket, use_container_width=True)

def main():
    st.title("📊 Análise de Vendas")

    # Seletor de período com valores padrão
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
    tab1, tab2 = st.tabs(["Visão Geral", "Análise Geográfica"])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_geographic_tab()

if __name__ == "__main__":
    main()
