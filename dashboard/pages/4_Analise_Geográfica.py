import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api import APIClient
from locale_config import setup_locale, format_number, format_brl
from datetime import datetime

# Primeiro comando Streamlit DEVE ser st.set_page_config
st.set_page_config(
    page_title="Análise Geográfica | Dashboard de Vendas",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar locale para formatação de números
setup_locale()

# Função para formatar valores monetários
def formatar_moeda(valor):
    return format_brl(valor)

# Função para formatar números grandes
def formatar_numero(valor):
    return format_number(valor)

# Inicialização do session state
if 'data_inicio' not in st.session_state:
    st.session_state.data_inicio = datetime(2011, 1, 4)
if 'data_fim' not in st.session_state:
    st.session_state.data_fim = datetime(2011, 12, 31)
if 'filtro_pais' not in st.session_state:
    st.session_state.filtro_pais = None

# Cache para dados da API
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_vendas_por_pais():
    try:
        client = APIClient()
        dados_pais = client.get_vendas_por_pais()
        if not isinstance(dados_pais, pd.DataFrame):
            dados_pais = pd.DataFrame(dados_pais['data'])
        return dados_pais
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Cache para cálculos de KPIs
@st.cache_data
def calcular_kpis(dados_pais):
    return {
        'total_vendas': dados_pais['total_vendas'].sum(),
        'total_clientes': dados_pais['numero_clientes'].sum(),
        'ticket_medio_global': dados_pais['total_vendas'].sum() / dados_pais['numero_clientes'].sum()
    }

# Título da página
st.title("🌎 Análise Geográfica de Vendas")
st.markdown("---")

# Carregando dados
dados_pais = carregar_vendas_por_pais()

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
    kpis = calcular_kpis(dados_pais)

    # KPIs principais em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total de Vendas",
            formatar_moeda(kpis['total_vendas'])
        )
    
    with col2:
        st.metric(
            "Total de Clientes",
            formatar_numero(kpis['total_clientes'])
        )
    
    with col3:
        st.metric(
            "Ticket Médio Global",
            formatar_moeda(kpis['ticket_medio_global'])
        )

    # Criando abas para diferentes visualizações
    tab1, tab2 = st.tabs(["🗺️ Mapa e Gráficos", "📋 Dados Detalhados"])

    with tab1:
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
            labels={
                'total_vendas': 'Total de Vendas (R$)',
                'numero_clientes': 'Número de Clientes',
                'ticket_medio': 'Ticket Médio (R$)'
            }
        )
        st.plotly_chart(fig_map, use_container_width=True)

        # Análise detalhada em duas colunas
        col1, col2 = st.columns(2)

        with col1:
            # Top 10 países por volume de vendas
            fig_top_vendas = px.bar(
                dados_pais.nlargest(10, 'total_vendas'),
                x='pais',
                y='total_vendas',
                title='Top 10 Países - Volume de Vendas',
                labels={'total_vendas': 'Total de Vendas (R$)', 'pais': 'País'},
                color='total_vendas',
                color_continuous_scale='Viridis'
            )
            fig_top_vendas.update_traces(texttemplate='R$%{y:,.2f}', textposition='outside')
            st.plotly_chart(fig_top_vendas, use_container_width=True)

        with col2:
            # Top 10 países por número de clientes
            fig_top_clientes = px.bar(
                dados_pais.nlargest(10, 'numero_clientes'),
                x='pais',
                y='numero_clientes',
                title='Top 10 Países - Base de Clientes',
                labels={'numero_clientes': 'Número de Clientes', 'pais': 'País'},
                color='numero_clientes',
                color_continuous_scale='Viridis'
            )
            fig_top_clientes.update_traces(texttemplate='%{y:,}', textposition='outside')
            st.plotly_chart(fig_top_clientes, use_container_width=True)

    with tab2:
        # Tabela detalhada
        st.subheader("Detalhamento por País")
        
        # Preparando DataFrame formatado para exibição
        df_display = dados_pais.copy()
        df_display['total_vendas'] = df_display['total_vendas'].apply(formatar_moeda)
        df_display['ticket_medio'] = df_display['ticket_medio'].apply(formatar_moeda)
        df_display['numero_clientes'] = df_display['numero_clientes'].apply(formatar_numero)
        
        # Renomeando colunas para exibição
        df_display.columns = ['País', 'Total de Vendas', 'Número de Clientes', 'Ticket Médio']
        
        # Exibindo tabela com dados formatados
        st.dataframe(
            df_display.sort_values('Total de Vendas', ascending=False),
            hide_index=True,
            use_container_width=True
        )

    # Adicionar botão para recarregar os dados
    if st.button("🔄 Recarregar Dados"):
        st.cache_data.clear()
        st.experimental_rerun()

else:
    st.error("Não foi possível carregar os dados. Por favor, verifique a conexão com a API.")
