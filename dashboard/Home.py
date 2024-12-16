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

# Card de Introdução
st.markdown("""
<div class="card">
    <div class="icon">💡</div>
    <h3 class="feature-title">Bem-vindo ao RetailSense</h3>
    <p class="feature-text">
        A RetailSense oferece soluções integradas de análise de dados para otimização 
        de operações no varejo. Nossa plataforma transforma dados em insights acionáveis 
        através de tecnologias avançadas e inteligência artificial.
    </p>
</div>
""", unsafe_allow_html=True)

# Páginas Disponíveis
st.markdown("""
<div class="card">
    <h3 class="feature-title">📱 Páginas Disponíveis</h3>
    <ul>
        <li><span class="highlight">1. Converse com os seus Dados</span>
            <ul>
                <li>Interface conversacional para análise de dados</li>
                <li>Possibilidade de foco em análises específicas de ESG no varejo</li>
            </ul>
        </li>
        <li><span class="highlight">2. Gere Relatórios Automaticamente</span>
            <ul>
                <li>Geração automatizada de relatórios personalizados</li>
            </ul>
        </li>
        <li><span class="highlight">3. Análise de Clientes e Segmentação</span></li>
        <li><span class="highlight">4. Análise de Produtos</span></li>
        <li><span class="highlight">5. Análise Geográfica</span></li>
        <li><span class="highlight">6. Análise Temporal de Vendas</span></li>
        <li><span class="highlight">7. Download de Dados</span></li>
        <li><span class="highlight">8. Exemplo de LLM com uso local</span>
            <ul>
                <li>Demonstração de códigos e implementação</li>
            </ul>
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Sobre os Dados
st.markdown("""
<div class="card">
    <div class="icon">📊</div>
    <h3 class="feature-title">Sobre os Dados</h3>
    <p class="feature-text">
        O conjunto de dados utilizado provém de uma empresa de varejo online do Reino Unido, 
        especializada em presentes únicos. Os dados abrangem transações entre 01/12/2010 e 09/12/2011.
    </p>
    <ul>
        <li>541.909 registros de transações</li>
        <li>6 características principais</li>
        <li>Dados multivariados com séries temporais</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="card" style="text-align: center; margin-top: 2em;">
    <p style="color: #87CEEB;">RetailSense © 2024 - Transformando Dados em Resultados</p>
</div>
""", unsafe_allow_html=True)
