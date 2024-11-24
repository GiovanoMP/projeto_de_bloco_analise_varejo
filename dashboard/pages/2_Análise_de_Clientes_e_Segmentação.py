import streamlit as st
import pandas as pd
import plotly.express as px
from utils.api import APIClient
from utils.locale_config import setup_locale  # Substituímos o import locale por este

# Configurar locale para formatação de números
setup_locale()  # Substituímos o locale.setlocale por esta linha


# Configuração da página
st.set_page_config(
    page_title="Análise de Clientes",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título da página
st.title("🌎 Análise Global de Clientes")
st.markdown("---")

# Função para formatar valores monetários
def formatar_moeda(valor):
    return f"R$ {valor:,.2f}"

# Função para formatar números grandes
def formatar_numero(valor):
    return locale.format_string("%d", valor, grouping=True)

# Função com cache para carregar dados
@st.cache_data(ttl=3600)
def carregar_dados_clientes():
    try:
        client = APIClient()
        response = client.get_vendas_por_pais()
        if isinstance(response, pd.DataFrame):
            return response
        elif isinstance(response, (list, dict)):
            return pd.DataFrame(response)
        return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Carregamento dos dados
df = carregar_dados_clientes()

if df is not None:
    # Criando colunas para métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_vendas = df['total_vendas'].sum()
        st.metric(
            "Total de Vendas",
            formatar_moeda(total_vendas)
        )
    
    with col2:
        total_clientes = df['numero_clientes'].sum()
        st.metric(
            "Total de Clientes",
            formatar_numero(total_clientes)
        )
    
    with col3:
        ticket_medio_global = total_vendas / total_clientes
        st.metric(
            "Ticket Médio Global",
            formatar_moeda(ticket_medio_global)
        )

    # Criando abas para diferentes visualizações
    tab1, tab2 = st.tabs(["📊 Gráficos", "📋 Dados Detalhados"])

    with tab1:
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            # Gráfico de Vendas por País
            fig_vendas = px.bar(
                df,
                x='pais',
                y='total_vendas',
                title='Vendas Totais por País',
                labels={'pais': 'País', 'total_vendas': 'Total de Vendas (R$)'},
                color='total_vendas',
                color_continuous_scale='Viridis'
            )
            fig_vendas.update_traces(texttemplate='R$%{y:,.2f}', textposition='outside')
            st.plotly_chart(fig_vendas, use_container_width=True)

        with col_graf2:
            # Gráfico de Número de Clientes por País
            fig_clientes = px.bar(
                df,
                x='pais',
                y='numero_clientes',
                title='Número de Clientes por País',
                labels={'pais': 'País', 'numero_clientes': 'Número de Clientes'},
                color='numero_clientes',
                color_continuous_scale='Viridis'
            )
            fig_clientes.update_traces(texttemplate='%{y:,}', textposition='outside')
            st.plotly_chart(fig_clientes, use_container_width=True)

        # Gráfico de Ticket Médio por País
        fig_ticket = px.bar(
            df,
            x='pais',
            y='ticket_medio',
            title='Ticket Médio por País',
            labels={'pais': 'País', 'ticket_medio': 'Ticket Médio (R$)'},
            color='ticket_medio',
            color_continuous_scale='Viridis'
        )
        fig_ticket.update_traces(texttemplate='R$%{y:,.2f}', textposition='outside')
        st.plotly_chart(fig_ticket, use_container_width=True)

    with tab2:
        # Preparando DataFrame formatado para exibição
        df_display = df.copy()
        df_display['total_vendas'] = df_display['total_vendas'].apply(formatar_moeda)
        df_display['ticket_medio'] = df_display['ticket_medio'].apply(formatar_moeda)
        df_display['numero_clientes'] = df_display['numero_clientes'].apply(formatar_numero)
        
        # Renomeando colunas para exibição
        df_display.columns = ['País', 'Total de Vendas', 'Número de Clientes', 'Ticket Médio']
        
        # Exibindo tabela com dados formatados
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

else:
    st.error("Não foi possível carregar os dados. Por favor, verifique a conexão com a API.")
