#Home
import streamlit as st

def main():
    # Configuração da página
    st.set_page_config(
        page_title="RetailSense AI",
        page_icon="🏪",
        layout="wide"
    )

    # Título principal com estilo personalizado
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B;'>RetailSense AI</h1>
        <h3 style='text-align: center;'>Inteligência Artificial para um Varejo mais Sustentável</h3>
    """, unsafe_allow_html=True)

    # Breve descrição do projeto
    st.markdown("""
    ---
    ### 🎯 Sobre o Projeto
    
    O RetailSense AI é uma plataforma inovadora que combina análise avançada de dados 
    com práticas sustentáveis para o varejo. Nossa solução oferece insights valiosos 
    para tomada de decisões mais inteligentes e ambientalmente responsáveis.
    
    ### 🌟 Principais Funcionalidades
    
    - **📊 Análise de Transações**: Visualize e analise dados de vendas com filtros personalizáveis
    - **🌍 Análise Geográfica**: Explore o desempenho de vendas por país
    - **📈 Análise por Categoria**: Acompanhe o desempenho por categoria de produtos
    - **💡 Insights Inteligentes**: Obtenha resumos e métricas importantes do seu negócio
    
    ### 📱 Como Usar
    
    1. **Navegação**: Use o menu lateral para acessar diferentes análises
    2. **Filtros**: Utilize os filtros de data para personalizar suas análises
    3. **Visualizações**: Interaja com os gráficos para obter informações detalhadas
    4. **Exportação**: Baixe relatórios e visualizações quando disponíveis
    
    ### 🎨 Recursos Visuais
    
    - Gráficos interativos
    - Dashboards personalizáveis
    - Métricas em tempo real
    - Exportação de dados
    """)

    # Informações adicionais em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📚 Documentação
        Para mais informações sobre como utilizar cada recurso, 
        consulte nossa documentação detalhada.
        """)

    with col2:
        st.markdown("""
        ### 💡 Dicas
        - Use os filtros de data para análises específicas
        - Compare períodos diferentes
        - Explore diferentes visualizações
        """)

    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p>Desenvolvido com ❤️ pela Equipe RetailSense AI</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

################################################################################################
# Vendas.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import requests
from datetime import timedelta
import traceback

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

@st.cache_data(ttl=3600)
def fetch_transactions_summary(start_date, end_date):
    """Busca o sumário de transações da API"""
    try:
        url = f"{API_BASE_URL}/transactions/summary"
        params = {
            "data_inicio": start_date.strftime("%Y-%m-%d"),
            "data_fim": end_date.strftime("%Y-%m-%d")
        }
        
        st.write("Debug - URL:", url)
        st.write("Debug - Parâmetros:", params)
        
        response = requests.get(url, params=params)
        
        if not response.ok:
            st.error(f"Erro na API (Status {response.status_code}): {response.text}")
            return None
        
        data = response.json()
        st.write("Debug - Resposta da API:", data)
        return data
    
    except Exception as e:
        st.error(f"Erro ao buscar sumário: {str(e)}")
        st.write("Traceback:", traceback.format_exc())
        return None

