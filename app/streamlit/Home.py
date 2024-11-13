import streamlit as st
import requests
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="RetailSense AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
def local_css():
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stTitle {
            color: #2c3e50;
            font-size: 48px !important;
        }
        .stSubheader {
            color: #34495e;
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

# Cabeçalho
col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("app/static/logo.svg", width=100, use_container_width=True)  # Parâmetro atualizado
    except Exception as e:
        st.error(f"Erro ao carregar logo: {str(e)}")
with col2:
    st.title("RetailSense AI")
    st.subheader("Inteligência em Varejo e Sustentabilidade")

# Informações adicionais
st.markdown("---")
st.markdown("""
### Sobre o RetailSense AI

O RetailSense AI é uma solução avançada de análise de dados para o varejo, focada em:

- 📊 **Análise de Vendas**: Métricas detalhadas e tendências
- 🎯 **Segmentação de Clientes**: Entendimento profundo do perfil de consumo
- 💹 **Performance de Produtos**: Análise completa do portfólio
- ♻️ **Sustentabilidade**: Métricas ESG e impacto ambiental

Navegue pelas diferentes seções usando o menu lateral para explorar análises específicas.
""")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Developed by Giovano M Panatta | v1.0.0</small>
</div>
""", unsafe_allow_html=True)