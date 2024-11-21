# pages/6_Insights_com_IA.py

import streamlit as st
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import plotly.express as px
from supabase import create_client
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

# Configuração inicial da página
st.set_page_config(
    page_title="AI Insights - ESG & Retail Analytics",
    page_icon="🤖",
    layout="wide"
)

# Configurações e constantes
ML_INSIGHTS = """=== ANÁLISE DETALHADA DE SEGMENTAÇÃO DE CLIENTES E PADRÕES DE COMPRA ===
[... seu texto completo de ML insights aqui ...]
"""

def get_supabase_client():
    """Inicializa o cliente Supabase"""
    try:
        return create_client(
            st.secrets["supabase"]["url"],
            st.secrets["supabase"]["key"]
        )
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {str(e)}")
        return None

def init_session_state():
    """Inicializa variáveis da sessão"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'cached_data' not in st.session_state:
        st.session_state.cached_data = None
    if 'last_data_fetch' not in st.session_state:
        st.session_state.last_data_fetch = None

def execute_sql_analysis(query_type: str) -> str:
    supabase = get_supabase_client()
    
    queries = {
        "analise_categorias": """
            SELECT 
                "CategoriaProduto",
                "CategoriaPreco",
                COUNT(*) as total_vendas,
                SUM("ValorTotalFatura") as valor_total,
                AVG("PrecoUnitario") as preco_medio,
                COUNT(DISTINCT "IDCliente") as num_clientes_unicos
            FROM transactions_sample
            GROUP BY "CategoriaProduto", "CategoriaPreco"
            ORDER BY valor_total DESC;
        """,
        
        "analise_geografica": """
            SELECT 
                "Pais",
                COUNT(DISTINCT "IDCliente") as num_clientes,
                COUNT(*) as total_transacoes,
                SUM("ValorTotalFatura") as valor_total,
                AVG("ValorTotalFatura") as ticket_medio,
                COUNT(DISTINCT "NumeroFatura") as num_faturas
            FROM transactions_sample
            GROUP BY "Pais"
            ORDER BY valor_total DESC;
        """,
        
        # ... (outras queries permanecem as mesmas)
    }
    
    try:
        if query_type in queries:
            response = supabase.query(queries[query_type]).execute()
            return json.dumps(response.data, default=str)
        return "Tipo de análise não reconhecido"
    except Exception as e:
        return f"Erro na análise SQL: {str(e)}"

def create_visualization(data_type: str, data: str) -> str:
    try:
        df = pd.read_json(data)
        
        if data_type == "geografico":
            fig = px.choropleth(
                df,
                locations="Pais",
                locationmode="country names",
                color="valor_total",
                hover_data=["num_clientes", "total_transacoes", "ticket_medio"],
                title="Análise Geográfica de Vendas"
            )
        
        elif data_type == "temporal":
            df['data'] = pd.to_datetime(df.apply(lambda x: f"{x['Ano']}-{x['Mes']}-01", axis=1))
            fig = px.line(
                df,
                x="data",
                y="valor_total",
                title="Evolução Temporal das Vendas"
            )
        
        elif data_type == "categorias":
            fig = px.treemap(
                df,
                path=["CategoriaProduto", "CategoriaPreco"],
                values="valor_total",
                title="Distribuição de Vendas por Categoria"
            )
        
        else:
            return "Tipo de visualização não suportado"
        
        return fig.to_json()
    
    except Exception as e:
        return f"Erro na criação da visualização: {str(e)}"

def setup_langchain_agent():
    """Configura o agente LangChain"""
    llm = ChatOpenAI(temperature=0, model="gpt-4-1106-preview")
    
    tools = [
        Tool(
            name="SQLAnalyzer",
            func=execute_sql_analysis,
            description="Executa análises SQL pré-definidas nos dados de transações"
        ),
        Tool(
            name="DataVisualizer",
            func=create_visualization,
            description="Cria visualizações a partir dos dados analisados"
        )
    ]
    
    prompt = PromptTemplate.from_template(
        """Você é um analista de dados especializado em varejo.
        Use as ferramentas disponíveis para analisar os dados e fornecer insights.
        
        Histórico do chat: {chat_history}
        Pergunta do usuário: {input}
        
        Pense passo a passo:
        1) Que tipo de análise é necessária?
        2) Quais ferramentas usar?
        3) Como interpretar os resultados?
        
        {agent_scratchpad}"""
    )
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def main():
    st.title("🤖 AI Insights - Análise de Dados")
    
    # Inicialização
    init_session_state()
    
    # Sidebar
    st.sidebar.title("Configurações")
    analysis_type = st.sidebar.selectbox(
        "Tipo de Análise",
        ["Visão Geral", "Análise Geográfica", "Análise Temporal", "Análise de Categorias", "Análise de Clientes"]
    )
    
    # Container principal
    main_container = st.container()
    
    with main_container:
        if analysis_type == "Visão Geral":
            st.header("Visão Geral do Negócio")
            
            # Métricas principais
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total de Clientes", "4,196")
            with col2:
                st.metric("Valor Total", "R$ 5.398.574,20")
            with col3:
                st.metric("Ticket Médio", "R$ 342,56")
            
            # Insights do ML
            st.subheader("Insights da Segmentação")
            st.text_area("", ML_INSIGHTS, height=300)
        
        elif analysis_type == "Análise Geográfica":
            st.header("Análise Geográfica")
            result = execute_sql_analysis("analise_geografica")
            
            if result:
                viz_result = create_visualization("geografico", result)
                if viz_result != "Tipo de visualização não suportado":
                    fig = go.Figure(json.loads(viz_result))
                    st.plotly_chart(fig)
    
    # Chat para perguntas
    st.sidebar.markdown("---")
    user_input = st.sidebar.text_input("Faça uma pergunta sobre os dados:")
    
    if user_input:
        agent = setup_langchain_agent()
        with st.spinner("Analisando..."):
            response = agent.run(input=user_input, chat_history=st.session_state.chat_history)
            st.write(response)
            st.session_state.chat_history.append((user_input, response))

if __name__ == "__main__":
    main()