@st.cache_data(ttl=3600)
def fetch_transactions_by_category(start_date, end_date):
    """Busca transações por categoria da API"""
    try:
        url = f"{API_BASE_URL}/transactions/by-category"
        params = {
            "data_inicio": start_date.strftime("%Y-%m-%d"),
            "data_fim": end_date.strftime("%Y-%m-%d")
        }
        
        response = requests.get(url, params=params)
        
        if not response.ok:
            st.error(f"Erro na API (Status {response.status_code}): {response.text}")
            return None
            
        return response.json()
    
    except Exception as e:
        st.error(f"Erro ao buscar dados por categoria: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def fetch_transactions_by_country(start_date, end_date):
    """Busca transações por país da API"""
    try:
        url = f"{API_BASE_URL}/transactions/by-country"
        params = {
            "data_inicio": start_date.strftime("%Y-%m-%d"),
            "data_fim": end_date.strftime("%Y-%m-%d")
        }
        
        response = requests.get(url, params=params)
        
        if not response.ok:
            st.error(f"Erro na API (Status {response.status_code}): {response.text}")
            return None
            
        return response.json()
    
    except Exception as e:
        st.error(f"Erro ao buscar dados por país: {str(e)}")
        return None

def load_data(start_date, end_date):
    """Carrega todos os dados necessários"""
    with st.spinner('Carregando dados...'):
        st.session_state['summary_data'] = fetch_transactions_summary(start_date, end_date)
        st.session_state['category_data'] = fetch_transactions_by_category(start_date, end_date)
        st.session_state['country_data'] = fetch_transactions_by_country(start_date, end_date)
        st.session_state['last_update'] = datetime.now()

def render_overview_tab():
    """Renderiza a aba de visão geral"""
    summary_data = st.session_state['summary_data']
    category_data = st.session_state['category_data']
    
    if not summary_data:
        st.warning("Não há dados de sumário disponíveis")
        return
    
    try:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value = summary_data.get('total_value', 0)
            st.metric(
                "Total de Vendas",
                f"R$ {float(total_value):,.2f}" if total_value else "R$ 0,00"
            )
        
        with col2:
            total_transactions = summary_data.get('total_transactions', 0)
            st.metric(
                "Total de Transações",
                f"{total_transactions:,}" if total_transactions else "0"
            )
        
        with col3:
            unique_customers = summary_data.get('unique_customers', 0)
            st.metric(
                "Clientes Únicos",
                f"{unique_customers:,}" if unique_customers else "0"
            )
        
        with col4:
            avg_price = summary_data.get('average_unit_price', 0)
            st.metric(
                "Ticket Médio",
                f"R$ {float(avg_price):,.2f}" if avg_price else "R$ 0,00"
            )

        # Gráficos de categoria
        if category_data:
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
                    labels={
                        "categoria": "Categoria",
                        "ticket_medio": "Ticket Médio (R$)",
                        "total_vendas": "Volume de Vendas"
                    }
                )
                st.plotly_chart(fig_ticket, use_container_width=True)
        else:
            st.warning("Dados de categoria não disponíveis")
    
    except Exception as e:
        st.error(f"Erro ao renderizar visualizações: {str(e)}")
        st.write("Traceback:", traceback.format_exc())

def render_geographic_tab():
    """Renderiza a aba de análise geográfica"""
    country_data = st.session_state['country_data']
    
    if not country_data:
        st.warning("Dados geográficos não disponíveis")
        return
    
    try:
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
            df_top_value = df_country.nlargest(10, 'valor_total')
            fig_top_value = px.bar(
                df_top_value,
                x='pais',
                y='valor_total',
                title="Top 10 Países por Valor Total"
            )
            st.plotly_chart(fig_top_value, use_container_width=True)
        
        with col2:
            df_top_ticket = df_country.nlargest(10, 'ticket_medio')
            fig_top_ticket = px.bar(
                df_top_ticket,
                x='pais',
                y='ticket_medio',
                title="Top 10 Países por Ticket Médio"
            )
            st.plotly_chart(fig_top_ticket, use_container_width=True)
    
    except Exception as e:
        st.error(f"Erro ao renderizar análise geográfica: {str(e)}")
        st.write("Traceback:", traceback.format_exc())

def main():
    st.title("📊 Análise de Vendas")

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
        st.sidebar.info(
            f"Última atualização: {st.session_state['last_update'].strftime('%d/%m/%Y %H:%M:%S')}"
        )

    # Abas
    tab1, tab2 = st.tabs(["Visão Geral", "Análise Geográfica"])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_geographic_tab()

if __name__ == "__main__":
    main()

###########################################################################################

#Produtos

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

###########################################################################################

#CLientes

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


##################################################################################################
# Downloads
import streamlit as st
import pandas as pd
import requests
from datetime import date
API_BASE_URL = st.secrets["API_BASE_URL"]


