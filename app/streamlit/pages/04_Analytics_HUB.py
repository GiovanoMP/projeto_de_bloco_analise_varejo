import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import requests
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional
from services.currency_service import CurrencyService
from core.database import get_db

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="RetailSense AI - Analytics Hub",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AnalyticsHub:
    def __init__(self):
        self.api_base_url = "http://localhost:8000/api/v1/analytics"
        self.currency_service = CurrencyService()
        self.openai_key = st.secrets["OPENAI_API_KEY"]
        
        # Inicializar LangChain
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=self.openai_key
        )
        
        # Template para análise
        self.analysis_prompt = ChatPromptTemplate.from_template("""
            Você é um especialista em análise de dados de varejo e negócios.
            Analise a seguinte pergunta e os dados disponíveis para fornecer insights valiosos:

            Pergunta do usuário: {question}

            Dados disponíveis:
            - Vendas: {sales_data}
            - Clientes: {customer_data}
            - Produtos: {product_data}
            - Taxa de Câmbio: {exchange_data}
            - Clima: {weather_data}
            - Tendências: {trends_data}

            Contexto adicional:
            - Período: {date_range}
            - Local: {location}
            - Segmento: {segment}

            Formate sua resposta de forma clara e estruturada, incluindo:
            1. Análise principal
            2. Métricas relevantes
            3. Recomendações práticas
            4. Possíveis riscos ou considerações
            
            Seja conciso mas informativo.
        """)
        
        self.chain = self.analysis_prompt | self.llm | StrOutputParser()
    
    @st.cache_data(ttl=3600)
    def get_all_data(self) -> Dict:
        """Obtém dados de todas as fontes"""
        try:
            data = {
                'sales': self._get_api_data('sales'),
                'customers': self._get_api_data('customers'),
                'products': self._get_api_data('products'),
                'exchange': self.currency_service.get_exchange_rates(),
                'weather': self._get_weather_data(),
                'trends': self._get_trends_data()
            }
            return data
        except Exception as e:
            logger.error(f"Erro ao obter dados: {str(e)}")
            return {}
    
    def process_query(self, question: str, context: Dict) -> str:
        """Processa pergunta do usuário e retorna análise"""
        try:
            response = self.chain.invoke({
                "question": question,
                "sales_data": context.get('sales', {}),
                "customer_data": context.get('customers', {}),
                "product_data": context.get('products', {}),
                "exchange_data": context.get('exchange', {}),
                "weather_data": context.get('weather', {}),
                "trends_data": context.get('trends', {}),
                "date_range": context.get('date_range', ''),
                "location": context.get('location', ''),
                "segment": context.get('segment', '')
            })
            return response
        except Exception as e:
            logger.error(f"Erro ao processar query: {str(e)}")
            return f"Erro ao processar sua pergunta: {str(e)}"
    
    def _get_api_data(self, endpoint: str) -> Dict:
        """Obtém dados da API interna"""
        try:
            response = requests.get(
                f"{self.api_base_url}/{endpoint}",
                timeout=10
            )
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            logger.error(f"Erro ao obter dados da API {endpoint}: {str(e)}")
            return {}
    
    def _get_weather_data(self) -> Dict:
        """Obtém dados climáticos"""
        # Implementar integração com OpenWeather API
        pass
    
    def _get_trends_data(self) -> Dict:
        """Obtém dados de tendências"""
        # Implementar integração com Google Trends
        pass

def main():
    # Inicializar Analytics Hub
    hub = AnalyticsHub()
    
    # Interface do usuário
    st.title("🤖 Analytics Hub")
    st.markdown("""
        Seu assistente inteligente para análise de dados de varejo. 
        Faça perguntas e obtenha insights valiosos baseados em dados em tempo real.
    """)
    
    # Sidebar com configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Filtros de contexto
        st.subheader("🎯 Contexto da Análise")
        
        date_range = st.date_input(
            "Período de Análise",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )
        
        location = st.multiselect(
            "Localização",
            options=["Reino Unido", "França", "Alemanha", "Portugal", "Outros"],
            default=["Reino Unido"]
        )
        
        segment = st.selectbox(
            "Segmento de Clientes",
            options=["Todos", "Champions", "Leais", "Em Risco", "Perdidos"]
        )
        
        st.markdown("---")
        
        # Fontes de dados
        st.subheader("📊 Fontes de Dados")
        st.write("Atualmente utilizando:")
        st.write("✅ Dados internos de vendas")
        st.write("✅ Taxas de câmbio")
        st.write("✅ Dados climáticos")
        st.write("✅ Tendências de mercado")
        
        st.markdown("---")
        
        # Informações do modelo
        st.subheader("🤖 Modelo")
        st.write("GPT-4 + Agentes especializados")
        st.write("Última atualização: " + datetime.now().strftime("%d/%m/%Y %H:%M"))
    
    # Área principal
    tab1, tab2 = st.tabs(["💬 Chat", "📈 Visualizações"])
    
    with tab1:
        # Inicializar histórico do chat se não existir
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Exibir mensagens anteriores
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Faça sua pergunta sobre os dados..."):
            # Adicionar pergunta ao histórico
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Exibir pergunta
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Processar resposta
            with st.chat_message("assistant"):
                with st.spinner("Analisando dados..."):
                    # Obter dados atualizados
                    data = hub.get_all_data()
                    
                    # Adicionar contexto
                    context = {
                        'date_range': date_range,
                        'location': location,
                        'segment': segment,
                        **data
                    }
                    
                    # Processar resposta
                    response = hub.process_query(prompt, context)
                    
                    # Exibir resposta
                    st.markdown(response)
                    
                    # Adicionar resposta ao histórico
                    st.session_state.messages.append({"role": "assistant", "content": response})
    
    with tab2:
        # Área para visualizações dinâmicas baseadas no contexto
        st.subheader("📊 Visualizações Relevantes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exemplo de visualização de vendas
            st.markdown("### 💰 Vendas por País")
            # Adicionar gráfico aqui
        
        with col2:
            # Exemplo de visualização de clientes
            st.markdown("### 👥 Distribuição de Clientes")
            # Adicionar gráfico aqui
        
        # Insights em tempo real
        st.markdown("### 💡 Insights em Tempo Real")
        
        # Métricas de exemplo
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Vendas Hoje",
                value="£ 12,345",
                delta="23%"
            )
        
        with col2:
            st.metric(
                label="Novos Clientes",
                value="48",
                delta="-12%"
            )
        
        with col3:
            st.metric(
                label="Satisfação",
                value="94%",
                delta="7%"
            )

if __name__ == "__main__":
    main()