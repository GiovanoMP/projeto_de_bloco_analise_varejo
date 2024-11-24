# pages/4_Downloads.py
import streamlit as st
import pandas as pd
from datetime import date
from utils.api import APIClient
import locale

# Configurar locale para formatação de números
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Configuração da página
st.set_page_config(
    page_title="Download de Dados",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dicionário com descrição dos campos
FIELD_DESCRIPTIONS = {
    "periodo": "Período da análise (mês)",
    "total_vendas": "Total de vendas no período em R$",
    "quantidade_vendas": "Quantidade de vendas realizadas",
    "ticket_medio": "Valor médio por venda em R$"
}

@st.cache_data(ttl=3600)
def carregar_dados_temporais(data_inicio, data_fim):
    """
    Carrega dados da análise temporal usando a API existente
    """
    try:
        client = APIClient()
        response = client.get_analise_temporal(
            data_inicio=data_inicio.strftime("%Y-%m-%d"),
            data_fim=data_fim.strftime("%Y-%m-%d")
        )
        
        if response.get('status') == 'success':
            dados = response.get('vendas_por_mes', [])
            return pd.DataFrame(dados)
        else:
            st.error("Erro na resposta da API")
            return None
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

def formatar_dados(df, selected_fields):
    """
    Formata os dados numéricos para o formato brasileiro
    """
    df_formatted = df[selected_fields].copy()
    
    if 'total_vendas' in selected_fields:
        df_formatted['total_vendas'] = df_formatted['total_vendas'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        )
    
    if 'ticket_medio' in selected_fields:
        df_formatted['ticket_medio'] = df_formatted['ticket_medio'].apply(
            lambda x: f"R$ {x:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        )
    
    return df_formatted

def main():
    # Título da página
    st.title("📥 Download de Dados")
    st.markdown("---")
    
    # Descrição da página
    st.markdown("""
    ### Exportação de Dados de Análise Temporal
    
    Utilize esta página para baixar os dados de vendas em formato CSV.
    Você pode:
    - Selecionar o período desejado
    - Escolher os campos para exportação
    - Visualizar uma prévia dos dados antes do download
    """)

    # Container para os filtros
    with st.container():
        st.subheader("🔍 Filtros de Período")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input(
                "Data Inicial",
                value=date(2011, 1, 1),
                min_value=date(2011, 1, 1),
                max_value=date(2011, 12, 31),
                format="DD/MM/YYYY"
            )
        with col2:
            data_fim = st.date_input(
                "Data Final",
                value=date(2011, 12, 31),
                min_value=date(2011, 1, 1),
                max_value=date(2011, 12, 31),
                format="DD/MM/YYYY"
            )

    # Descrição dos campos disponíveis
    with st.expander("ℹ️ Descrição dos Campos"):
        for field, description in FIELD_DESCRIPTIONS.items():
            st.markdown(f"**{field}**: {description}")

    # Seleção de campos
    st.subheader("📋 Campos para Exportação")
    
    # Checkbox para selecionar todos
    all_fields = list(FIELD_DESCRIPTIONS.keys())
    selecionar_todos = st.checkbox("Selecionar todos os campos", value=True)
    
    if selecionar_todos:
        selected_fields = all_fields
    else:
        # Criar múltiplas colunas para os checkboxes
        num_cols = 2
        cols = st.columns(num_cols)
        field_chunks = [all_fields[i::num_cols] for i in range(num_cols)]
        
        selected_fields = []
        for i, col in enumerate(cols):
            with col:
                for field in field_chunks[i]:
                    if st.checkbox(field, key=field):
                        selected_fields.append(field)

    # Botão de geração do CSV
    if st.button("🔄 Carregar Dados", type="primary"):
        if not selected_fields:
            st.warning("Por favor, selecione pelo menos um campo para exportação.")
            return

        with st.spinner('Carregando dados...'):
            df = carregar_dados_temporais(data_inicio, data_fim)
            
            if df is not None and not df.empty:
                # Mostrar prévia dos dados
                st.subheader("📊 Prévia dos Dados")
                df_preview = formatar_dados(df, selected_fields)
                st.dataframe(df_preview, use_container_width=True)
                
                # Preparar dados para download
                df_download = df[selected_fields].copy()
                
                # Botão de download
                csv = df_download.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"dados_vendas_{data_inicio.strftime('%Y%m%d')}_{data_fim.strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )
            else:
                st.error("Não foram encontrados dados para o período selecionado.")

if __name__ == "__main__":
    main()