# Configuração da página
st.set_page_config(page_title="Download de Dados", layout="wide")



# Dicionário com descrição dos campos
FIELD_DESCRIPTIONS = {
    "id": "Identificador único da transação",
    "created_at": "Data de criação do registro",
    "NumeroFatura": "Número identificador da fatura",
    "CodigoProduto": "Código único do produto",
    "Descricao": "Descrição do produto",
    "Quantidade": "Quantidade de itens vendidos",
    "DataFatura": "Data em que a fatura foi emitida",
    "PrecoUnitario": "Preço unitário do produto",
    "IDCliente": "Identificador único do cliente",
    "Pais": "País onde a venda foi realizada",
    "CategoriaProduto": "Categoria do produto",
    "CategoriaPreco": "Categoria de preço",
    "ValorTotalFatura": "Valor total da fatura",
    "FaturaUnica": "Indica se é uma fatura única",
    "Ano": "Ano da venda",
    "Mes": "Mês da venda",
    "Dia": "Dia da venda",
    "DiaSemana": "Dia da semana (0-6)"
}

# Função para buscar dados
@st.cache_data(ttl=3600)
def fetch_transactions(start_date, end_date):
    try:
        params = {
            "data_inicio": start_date,
            "data_fim": end_date,
            "skip": 0,
            "limit": 10000  # Ajuste conforme necessário
        }

        response = requests.get(
            f"{API_BASE_URL}/transactions/",
            params=params
        )
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Erro na API: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

def main():
    st.title("📥 Download de Dados")
    
    # Descrição da página
    st.markdown("""
    Esta página permite o download dos dados de transações do banco de dados.
    Selecione o período desejado e os campos que deseja incluir no arquivo CSV.
    """)

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

    # Descrição dos campos disponíveis
    with st.expander("Ver descrição dos campos"):
        for field, description in FIELD_DESCRIPTIONS.items():
            st.markdown(f"**{field}**: {description}")

    # Seleção de campos
    st.subheader("Selecione os campos para download")
    
    # Checkbox para selecionar todos
    all_fields = list(FIELD_DESCRIPTIONS.keys())
    if st.checkbox("Selecionar todos os campos", value=True):
        selected_fields = all_fields
    else:
        # Criar múltiplas colunas para os checkboxes
        num_cols = 3
        cols = st.columns(num_cols)
        field_chunks = [all_fields[i::num_cols] for i in range(num_cols)]
        
        selected_fields = []
        for i, col in enumerate(cols):
            with col:
                for field in field_chunks[i]:
                    if st.checkbox(field, key=field):
                        selected_fields.append(field)

    # Botão de download
    if st.button("Gerar CSV"):
        if selected_fields:
            with st.spinner('Carregando dados...'):
                df = fetch_transactions(start_date, end_date)
                
                if df is not None:
                    # Selecionar apenas as colunas escolhidas
                    df = df[selected_fields]
                    
                    # Converter para CSV
                    csv = df.to_csv(index=False)
                    
                    # Botão de download
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"transacoes_{start_date}_{end_date}.csv",
                        mime="text/csv"
                    )
                    
                    # Mostrar preview dos dados
                    st.subheader("Preview dos dados")
                    st.dataframe(df.head())
                    st.info(f"Total de registros: {len(df)}")
        else:
            st.warning("Selecione pelo menos um campo para download.")

if __name__ == "__main__":
    main()

#######################################################################################

#Analise de sentimentos
import streamlit as st
from transformers import pipeline
from datetime import datetime
import pandas as pd

# Configuração inicial do modelo
@st.cache_resource
def load_model():
    """Carrega o modelo BERT multilíngue para análise de sentimento"""
    try:
        model = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {str(e)}")
        return None

