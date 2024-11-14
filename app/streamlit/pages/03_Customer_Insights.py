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
    page_title="RetailSense AI - Insights de Clientes",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações da API e constantes
API_BASE_URL = "http://localhost:8000/api/v1/analytics"

# Funções de API
@st.cache_data(ttl=3600)
def get_customer_data() -> Optional[Dict]:
    """Busca dados de clientes da API"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/customers",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erro na API de clientes (Status {response.status_code})")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao conectar com a API de clientes: {str(e)}")
        st.error(f"Erro ao carregar dados de clientes: {str(e)}")
        return None

# Funções auxiliares
def format_currency(value: float) -> str:
    """Formata valor para moeda brasileira"""
    return f"R$ {value:,.2f}"

def format_number(value: float) -> str:
    """Formata números com separadores de milhar"""
    return f"{value:,.0f}"

def create_segment_sankey(data: Dict) -> go.Figure:
    """Cria diagrama Sankey para visualização de segmentos"""
    try:
        segments = data['customer_segments']
        
        # Preparar dados para o diagrama Sankey
        nodes = ['Total'] + list(segments.keys())
        
        # Calcular valores
        total = sum(seg['customer_count'] for seg in segments.values())
        values = [float(seg['customer_count']) for seg in segments.values()]
        
        # Criar figura
        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 15,
                thickness = 20,
                line = dict(color = "white", width = 0.5),
                label = nodes,
                color = ["#2196F3"] + ["#4CAF50", "#FFC107", "#FF5722", "#9C27B0"][:len(segments)]
            ),
            link = dict(
                source = [0] * len(segments),  # Todos começam do total
                target = list(range(1, len(segments) + 1)),  # Ligam aos segmentos
                value = values,
                color = ["rgba(76, 175, 80, 0.3)", "rgba(255, 193, 7, 0.3)", 
                        "rgba(255, 87, 34, 0.3)", "rgba(156, 39, 176, 0.3)"][:len(segments)]
            )
        )])

        fig.update_layout(
            title="Distribuição de Clientes por Segmento",
            template='plotly_dark',
            font=dict(size=12, color='white'),
            height=400
        )
        
        return fig
    except Exception as e:
        logger.error(f"Erro ao criar diagrama Sankey: {str(e)}")
        return None

def create_segment_metrics(data: Dict) -> Dict[str, Dict]:
    """Cria métricas por segmento"""
    try:
        segments = data['customer_segments']
        total_customers = data['total_unique_customers']
        
        metrics = {}
        for name, info in segments.items():
            metrics[name] = {
                'count': info['customer_count'],
                'percentage': (info['customer_count'] / total_customers) * 100,
                'avg_value': info['average_value'],
                'status': 'up' if info['average_value'] > data['average_customer_value'] else 'down'
            }
        
        return metrics
    except Exception as e:
        logger.error(f"Erro ao calcular métricas por segmento: {str(e)}")
        return {}

def main():
    # Título e descrição
    st.title("👥 Insights de Clientes")
    st.markdown("""
        Análise detalhada da base de clientes, incluindo segmentação, comportamento de compra
        e oportunidades identificadas.
    """)
    
    # Carregar dados
    with st.spinner("Carregando dados dos clientes..."):
        customer_data = get_customer_data()
        
        if not customer_data:
            st.error("Não foi possível carregar os dados dos clientes.")
            return

    # Criar métricas por segmento
    segment_metrics = create_segment_metrics(customer_data)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Clientes",
            format_number(customer_data['total_unique_customers']),
            help="Número total de clientes únicos"
        )
    
    with col2:
        st.metric(
            "Valor Médio por Cliente",
            format_currency(customer_data['average_customer_value']),
            help="Valor médio gasto por cliente"
        )
    
    with col3:
        total_segments = len(customer_data['customer_segments'])
        st.metric(
            "Segmentos",
            str(total_segments),
            help="Número de segmentos de clientes"
        )
    
    with col4:
        top_country = customer_data['top_countries'][0]
        st.metric(
            "Principal País",
            f"{top_country['country']}",
            f"{format_number(top_country['customer_count'])} clientes",
            help="País com maior número de clientes"
        )

    # Tabs de análise
    tab1, tab2, tab3 = st.tabs([
        "🎯 Segmentação",
        "🌍 Geografia",
        "💡 Insights"
    ])
    
    with tab1:
        # Visão geral dos segmentos
        st.markdown("### Visão Geral dos Segmentos")
        
        # Diagrama Sankey
        fig_sankey = create_segment_sankey(customer_data)
        if fig_sankey:
            st.plotly_chart(fig_sankey, use_container_width=True)
        
        # Detalhes dos segmentos
        st.markdown("### 📊 Análise Detalhada por Segmento")
        
        # Grid de cards de segmentos
        for i in range(0, len(segment_metrics), 2):
            col1, col2 = st.columns(2)
            
            segments = list(segment_metrics.items())
            for j, col in enumerate([col1, col2]):
                if i + j < len(segments):
                    name, metrics = segments[i + j]
                    with col:
                        st.markdown(
                            f"""
                            <div style="
                                padding: 20px;
                                border-radius: 10px;
                                background-color: rgba(255, 255, 255, 0.1);
                                margin-bottom: 20px;
                            ">
                                <h3>{name}</h3>
                                <p>
                                    🎯 {format_number(metrics['count'])} clientes ({metrics['percentage']:.1f}%)<br>
                                    💰 Valor médio: {format_currency(metrics['avg_value'])}<br>
                                    📈 Performance: {'↗️ Acima' if metrics['status'] == 'up' else '↘️ Abaixo'} da média
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    
    with tab2:
        st.markdown("### 🌍 Distribuição Geográfica")
        
        # Métricas por país
        country_data = pd.DataFrame(customer_data['top_countries'])
        
        # Gráfico de barras para países
        fig_countries = px.bar(
            country_data,
            x='country',
            y='customer_count',
            color='average_spend',
            title='Distribuição de Clientes por País',
            labels={
                'country': 'País',
                'customer_count': 'Número de Clientes',
                'average_spend': 'Gasto Médio (R$)'
            },
            color_continuous_scale='Viridis'
        )
        fig_countries.update_layout(template='plotly_dark')
        st.plotly_chart(fig_countries, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("### 📊 Detalhamento por País")
        
        # Formatar dados para exibição
        display_data = country_data.copy()
        display_data['average_spend'] = display_data['average_spend'].apply(format_currency)
        display_data['customer_count'] = display_data['customer_count'].apply(format_number)
        
        st.dataframe(
            display_data,
            column_config={
                'country': 'País',
                'customer_count': 'Número de Clientes',
                'average_spend': 'Gasto Médio'
            },
            use_container_width=True
        )
    
    with tab3:
        st.markdown("### 💡 Insights e Oportunidades")
        
        # Criar cards de insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                #### 🎯 Segmentação
                - **Champions** representam 27% da base
                - Foco em retenção e programas premium
                - Potencial para embaixadores da marca
                
                #### 💰 Valor
                - Ticket médio varia significativamente
                - Oportunidade de up-selling
                - Programas de fidelidade personalizados
                """,
            )
        
        with col2:
            st.markdown(
                """
                #### 🌍 Geografia
                - Concentração em mercados principais
                - Oportunidade de expansão
                - Adaptação local de estratégias
                
                #### ⚠️ Atenção
                - 34.3% dos clientes em risco
                - Necessidade de reengajamento
                - Campanhas de reativação
                """,
            )
        
        # Recomendações
        st.markdown("### 📋 Recomendações Práticas")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
                #### Curto Prazo (1-3 meses)
                - Implementar programa de fidelidade
                - Campanha de reativação
                - Melhorar comunicação
            """)
        
        with col2:
            st.warning("""
                #### Médio Prazo (3-6 meses)
                - Desenvolver segmentação dinâmica
                - Criar jornadas personalizadas
                - Implementar sistema de alertas
            """)
        
        with col3:
            st.success("""
                #### Longo Prazo (6-12 meses)
                - Expandir para novos mercados
                - Desenvolver programa VIP
                - Automatizar campanhas
            """)

if __name__ == "__main__":
    main()