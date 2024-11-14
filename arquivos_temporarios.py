import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import requests
from datetime import datetime, timedelta
import calendar
import logging
from typing import Dict, List, Optional

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração inicial da página
st.set_page_config(
    page_title="RetailSense AI - Análise de Produtos",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações da API e constantes
API_BASE_URL = "http://localhost:8000/api/v1/analytics"
DEFAULT_YEAR = 2011

# Funções de API
@st.cache_data(ttl=3600)
def get_product_data(limit: int = 50) -> Optional[List[Dict]]:
    """
    Busca dados de produtos da API
    
    Args:
        limit: Número máximo de produtos a retornar
        
    Returns:
        Lista de produtos com suas métricas ou None em caso de erro
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/products",
            params={"limit": limit},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API de produtos (Status {response.status_code})")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao conectar com a API de produtos: {str(e)}")
        st.error(f"Erro ao carregar dados de produtos: {str(e)}")
        return None

# Funções auxiliares
def format_currency(value: float) -> str:
    """Formata valor para moeda brasileira"""
    return f"R$ {value:,.2f}"

def format_number(value: float) -> str:
    """Formata números com separadores de milhar"""
    return f"{value:,.0f}"

def calculate_product_metrics(df: pd.DataFrame) -> Dict:
    """
    Calcula métricas gerais dos produtos
    
    Args:
        df: DataFrame com dados dos produtos
        
    Returns:
        Dicionário com métricas calculadas
    """
    try:
        metrics = {
            "total_revenue": df["total_revenue"].sum(),
            "total_quantity": df["total_quantity"].sum(),
            "avg_price": df["total_revenue"].sum() / df["total_quantity"].sum(),
            "unique_products": len(df),
            "categories": df["category"].nunique(),
            "top_category": df.groupby("category")["total_revenue"].sum().idxmax(),
            "best_seller": df.loc[df["total_quantity"].idxmax(), "description"]
        }
        return metrics
    except Exception as e:
        logger.error(f"Erro ao calcular métricas: {str(e)}")
        return {}

def create_product_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de distribuição de produtos"""
    try:
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Distribuição por Receita', 'Distribuição por Quantidade')
        )
        
        # Distribuição por receita
        fig.add_trace(
            go.Histogram(
                x=df['total_revenue'],
                name='Receita',
                nbinsx=30,
                marker_color='#4CAF50'
            ),
            row=1, col=1
        )
        
        # Distribuição por quantidade
        fig.add_trace(
            go.Histogram(
                x=df['total_quantity'],
                name='Quantidade',
                nbinsx=30,
                marker_color='#2196F3'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            template='plotly_dark',
            showlegend=False,
            title_text="Distribuição de Produtos",
            height=400
        )
        
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar gráfico de distribuição: {str(e)}")
        return None

def create_category_analysis(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de análise por categorias"""
    try:
        category_data = df.groupby('category').agg({
            'total_revenue': 'sum',
            'total_quantity': 'sum'
        }).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=category_data['category'],
            y=category_data['total_revenue'],
            name='Receita',
            marker_color='#4CAF50'
        ))
        
        fig.add_trace(go.Scatter(
            x=category_data['category'],
            y=category_data['total_quantity'],
            name='Quantidade',
            yaxis='y2',
            marker_color='#2196F3'
        ))
        
        fig.update_layout(
            template='plotly_dark',
            title='Análise por Categoria',
            yaxis=dict(title='Receita Total (R$)'),
            yaxis2=dict(title='Quantidade', overlaying='y', side='right'),
            height=500,
            showlegend=True
        )
        
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar análise por categoria: {str(e)}")
        return None

def create_price_analysis(df: pd.DataFrame) -> go.Figure:
    """Cria gráfico de análise de preços"""
    try:
        price_data = df.groupby('price_category').agg({
            'total_revenue': 'sum',
            'total_quantity': 'sum'
        }).reset_index()
        
        price_data['avg_price'] = price_data['total_revenue'] / price_data['total_quantity']
        
        fig = px.bar(
            price_data,
            x='price_category',
            y='total_revenue',
            color='avg_price',
            title='Análise por Faixa de Preço',
            labels={
                'price_category': 'Faixa de Preço',
                'total_revenue': 'Receita Total (R$)',
                'avg_price': 'Preço Médio (R$)'
            },
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(template='plotly_dark', height=400)
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar análise de preços: {str(e)}")
        return None

def main():
    # Título e descrição
    st.title("📦 Análise de Produtos")
    st.markdown("""
        Dashboard completo para análise de performance dos produtos, incluindo métricas 
        de vendas, distribuições e tendências por categoria.
    """)
    
    # Carregar dados
    with st.spinner("Carregando dados dos produtos..."):
        products_data = get_product_data()
        
        if not products_data:
            st.error("Não foi possível carregar os dados dos produtos.")
            return
        
        df = pd.DataFrame(products_data)
        metrics = calculate_product_metrics(df)
    
    # Sidebar com filtros
    with st.sidebar:
        st.header("Filtros")
        
        # Filtro de categorias
        categories = sorted(df['category'].unique())
        selected_categories = st.multiselect(
            "Categorias",
            options=categories,
            default=categories[:3],
            help="Selecione as categorias de produtos"
        )
        
        # Filtro de faixa de preço
        price_ranges = sorted(df['price_category'].unique())
        selected_price_ranges = st.multiselect(
            "Faixas de Preço",
            options=price_ranges,
            default=price_ranges,
            help="Selecione as faixas de preço"
        )
        
        # Limpar filtros
        if st.button("🔄 Limpar Filtros"):
            selected_categories = categories
            selected_price_ranges = price_ranges
    
    # Aplicar filtros
    mask = df['category'].isin(selected_categories) & df['price_category'].isin(selected_price_ranges)
    df_filtered = df[mask]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Receita Total",
            format_currency(metrics["total_revenue"]),
            help="Receita total gerada pelos produtos"
        )
    
    with col2:
        st.metric(
            "Quantidade Vendida",
            format_number(metrics["total_quantity"]),
            help="Quantidade total de itens vendidos"
        )
    
    with col3:
        st.metric(
            "Preço Médio",
            format_currency(metrics["avg_price"]),
            help="Preço médio por unidade"
        )
    
    with col4:
        st.metric(
            "Produtos Únicos",
            format_number(metrics["unique_products"]),
            help="Número de produtos diferentes"
        )
    
    # Tabs com análises
    tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "📈 Distribuições", "💰 Preços"])
    
    with tab1:
        # Top 10 produtos
        st.subheader("Top 10 Produtos por Receita")
        top_products = df_filtered.nlargest(10, 'total_revenue')
        
        fig = px.bar(
            top_products,
            x='description',
            y='total_revenue',
            color='category',
            title='Produtos Mais Vendidos',
            labels={
                'description': 'Produto',
                'total_revenue': 'Receita Total (R$)',
                'category': 'Categoria'
            }
        )
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
        # Análise por categoria
        st.plotly_chart(
            create_category_analysis(df_filtered),
            use_container_width=True
        )
    
    with tab2:
        # Gráficos de distribuição
        st.plotly_chart(
            create_product_distribution_chart(df_filtered),
            use_container_width=True
        )
    
    with tab3:
        # Análise de preços
        st.plotly_chart(
            create_price_analysis(df_filtered),
            use_container_width=True
        )
    
    # Detalhes dos produtos
    with st.expander("📋 Dados Detalhados"):
        st.dataframe(
            df_filtered.sort_values('total_revenue', ascending=False),
            use_container_width=True
        )
        
        # Opção de download
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "produtos_analise.csv",
            "text/csv",
            key='download-csv'
        )

if __name__ == "__main__":
    main()