def analyze_sentiment(text, analyzer):
    """Analisa o sentimento do texto fornecido"""
    try:
        sentiment_result = analyzer(text)[0]
        
        label = sentiment_result['label']
        score = float(sentiment_result['score'])
        
        polarity = (float(label.split()[0]) - 3) / 2
        
        if polarity > 0:
            sentiment = "Positivo"
            color = "🟢"
        elif polarity < 0:
            sentiment = "Negativo"
            color = "🔴"
        else:
            sentiment = "Neutro"
            color = "⚪"

        return {
            "text": text,
            "sentiment": sentiment,
            "polarity": polarity,
            "score": score,
            "color": color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        st.error(f"Erro ao analisar texto: {str(e)}")
        return None

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise de Sentimentos",
        page_icon="🎭",
        layout="wide"
    )

    # Carregar modelo
    model = load_model()
    if not model:
        st.error("Não foi possível carregar o modelo. Por favor, recarregue a página.")
        return

    # Título e descrição
    st.title("🎭 Análise de Sentimentos em Tempo Real")
    st.markdown("""
    ### Analise sentimentos em textos usando Inteligência Artificial
    Esta ferramenta utiliza um modelo BERT multilíngue para detectar sentimentos em textos.
    """)

    # Layout principal
    col1, col2 = st.columns([2, 1])

    with col1:
        # Área de entrada de texto
        st.subheader("💭 Digite seu texto")
        text_input = st.text_area(
            "Digite o texto para análise",
            height=100,
            placeholder="Escreva aqui o texto que você quer analisar..."
        )

        # Histórico de análises
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []

        # Botão de análise
        if st.button("🔍 Analisar Sentimento", use_container_width=True):
            if text_input.strip():
                result = analyze_sentiment(text_input, model)
                if result:
                    st.session_state.analysis_history.append(result)
                    
                    # Mostrar resultado atual
                    st.success("Análise concluída!")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    with col_res1:
                        st.metric("Sentimento", f"{result['color']} {result['sentiment']}")
                    with col_res2:
                        st.metric("Confiança", f"{result['score']:.2%}")
                    with col_res3:
                        st.metric("Polaridade", f"{result['polarity']:.2f}")
            else:
                st.warning("Por favor, digite algum texto para análise.")

        # Histórico de análises em tabela
        if st.session_state.analysis_history:
            st.subheader("📊 Histórico de Análises")
            df = pd.DataFrame(st.session_state.analysis_history)
            st.dataframe(
                df[['text', 'sentiment', 'score', 'timestamp']],
                hide_index=True,
                use_container_width=True
            )

    with col2:
        st.subheader("⚙️ Controles e Informações")
        
        # Botão para limpar histórico
        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state.analysis_history = []
            st.experimental_rerun()

        # Estatísticas
        if st.session_state.analysis_history:
            st.subheader("📈 Estatísticas")
            total = len(st.session_state.analysis_history)
            positivos = sum(1 for x in st.session_state.analysis_history if x['sentiment'] == 'Positivo')
            negativos = sum(1 for x in st.session_state.analysis_history if x['sentiment'] == 'Negativo')
            neutros = total - positivos - negativos

            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Positivos", f"{positivos} ({(positivos/total)*100:.1f}%)")
            with col_stat2:
                st.metric("Negativos", f"{negativos} ({(negativos/total)*100:.1f}%)")
            with col_stat3:
                st.metric("Neutros", f"{neutros} ({(neutros/total)*100:.1f}%)")

        # Informações sobre o modelo
        st.subheader("ℹ️ Sobre o Modelo")
        st.markdown("""
        **Modelo:** BERT Multilíngue
        
        **Capacidades:**
        - Análise de textos em múltiplos idiomas
        - Detecção de sentimentos: Positivo, Negativo, Neutro
        - Pontuação de confiança para cada análise
        
        **Como interpretar:**
        - 🟢 Positivo: Sentimento favorável
        - ⚪ Neutro: Sentimento ambíguo ou neutral
        - 🔴 Negativo: Sentimento desfavorável
        
        A pontuação de confiança indica o quão seguro o modelo está da sua análise.
        """)

if __name__ == "__main__":
    main()
