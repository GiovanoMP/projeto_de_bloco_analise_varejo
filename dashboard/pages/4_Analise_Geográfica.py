# pages/1_analise_geografica.py
import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api import APIClient
from utils.helpers import format_currency, format_large_number
from components.filters import date_range_filter
from components.charts import create_map_chart
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Análise Geográfica | Dashboard de Vendas",
    page_icon="🌎",
    layout="wide"
)

# Inicialização do session state
if 'data_inicio' not in st.session_state:
    st.session_state.data_inicio = datetime(2011, 1, 4)
if 'data_fim' not in st.session_state:
    st.session_state.data_fim = datetime(2011, 12, 31)
if 'filtro_pais' not in st.session_state:
    st.session_state.filtro_pais = None

# Cache para dados da API
@st.cache_data(ttl=3600)  # Cache por 1 hora
def load_vendas_por_pais():
    client = APIClient()
    try:
        dados_pais = client.get_vendas_por_pais()
        if not isinstance(dados_pais, pd.DataFrame):
            dados_pais = pd.DataFrame(dados_pais['data'])
        return dados_pais
    except Exception as e:
        st.error("Erro ao carregar dados da API")
        st.exception(e)
        return None

# Cache para cálculos de KPIs
@st.cache_data
def calculate_kpis(dados_pais):
    return {
        'total_vendas': dados_pais['total_vendas'].sum(),
        'total_clientes': dados_pais['numero_clientes'].sum(),
        'ticket_medio_global': dados_pais['total_vendas'].sum() / dados_pais['numero_clientes'].sum()
    }

# Título da página
st.title("🌎 Análise Geográfica de Vendas")

# Carregando dados
dados_pais = load_vendas_por_pais()

if dados_pais is not None:
    # Filtros
    with st.expander("Filtros", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Data Início",
                value=st.session_state.data_inicio,
                min_value=datetime(2011, 1, 4),
                max_value=datetime(2011, 12, 31)
            )
        with col2:
            end_date = st.date_input(
                "Data Fim",
                value=st.session_state.data_fim,
                min_value=datetime(2011, 1, 4),
                max_value=datetime(2011, 12, 31)
            )
        
        # Atualizar session state
        st.session_state.data_inicio = start_date
        st.session_state.data_fim = end_date

    # Cálculo de KPIs
    kpis = calculate_kpis(dados_pais)

    # KPIs principais em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total de Vendas",
            format_currency(kpis['total_vendas']),
            "Volume Total"
        )
    
    with col2:
        st.metric(
            "Total de Clientes",
            format_large_number(kpis['total_clientes']),
            "Base de Clientes"
        )
    
    with col3:
        st.metric(
            "Ticket Médio Global",
            format_currency(kpis['ticket_medio_global']),
            "Por Cliente"
        )

    # Mapa de calor das vendas
    st.subheader("Distribuição Global de Vendas")
    fig_map = px.choropleth(
        dados_pais,
        locations='pais',
        locationmode='country names',
        color='total_vendas',
        hover_name='pais',
        hover_data={
            'total_vendas': ':,.2f',
            'numero_clientes': ':,',
            'ticket_medio': ':,.2f'
        },
        color_continuous_scale='Viridis',
        title='Vendas por País'
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Análise detalhada em duas colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Países por Volume de Vendas")
        fig_top_vendas = px.bar(
            dados_pais.nlargest(10, 'total_vendas'),
            x='pais',
            y='total_vendas',
            title='Top 10 Países - Volume de Vendas',
            labels={'total_vendas': 'Total de Vendas', 'pais': 'País'}
        )
        st.plotly_chart(fig_top_vendas, use_container_width=True)

    with col2:
        st.subheader("Top 10 Países por Número de Clientes")
        fig_top_clientes = px.bar(
            dados_pais.nlargest(10, 'numero_clientes'),
            x='pais',
            y='numero_clientes',
            title='Top 10 Países - Base de Clientes',
            labels={'numero_clientes': 'Número de Clientes', 'pais': 'País'}
        )
        st.plotly_chart(fig_top_clientes, use_container_width=True)

    # Tabela detalhada com cache
    @st.cache_data
    def format_dataframe(df):
        df = df.copy()
        df['total_vendas'] = df['total_vendas'].map(lambda x: f"£ {x:,.2f}")
        df['ticket_medio'] = df['ticket_medio'].map(lambda x: f"£ {x:,.2f}")
        return df

    st.subheader("Detalhamento por País")
    dados_formatados = format_dataframe(dados_pais)
    st.dataframe(
        dados_formatados.sort_values('total_vendas', ascending=False),
        column_config={
            'pais': 'País',
            'total_vendas': 'Total de Vendas',
            'numero_clientes': 'Número de Clientes',
            'ticket_medio': 'Ticket Médio'
        },
        hide_index=True
    )

