import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="RetailSense | Home",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS otimizado para tema escuro
st.markdown("""
<style>
    /* Ajustes gerais para tema escuro */
    .main-title {
        color: #00BFFF;  /* Azul brilhante */
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1em;
    }
    .subtitle {
        color: #87CEEB;  /* Azul claro */
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 2em;
    }
    .card {
        background-color: rgba(25, 25, 25, 0.8);  /* Fundo escuro semi-transparente */
        padding: 1.2em;
        border-radius: 10px;
        border: 1px solid #404040;
        margin: 1em 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    .feature-title {
        color: #00BFFF;  /* Azul brilhante */
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 0.8em;
    }
    .feature-text {
        color: #E0E0E0;  /* Texto claro */
    }
    .highlight {
        color: #FFD700;  /* Dourado */
        font-weight: bold;
    }
    /* Ajuste para links */
    a {
        color: #00BFFF !important;
        text-decoration: none;
    }
    a:hover {
        color: #87CEEB !important;
        text-decoration: underline;
    }
    /* Lista com melhor visibilidade */
    ul {
        color: #E0E0E0;
        margin-left: 1.5em;
    }
    li {
        margin: 0.5em 0;
    }
    /* Ícones com melhor contraste */
    .icon {
        font-size: 1.5em;
        color: #00BFFF;
        margin-bottom: 0.5em;
    }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<h1 class="main-title">🏪 RetailSense</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">Soluções em Análise de Dados para Varejo</h2>', unsafe_allow_html=True)

# Introdução em card
st.markdown("""
<div class="card">
    <p class="feature-text">
        A RetailSense oferece soluções integradas de análise de dados e ESG para otimização 
        de operações no varejo. Nossa plataforma transforma dados em insights acionáveis 
        através de três principais vertentes:
    </p>
</div>
""", unsafe_allow_html=True)

# Colunas principais
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div class="icon">📊</div>
        <h3 class="feature-title">Análise de Dados</h3>
        <ul>
            <li>Processamento de dados de vendas</li>
            <li>Análise de métricas fundamentais</li>
            <li>Relatórios automatizados</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="icon">🌱</div>
        <h3 class="feature-title">Métricas ESG</h3>
        <ul>
            <li>Indicadores de sustentabilidade</li>
            <li>Métricas de governança</li>
            <li>Relatórios de impacto social</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="icon">🤖</div>
        <h3 class="feature-title">Agentes IA</h3>
        <ul>
            <li>Análise automatizada</li>
            <li>Processamento inteligente</li>
            <li>Suporte à decisão</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Módulos Disponíveis
st.markdown("""
<div class="card">
    <h3 class="feature-title">📦 Módulos Disponíveis</h3>
    <ul>
        <li><span class="highlight">Análise de Vendas</span>
            <ul>
                <li>Histórico e tendências</li>
                <li>Métricas principais</li>
                <li>Relatórios periódicos</li>
            </ul>
        </li>
        <li><span class="highlight">Dashboard ESG</span>
            <ul>
                <li>Indicadores ambientais</li>
                <li>Métricas sociais</li>
                <li>Governança corporativa</li>
            </ul>
        </li>
        <li><span class="highlight">Visualização de Dados</span>
            <ul>
                <li>Gráficos interativos</li>
                <li>Filtros dinâmicos</li>
                <li>Exportação de relatórios</li>
            </ul>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Seção de Desenvolvimento
st.markdown("""
<div class="card">
    <h3 class="feature-title">🔬 Em Desenvolvimento</h3>
    <ul>
        <li>Expansão das APIs de integração</li>
        <li>Novos módulos de análise</li>
        <li>Recursos avançados de visualização</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="card" style="text-align: center; margin-top: 2em;">
    <p style="color: #87CEEB;">RetailSense © 2024 - Transformando Dados em Resultados</p>
</div>
""", unsafe_allow_html=True)
