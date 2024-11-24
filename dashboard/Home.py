import streamlit as st
import plotly.express as px
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="RetailSense | Varejo Inteligente e ESG",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal com logo e nome da empresa
st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <h1>🏪 RetailSense</h1>
        <h3>Varejo Inteligente e ESG</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Mensagem de boas-vindas e descrição
st.markdown("""
    ### 👋 Bem-vindo à RetailSense
    
    Somos especialistas em transformar dados em insights acionáveis para o varejo, 
    combinando análise avançada com práticas ESG para um crescimento sustentável.
""")

# Cards das principais funcionalidades
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    ### 📈 Análise Temporal
    Acompanhe tendências de vendas, sazonalidade e evolução do ticket médio ao longo do tempo.
    """)

with col2:
    st.markdown("""
    ### 🌎 Análise Geográfica
    Visualize o desempenho de vendas por região e identifique oportunidades de expansão.
    """)

with col3:
    st.markdown("""
    ### 📦 Análise de Produtos
    Monitore o desempenho do portfólio e identifique produtos com maior potencial.
    """)

with col4:
    st.markdown("""
    ### 📊 Gestão de Dados
    Acesse, baixe e analise dados históricos de forma simples e intuitiva.
    """)

st.markdown("---")

# Seção de ESG
st.markdown("""
## 🌱 Nossa Abordagem ESG

A RetailSense integra Inteligência Artificial com práticas ESG para criar um varejo mais sustentável:

- **Environmental** 🌿
  - Monitoramento de indicadores ambientais
  - Otimização de recursos e redução de desperdício
  
- **Social** 👥
  - Análise de impacto social das operações
  - Desenvolvimento de comunidades locais
  
- **Governance** ⚖️
  - Transparência nas operações
  - Tomada de decisão baseada em dados
""")

# Seção de Navegação Rápida
st.markdown("## 🚀 Navegação Rápida")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Análises Principais
    - [📈 Análise Temporal de Vendas](/Análise_Temporal)
    - [🌎 Análise Geográfica](/Análise_Geográfica)
    - [📦 Análise de Produtos](/Análise_Produtos)
    """)

with col2:
    st.markdown("""
    ### Recursos Adicionais
    - [📥 Download de Dados](/Download_Dados)
    - [📚 Documentação](/Documentação)
    - [❓ Suporte](mailto:suporte@retailsense.com)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 1rem;'>
    <p>RetailSense © 2024 - Transformando dados em resultados sustentáveis</p>
</div>
""", unsafe_allow_html=True)
