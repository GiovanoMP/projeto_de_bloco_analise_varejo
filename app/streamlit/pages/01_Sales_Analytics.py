# Importações necessárias
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime, timedelta
import calendar
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração inicial da página
st.set_page_config(
    page_title="RetailSense AI - Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Configurações da API e constantes
SUPABASE_URL = st.secrets["supabase"]["url"]  
SUPABASE_KEY = st.secrets["supabase"]["key"] 
API_BASE_URL = f"{SUPABASE_URL}/analytics-api"

# Configurações de headers padrão
DEFAULT_HEADERS = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
DEFAULT_YEAR = 2011
DATE_MIN = datetime(DEFAULT_YEAR, 1, 1)
DATE_MAX = datetime(DEFAULT_YEAR, 12, 31)


@st.cache_data(ttl=3600)
def get_sales_data(start_date, end_date):
    """Busca dados de vendas"""
    try:
        logger.info(f"Buscando dados de vendas para o período: {start_date} até {end_date}")

        url = f"{API_BASE_URL}/sales"
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.get(
            url=url,
            headers=DEFAULT_HEADERS,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            logger.info("Dados de vendas recuperados com sucesso")
            return data
        else:
            logger.error(f"Erro na API (Status {response.status_code}): {response.text}")
            st.error(f"Erro ao carregar dados de vendas (Status {response.status_code})")
            return None

    except Exception as e:
        logger.error(f"Erro ao conectar com a API de vendas: {str(e)}")
        st.error("Erro ao carregar dados. Verifique a conexão com a API.")
        return None


@st.cache_data(ttl=3600)
def get_temporal_data(start_date, end_date, window=7):
    """Busca dados temporais de vendas"""
    try:
        logger.info(f"Buscando dados temporais para o período: {start_date} até {end_date}, janela: {window}")

        url = f"{API_BASE_URL}/sales/temporal"
        params = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "window": window
        }

        response = requests.get(
            url=url,
            headers=DEFAULT_HEADERS,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            logger.info("Dados temporais recuperados com sucesso")
            return data
        else:
            logger.error(f"Erro na API temporal (Status {response.status_code}): {response.text}")
            st.error(f"Erro ao carregar dados temporais (Status {response.status_code})")
            return None

    except Exception as e:
        logger.error(f"Erro ao conectar com a API temporal: {str(e)}")
        st.error("Erro ao carregar dados temporais. Verifique a conexão com a API.")
        return None


# Funções auxiliares
def format_currency(value):
    return f"R$ {value:,.2f}"


def test_api_connection():
    """Testa a conexão com a API"""
    st.write("Testando conexão com a API...")

    # Teste 1: get_sales_data
    test_start = DATE_MIN
    test_end = test_start + timedelta(days=30)

    st.write("### Teste 1: Dados de Vendas")
    sales_result = get_sales_data(test_start, test_end)
    if sales_result:
        st.write("✅ Conexão com dados de vendas OK")
        st.write("Exemplo de dados:", sales_result)
    else:
        st.write("❌ Erro na conexão com dados de vendas")

    # Teste 2: get_temporal_data
    st.write("### Teste 2: Dados Temporais")
    temporal_result = get_temporal_data(test_start, test_end)
    if temporal_result:
        st.write("✅ Conexão com dados temporais OK")
        st.write("Exemplo de dados:", temporal_result)
    else:
        st.write("❌ Erro na conexão com dados temporais")


def calculate_metrics(temporal_data):
    """Calcula métricas adicionais"""
    if temporal_data is None:
        return None

    df = pd.DataFrame(temporal_data)
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.dayofweek

    monthly_data = df.groupby('month').agg({
        'total_sales': 'sum',
        'transactions': 'sum',
        'unique_customers': 'mean'
    }).reset_index()

    daily_data = df.groupby('day_of_week').agg({
        'total_sales': 'mean',
        'transactions': 'mean'
    }).reset_index()

    daily_data['day_name'] = daily_data['day_of_week'].apply(lambda x: calendar.day_name[x])

    return {
        'monthly_data': monthly_data,
        'daily_data': daily_data,
        'trends': {
            'best_day': daily_data.loc[daily_data['total_sales'].idxmax(), 'day_name'],
            'best_month': calendar.month_name[monthly_data.loc[monthly_data['total_sales'].idxmax(), 'month']],
            'avg_ticket_trend': (df['total_sales'] / df['transactions']).mean(),
            'customer_frequency': (df['transactions'] / df['unique_customers']).mean()
        }
    }


def create_sales_chart(temporal_data, window):
    """Cria gráfico de vendas"""
    fig = go.Figure()

    df = pd.DataFrame(temporal_data)

    # Vendas diárias
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total_sales'],
        name='Vendas Diárias',
        mode='lines',
        line=dict(color='#4287f5', width=2)
    ))

    # Média móvel
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['moving_avg_sales'],
        name=f'Média Móvel ({window} dias)',
        mode='lines',
        line=dict(color='#ff6b3d', width=2, dash='dash')
    ))

    fig.update_layout(
        title='Evolução de Vendas',
        template='plotly_dark',
        xaxis_title='Data',
        yaxis_title='Vendas (R$)',
        hovermode='x unified'
    )

    return fig


