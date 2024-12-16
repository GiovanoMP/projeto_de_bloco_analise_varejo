# pages/2_Análise_Temporal.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.api import APIClient

# Título da página
st.title("📈 Análise Temporal de Vendas")
st.markdown("---")

# Função com cache para carregar dados
@st.cache_data(ttl=3600)  # Cache por 1 hora
def carregar_dados_temporais(data_inicio, data_fim):
    try:
        client = APIClient()
        return client.get_analise_temporal(
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Adicionar filtro de datas
col_data1, col_data2 = st.columns(2)
with col_data1:
    data_inicial = st.date_input(
        "Data Inicial",
        value=datetime(2011, 1, 4),
        min_value=datetime(2011, 1, 4),
        max_value=datetime(2011, 12, 31)
    )

with col_data2:
    data_final = st.date_input(
        "Data Final",
        value=datetime(2011, 12, 31),
        min_value=datetime(2011, 1, 4),
        max_value=datetime(2011, 12, 31)
    )

# Validação das datas
if data_inicial > data_final:
    st.error("A data inicial não pode ser maior que a data final!")
else:
    # Carregamento dos dados com os parâmetros de data
    dados = carregar_dados_temporais(data_inicial, data_final)

    if dados and dados.get('status') == 'success':
        # Convertendo dados para DataFrames
        df_mensal = pd.DataFrame(dados.get('vendas_por_mes', []))
        df_semanal = pd.DataFrame(dados.get('vendas_por_semana', []))
        df_dia_semana = pd.DataFrame(dados.get('vendas_por_dia_semana', []))

        # Seção de Vendas Mensais
        st.subheader("📊 Vendas Mensais")
        col1, col2 = st.columns(2)
        with col1:
            if not df_mensal.empty:
                st.line_chart(df_mensal.set_index('periodo')['total_vendas'])
        with col2:
            if not df_mensal.empty:
                st.metric(
                    "Ticket Médio Mensal",
                    f"R$ {df_mensal['ticket_medio'].mean():.2f}",
                    f"{df_mensal['quantidade_vendas'].sum()} vendas"
                )

        # Seção de Vendas Semanais
        st.subheader("📅 Vendas Semanais")
        col3, col4 = st.columns(2)
        with col3:
            if not df_semanal.empty:
                st.line_chart(df_semanal.set_index('periodo')['total_vendas'])
        with col4:
            if not df_semanal.empty:
                st.metric(
                    "Ticket Médio Semanal",
                    f"R$ {df_semanal['ticket_medio'].mean():.2f}",
                    f"{df_semanal['quantidade_vendas'].sum()} vendas"
                )

        # Seção de Vendas por Dia da Semana
        st.subheader("📆 Vendas por Dia da Semana")
        col5, col6 = st.columns(2)
        with col5:
            if not df_dia_semana.empty:
                st.bar_chart(df_dia_semana.set_index('periodo')['total_vendas'])
        with col6:
            if not df_dia_semana.empty:
                st.metric(
                    "Ticket Médio por Dia",
                    f"R$ {df_dia_semana['ticket_medio'].mean():.2f}",
                    f"{df_dia_semana['quantidade_vendas'].sum()} vendas"
                )

        # Tabelas detalhadas (expansíveis)
        with st.expander("Ver Dados Detalhados"):
            tab1, tab2, tab3 = st.tabs(["Mensal", "Semanal", "Diário"])
            
            with tab1:
                if not df_mensal.empty:
                    st.dataframe(df_mensal, use_container_width=True)
            
            with tab2:
                if not df_semanal.empty:
                    st.dataframe(df_semanal, use_container_width=True)
            
            with tab3:
                if not df_dia_semana.empty:
                    st.dataframe(df_dia_semana, use_container_width=True)

    else:
        st.error("Não foi possível carregar os dados de análise temporal.")
