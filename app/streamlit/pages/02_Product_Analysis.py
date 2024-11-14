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
    """Busca dados de produtos da API"""
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
    """Calcula métricas gerais dos produtos"""
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

def generate_product_insights(df: pd.DataFrame) -> Dict[str, Dict]:
    """Gera insights baseados nos dados dos produtos"""
    try:
        insights = {}
        
        # Insight 1: Concentração de Receita
        top_5_revenue = df.nlargest(5, 'total_revenue')
        top_5_percentage = (top_5_revenue['total_revenue'].sum() / df['total_revenue'].sum()) * 100
        
        insights['revenue_concentration'] = {
            'title': '📊 Concentração de Receita',
            'description': f"Os top 5 produtos representam {top_5_percentage:.1f}% da receita total",
            'impact': 'alto' if top_5_percentage > 50 else 'médio',
            'recommendation': """
                * Diversificar portfólio se concentração for muito alta
                * Garantir estoque adequado dos produtos principais
                * Desenvolver estratégias de cross-selling
            """ if top_5_percentage > 50 else "Manter estratégia atual de diversificação"
        }
        
        # Insight 2: Análise de Preços
        avg_price_category = df.groupby('price_category')['total_quantity'].sum()
        top_price_category = avg_price_category.idxmax()
        price_preference = (avg_price_category[top_price_category] / avg_price_category.sum()) * 100
        
        insights['price_sensitivity'] = {
            'title': '💰 Sensibilidade a Preço',
            'description': f"Categoria de preço '{top_price_category}' representa {price_preference:.1f}% das vendas",
            'impact': 'alto' if price_preference > 40 else 'médio',
            'recommendation': "Considerar estratégias de precificação dinâmica e promoções direcionadas"
        }
        
        # Insight 3: Oportunidades por Categoria
        category_metrics = df.groupby('category').agg({
            'total_revenue': 'sum',
            'total_quantity': 'sum'
        })
        category_metrics['avg_ticket'] = category_metrics['total_revenue'] / category_metrics['total_quantity']
        
        high_ticket_category = category_metrics['avg_ticket'].idxmax()
        high_ticket_value = category_metrics.loc[high_ticket_category, 'avg_ticket']
        
        insights['category_opportunity'] = {
            'title': '🎯 Oportunidades por Categoria',
            'description': f"Categoria '{high_ticket_category}' tem o maior ticket médio (R$ {high_ticket_value:.2f})",
            'impact': 'médio',
            'recommendation': """
                * Aumentar foco em categorias de alto ticket
                * Desenvolver bundles de produtos
                * Implementar programa de fidelidade por categoria
            """
        }
        
        # Insight 4: Sustentabilidade (ESG)
        low_moving_products = df[df['total_quantity'] < df['total_quantity'].quantile(0.25)]
        slow_moving_percentage = (len(low_moving_products) / len(df)) * 100
        
        insights['sustainability'] = {
            'title': '🌱 Sustentabilidade e Eficiência',
            'description': f"{slow_moving_percentage:.1f}% dos produtos têm baixa rotatividade",
            'impact': 'alto' if slow_moving_percentage > 30 else 'médio',
            'recommendation': """
                * Otimizar gestão de estoque
                * Reduzir desperdícios
                * Considerar promoções para produtos de baixo giro
                * Implementar práticas sustentáveis na gestão de estoque
            """
        }
        
        return insights
    
    except Exception as e:
        logger.error(f"Erro ao gerar insights: {str(e)}")
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