def create_sales_dashboard(sales_data, temporal_data, advanced_metrics):
    """Cria dashboard completo de vendas"""

    # KPIs Principais
    st.markdown("### Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total de Vendas", format_currency(sales_data['total_sales']))
    with col2:
        st.metric("Ticket Médio", format_currency(sales_data['average_ticket']))
    with col3:
        st.metric("Clientes Únicos", f"{sales_data['total_customers']:,}")
    with col4:
        st.metric("Total Transações", f"{sales_data['total_transactions']:,}")

    # Gráficos em Tabs
    tab1, tab2, tab3 = st.tabs(["📈 Tendências", "📊 Análise Temporal", "🎯 Insights"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            # Vendas por Dia da Semana
            fig_daily = px.bar(
                advanced_metrics['daily_data'],
                x='day_name',
                y='total_sales',
                title='Média de Vendas por Dia da Semana',
                labels={'total_sales': 'Vendas (R$)', 'day_name': 'Dia'},
                color='total_sales',
                color_continuous_scale='Viridis'
            )
            fig_daily.update_layout(template='plotly_dark')
            st.plotly_chart(fig_daily, use_container_width=True)

        with col2:
            # Vendas Mensais
            fig_monthly = px.line(
                advanced_metrics['monthly_data'],
                x='month',
                y=['total_sales', 'transactions'],
                title='Evolução Mensal',
                labels={'value': 'Valor', 'month': 'Mês'},
                color_discrete_sequence=['#00ff7f', '#00bfff']
            )
            fig_monthly.update_layout(template='plotly_dark')
            st.plotly_chart(fig_monthly, use_container_width=True)

    with tab2:
        # Gráfico temporal principal
        st.plotly_chart(create_sales_chart(temporal_data, 7), use_container_width=True)

        # Distribuição de vendas
        df_temp = pd.DataFrame(temporal_data)
        fig_dist = px.histogram(
            df_temp,
            x='total_sales',
            nbins=30,
            title='Distribuição das Vendas Diárias',
            labels={'total_sales': 'Valor de Vendas'},
            color_discrete_sequence=['#4287f5']
        )
        fig_dist.update_layout(template='plotly_dark')
        st.plotly_chart(fig_dist, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Insights Principais")
            st.info(f"""
            - **Melhor Dia**: {advanced_metrics['trends']['best_day']}
            - **Melhor Mês**: {advanced_metrics['trends']['best_month']}
            - **Frequência Média**: {advanced_metrics['trends']['customer_frequency']:.2f} compras/cliente
            - **Ticket Médio**: {format_currency(advanced_metrics['trends']['avg_ticket_trend'])}
            """)

        with col2:
            st.markdown("### 📈 Oportunidades")
            st.success(f"""
            - **Taxa de Conversão**: {(sales_data['total_transactions']/sales_data['total_customers']):.1f} compras/cliente
            - **Potencial de Crescimento**: {format_currency(advanced_metrics['trends']['avg_ticket_trend'] * 1.2)}
            - **Meta Sugerida**: +20% sobre média atual
            """)


def main():
    st.title("📊 Análise de Vendas")

    # Botão de teste de API
    if st.button("🔍 Testar Conexão com API"):
        test_api_connection()
        return

    st.markdown("Dashboard completo de métricas e insights de vendas")

    # Sidebar
    with st.sidebar:
        st.header("Filtros")

        start_date = st.date_input(
            "Data Inicial",
            value=DATE_MIN.date(),
            min_value=DATE_MIN.date(),
            max_value=DATE_MAX.date()
        )

        end_date = st.date_input(
            "Data Final",
            value=DATE_MAX.date(),
            min_value=DATE_MIN.date(),
            max_value=DATE_MAX.date()
        )

        window = st.slider(
            "Janela da Média Móvel (dias)",
            min_value=3,
            max_value=30,
            value=7
        )

        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()

        # Adicionar separador
        st.markdown("---")

        # Seção de Importar/Exportar
        st.subheader("📈 Importar/Exportar")

        # Upload de CSV
        uploaded_file = st.file_uploader(
            "Importar CSV",
            type=['csv'],
            help="O arquivo deve incluir: DataFatura, ValorTotalFatura, IDCliente"
        )

        if uploaded_file:
            try:
                df_upload = pd.read_csv(uploaded_file)
                required_cols = ["DataFatura", "ValorTotalFatura", "IDCliente"]

                if all(col in df_upload.columns for col in required_cols):
                    df_upload['DataFatura'] = pd.to_datetime(df_upload['DataFatura'])

                    with st.expander("👀 Preview dos Dados"):
                        st.dataframe(df_upload.head())
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Total Registros", len(df_upload))
                        with col2:
                            st.metric("Período", f"{df_upload['DataFatura'].min().strftime('%d/%m/%Y')} - {df_upload['DataFatura'].max().strftime('%d/%m/%Y')}")
                else:
                    st.error("❌ Formato inválido - Verifique as colunas necessárias")
            except Exception as e:
                st.error(f"❌ Erro ao processar arquivo: {str(e)}")

    # Validação de datas
    if start_date > end_date:
        st.error("A data inicial deve ser anterior à data final!")
        return

    # Carregar e processar dados
    with st.spinner("Carregando dados..."):
        sales_data = get_sales_data(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time())
        )

        temporal_data = get_temporal_data(
            datetime.combine(start_date, datetime.min.time()),
            datetime.combine(end_date, datetime.max.time()),
            window
        )

        if sales_data and temporal_data is not None:
            advanced_metrics = calculate_metrics(temporal_data)
            create_sales_dashboard(sales_data, temporal_data, advanced_metrics)
        else:
            st.error("Erro ao carregar dados. Verifique a conexão com a API.")


if __name__ == "__main__":
    main()