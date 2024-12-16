import streamlit as st

# Primeiro comando Streamlit DEVE ser st.set_page_config
st.set_page_config(
    page_title="Análise de Produtos | Dashboard de Vendas",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Depois vêm os outros imports
import plotly.express as px
import pandas as pd
from utils.api import APIClient
from locale_config import setup_locale, format_number, format_brl

# Configurar locale para formatação de números
setup_locale()

# Título da página
st.title("📦 Análise de Produtos")
st.markdown("---")

# Função para formatar valores monetários
def formatar_moeda(valor):
    return format_brl(valor)

# Função para formatar números grandes
def formatar_numero(valor):
    return format_number(valor)

# Função com cache para carregar dados
@st.cache_data(ttl=3600)
def carregar_dados_produtos():
    try:
        client = APIClient()
        response = client.get_analise_produtos()
        if response is None:
            return None
        return response
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Carregar dados com indicador de progresso
with st.spinner('Carregando dados dos produtos...'):
    dados = carregar_dados_produtos()

if dados is not None:
    try:
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
                hover_data=['descricao', 'quantidade_vendida', 'ticket_medio'],
                labels={
                    'codigo': 'Código',
                    'valor_total': 'Valor Total (R$)',
                    'descricao': 'Descrição',
                    'quantidade_vendida': 'Qtd. Vendida',
                    'ticket_medio': 'Ticket Médio'
                }
            )
            fig_top.update_traces(texttemplate='R$%{y:,.2f}', textposition='outside')
            st.plotly_chart(fig_top, use_container_width=True)

        with col2:
            # Gráfico de Categorias
            st.subheader("Vendas por Categoria")
            fig_cat = px.pie(
                dados['categorias'],
                values='valor_total',
                names='categoria',
                title="Distribuição de Vendas por Categoria",
                labels={'categoria': 'Categoria', 'valor_total': 'Valor Total'}
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        # Distribuição de Preço
        st.subheader("Distribuição por Faixa de Preço")
        df_preco = pd.DataFrame(
            list(dados['distribuicao_preco'].items()), 
            columns=['faixa_preco', 'valor']
        )
        fig_preco = px.pie(
            df_preco,
            values='valor',
            names='faixa_preco',
            title="Distribuição por Faixa de Preço",
            labels={'faixa_preco': 'Faixa de Preço', 'valor': 'Valor'}
        )
        st.plotly_chart(fig_preco, use_container_width=True)

        # Tabelas Detalhadas
        tab1, tab2 = st.tabs(["📊 Top Produtos", "📋 Categorias"])
        
        with tab1:
            st.subheader("Detalhamento dos Top Produtos")
            df_top = pd.DataFrame(dados['top_produtos'])
            
            # Formatando valores
            df_top['valor_total'] = df_top['valor_total'].apply(formatar_moeda)
            df_top['ticket_medio'] = df_top['ticket_medio'].apply(formatar_moeda)
            df_top['quantidade_vendida'] = df_top['quantidade_vendida'].apply(formatar_numero)
            
            st.dataframe(
                df_top,
                column_config={
                    'codigo': 'Código',
                    'descricao': 'Descrição',
                    'quantidade_vendida': 'Qtd. Vendida',
                    'valor_total': 'Valor Total',
                    'ticket_medio': 'Ticket Médio'
                },
                hide_index=True,
                use_container_width=True
            )

        with tab2:
            st.subheader("Detalhamento por Categoria")
            df_cat = pd.DataFrame(dados['categorias'])
            
            # Formatando valores
            df_cat['valor_total'] = df_cat['valor_total'].apply(formatar_moeda)
            df_cat['ticket_medio'] = df_cat['ticket_medio'].apply(formatar_moeda)
            df_cat['quantidade_vendida'] = df_cat['quantidade_vendida'].apply(formatar_numero)
            
            st.dataframe(
                df_cat,
                column_config={
                    'categoria': 'Categoria',
                    'valor_total': 'Valor Total',
                    'quantidade_vendida': 'Qtd. Vendida',
                    'ticket_medio': 'Ticket Médio'
                },
                hide_index=True,
                use_container_width=True
            )

    except Exception as e:
        st.error(f"Erro ao processar os dados: {str(e)}")

else:
    st.error("Não foi possível carregar os dados. Por favor, verifique a conexão com a API.")

# Adicionar botão para recarregar os dados
if st.button("🔄 Recarregar Dados"):
    st.cache_data.clear()
    st.experimental_rerun()