def filter_dataframe(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """Aplica filtros ao DataFrame"""
    try:
        filtered_df = df.copy()
        
        if filters.get("category"):
            filtered_df = filtered_df[filtered_df["category"] == filters["category"]]
            
        if filters.get("price_range"):
            filtered_df = filtered_df[filtered_df["price_category"] == filters["price_range"]]
            
        if filters.get("view_type") == "Top Produtos" and filters.get("top_n"):
            filtered_df = filtered_df.nlargest(filters["top_n"], "total_revenue")
            
        return filtered_df
    
    except Exception as e:
        logger.error(f"Erro ao filtrar dados: {str(e)}")
        return df

def main():
    # Título e descrição
    st.title("📦 Análise de Produtos")
    st.markdown("""
        Dashboard completo para análise de performance dos produtos, incluindo métricas 
        de vendas, distribuições e insights.
    """)
    
    # Carregar dados
    with st.spinner("Carregando dados dos produtos..."):
        products_data = get_product_data()
        
        if not products_data:
            st.error("Não foi possível carregar os dados dos produtos.")
            return
        
        df = pd.DataFrame(products_data)
        
    # Sidebar com filtros
    st.sidebar.header("📊 Filtros de Análise")
    
    # Tipo de Visualização
    st.sidebar.subheader("🎯 Tipo de Visualização")
    view_type = st.sidebar.radio(
        "Selecione o tipo de análise:",
        options=["Todos os Produtos", "Top Produtos", "Por Categoria"],
        index=0,
        help="Escolha como deseja visualizar os dados"
    )
    
    top_n = None
    if view_type == "Top Produtos":
        top_n = st.sidebar.slider(
            "Quantidade de produtos",
            min_value=5,
            max_value=50,
            value=10,
            step=5,
            help="Selecione quantos produtos deseja visualizar"
        )
    
    st.sidebar.markdown("---")
    
    # Categorias
    st.sidebar.subheader("📦 Categorias")
    category_options = ["Todas"] + sorted(df['category'].unique().tolist())
    selected_category = st.sidebar.radio(
        "Selecione uma categoria:",
        options=category_options,
        index=0,
        help="Filtrar por categoria específica"
    )
    
    st.sidebar.markdown("---")
    
    # Faixa de Preço
    st.sidebar.subheader("💰 Faixa de Preço")
    price_options = ["Todas"] + sorted(df['price_category'].unique().tolist())
    selected_price = st.sidebar.radio(
        "Selecione uma faixa de preço:",
        options=price_options,
        index=0,
        help="Filtrar por faixa de preço"
    )
    
    # Aplicar filtros
    filters = {
        "view_type": view_type,
        "top_n": top_n,
        "category": None if selected_category == "Todas" else selected_category,
        "price_range": None if selected_price == "Todas" else selected_price
    }
    
    df_filtered = filter_dataframe(df, filters)
    metrics = calculate_product_metrics(df_filtered)
    
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
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visão Geral",
        "📈 Distribuições",
        "💰 Preços",
        "💡 Insights"
    ])
    
    with tab1:
        # Top produtos
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
        price_data = df_filtered.groupby('price_category').agg({
            'total_revenue': 'sum',
            'total_quantity': 'sum'
        }).reset_index()
        
        price_data['avg_price'] = price_data['total_revenue'] / price_data['total_quantity']
        
        # Gráfico de análise de preços
        fig_price = px.bar(
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
        fig_price.update_layout(template='plotly_dark', height=400)
        st.plotly_chart(fig_price, use_container_width=True)
        
        # Análise de margem por faixa de preço
        st.subheader("📊 Distribuição de Vendas por Faixa de Preço")
        
        col1, col2 = st.columns(2)
        with col1:
            # Gráfico de pizza para distribuição de receita
            fig_pie = px.pie(
                price_data,
                values='total_revenue',
                names='price_category',
                title='Distribuição da Receita',
                hole=0.4
            )
            fig_pie.update_layout(template='plotly_dark')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Tabela com métricas detalhadas
            st.markdown("### Métricas por Faixa de Preço")
            price_metrics = price_data.copy()
            price_metrics['receita'] = price_metrics['total_revenue'].apply(format_currency)
            price_metrics['preço_médio'] = price_metrics['avg_price'].apply(format_currency)
            price_metrics['quantidade'] = price_metrics['total_quantity'].apply(format_number)
            
            st.dataframe(
                price_metrics[['price_category', 'receita', 'quantidade', 'preço_médio']],
                column_config={
                    'price_category': 'Faixa de Preço',
                    'receita': 'Receita Total',
                    'quantidade': 'Quantidade',
                    'preço_médio': 'Preço Médio'
                },
                use_container_width=True
            )
    
    with tab4:
        st.subheader("💡 Insights e Recomendações")
        
        insights = generate_product_insights(df_filtered)
        
        # Dividir insights em duas colunas
        col1, col2 = st.columns(2)
        
        insight_columns = {
            0: [insights['revenue_concentration'], insights['category_opportunity']],
            1: [insights['price_sensitivity'], insights['sustainability']]
        }
        
        for col_idx, col_insights in insight_columns.items():
            with col1 if col_idx == 0 else col2:
                for insight in col_insights:
                    with st.expander(f"{insight['title']} | Impacto: {insight['impact'].upper()}", expanded=True):
                        st.markdown(f"**Análise:** {insight['description']}")
                        st.markdown("**Recomendações:**")
                        st.markdown(insight['recommendation'])
        
        # Métricas de sustentabilidade
        st.markdown("---")
        st.subheader("🌱 Métricas de Sustentabilidade")
        
        sus_col1, sus_col2, sus_col3 = st.columns(3)
        
        with sus_col1:
            efficiency_score = (1 - len(df_filtered[df_filtered['total_quantity'] < df_filtered['total_quantity'].quantile(0.25)]) / len(df_filtered)) * 100
            st.metric(
                "Eficiência de Portfólio",
                f"{efficiency_score:.1f}%",
                help="Percentual de produtos com boa performance"
            )
        
        with sus_col2:
            stock_health = 100 - float(insights['sustainability']['description'].split('%')[0])
            st.metric(
                "Saúde do Estoque",
                f"{stock_health:.1f}%",
                help="Percentual de produtos com rotatividade adequada"
            )
        
        with sus_col3:
            category_efficiency = (df_filtered.groupby('category')['total_quantity'].sum() / df_filtered['total_quantity'].sum() * 100).max()
            st.metric(
                "Diversificação de Categorias",
                f"{100 - category_efficiency:.1f}%",
                help="Nível de diversificação do portfólio entre categorias"
            )
    
    # Dados detalhados
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