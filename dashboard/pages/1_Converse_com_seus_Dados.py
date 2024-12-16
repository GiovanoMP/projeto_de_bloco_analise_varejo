import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

class SerperAPI:
    """Classe para buscar informações ESG usando Serper"""
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.base_url = "https://google.serper.dev/search"
        
    def search_esg_insights(self, industry_context, analysis_type, max_results=5):
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        query_mapping = {
            "Análise de Vendas por País": f"retail ESG initiatives sustainable sales {industry_context}",
            "Análise Temporal": f"retail sustainability trends timeline {industry_context}",
            "Análise de Produtos": f"sustainable retail products initiatives {industry_context}",
            "Análise de Clientes": f"sustainable retail customer engagement {industry_context}",
            "Análise de Faturamento": f"ESG retail financial performance {industry_context}"
        }
        
        query = query_mapping.get(analysis_type, f"retail ESG initiatives {industry_context}")
        payload = {
            'q': query,
            'num': max_results
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            results = response.json()
            return [{'title': r.get('title', ''), 'snippet': r.get('snippet', '')} 
                   for r in results.get('organic', [])[:max_results]]
        except Exception as e:
            print(f"Erro ao buscar insights ESG: {str(e)}")
            return []

class RetailAPI:
    """Classe para gerenciar chamadas à API de dados de varejo"""
    def __init__(self):
        self.base_url = "https://render-api-rvd7.onrender.com/api/v1/analise"
        
    def get_data(self, analysis_type):
        endpoint_mapping = {
            "Análise de Vendas por País": "/vendas-por-pais",
            "Análise Temporal": "/temporal",
            "Análise de Produtos": "/produtos",
            "Análise de Clientes": "/clientes",
            "Análise de Faturamento": "/faturamento"
        }

        try:
            endpoint = endpoint_mapping.get(analysis_type)
            if not endpoint:
                raise ValueError(f"Tipo de análise inválido: {analysis_type}")

            url = f"{self.base_url}{endpoint}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Erro ao obter dados da API: {str(e)}")

class RetailAssistant:
    """Classe principal do assistente de análise de varejo otimizado"""
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.5,
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        self.serper = SerperAPI()
        
        # Atualização do template para lidar melhor com perguntas gerais e específicas
        self.template = """
        Você é um assistente especializado em análise de dados de varejo e sustentabilidade.

        Contexto Atual: {analysis_type}
        Dados Disponíveis: {current_data}
        Insights ESG: {esg_insights}
        Pergunta do Usuário: {human_input}

        Se a pergunta for sobre capacidades gerais, explique suas funcionalidades na área atual:

        Para Análise de Dados:
        - Análise de Vendas por País: análise geográfica, mercados principais, desempenho internacional
        - Análise Temporal: tendências, sazonalidade, períodos de pico
        - Análise de Produtos: performance, produtos principais, oportunidades
        - Análise de Clientes: segmentação, comportamento, perfis
        - Análise de Faturamento: métricas financeiras, receita, crescimento

        Para ESG e Sustentabilidade:
        - Impacto ambiental: pegada de carbono, eficiência energética, resíduos
        - Responsabilidade social: práticas trabalhistas, impacto na comunidade
        - Governança: políticas, compliance, transparência
        - Iniciativas sustentáveis: certificações, práticas verdes
        - Métricas ESG: KPIs, benchmarks, metas

        Para análises específicas, forneça:
        1. Análise Detalhada (usando dados disponíveis)
        2. Insights Principais (tendências e padrões)
        3. Recomendações Práticas (ações específicas)
        4. Considerações ESG (quando relevante)
        5. Próximos Passos (implementação)

        Para qualquer tipo de pergunta:
        - Base suas respostas em dados quando disponíveis
        - Inclua exemplos práticos e específicos
        - Forneça recomendações acionáveis
        - Conecte análises de dados com aspectos ESG quando relevante
        - Mantenha o foco no contexto do varejo
        """
        
        self.prompt = PromptTemplate(
            input_variables=["analysis_type", "current_data", "esg_insights", "human_input"],
            template=self.template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=False
        )

    def get_suggested_questions(self, analysis_type, focus="Geral"):
        if focus == "ESG/Sustentabilidade":
            suggestions = {
                "Análise de Vendas por País": [
                    "Como reduzir a pegada de carbono na logística?",
                    "Quais mercados priorizam sustentabilidade?",
                    "Como alinhar expansão com ESG?"
                ],
                "Análise Temporal": [
                    "Impacto das iniciativas ESG nas vendas?",
                    "Tendências de sustentabilidade?",
                    "Períodos ideais para ações ESG?"
                ],
                "Análise de Produtos": [
                    "Produtos mais sustentáveis?",
                    "Como ser mais eco-friendly?",
                    "Potencial de certificação verde?"
                ],
                "Análise de Clientes": [
                    "Perfil do consumidor sustentável?",
                    "Como aumentar engajamento ESG?",
                    "Demanda por produtos verdes?"
                ],
                "Análise de Faturamento": [
                    "ROI de iniciativas ESG?",
                    "Equilibrar lucro e sustentabilidade?",
                    "Impacto ESG no faturamento?"
                ]
            }
        else:
            suggestions = {
                "Análise de Vendas por País": [
                    "Top 3 países em vendas?",
                    "Mercados em crescimento?",
                    "Oportunidades de expansão?"
                ],
                "Análise Temporal": [
                    "Melhor período de vendas?",
                    "Tendências atuais?",
                    "Padrões sazonais?"
                ],
                "Análise de Produtos": [
                    "Produtos mais rentáveis?",
                    "Itens com baixo desempenho?",
                    "Otimização de portfólio?"
                ],
                "Análise de Clientes": [
                    "Perfil dos melhores clientes?",
                    "Padrões de compra?",
                    "Estratégias de retenção?"
                ],
                "Análise de Faturamento": [
                    "Desempenho atual?",
                    "Tendências de receita?",
                    "Áreas para melhorar?"
                ]
            }
        return suggestions.get(analysis_type, [])

    def analyze(self, query, analysis_type, data):
        try:
            esg_insights = self.serper.search_esg_insights("retail", analysis_type)
            processed_data = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            esg_insights_str = json.dumps(esg_insights, ensure_ascii=False)
            
            with get_openai_callback() as cb:
                response = self.chain.run(
                    human_input=query,
                    analysis_type=analysis_type,
                    current_data=processed_data,
                    esg_insights=esg_insights_str
                )
                st.sidebar.write(f"💰 Tokens: {cb.total_tokens}")
                return response
        except Exception as e:
            return f"Erro na análise: {str(e)}"

def main():
    st.set_page_config(
        page_title="Análise de Dados de Varejo e Sustentabilidade",
        page_icon="🌱",
        layout="wide"
    )
    
    st.title("🌱 Assistente de Análise de Varejo e Sustentabilidade")
    
    if 'api' not in st.session_state:
        st.session_state.api = RetailAPI()
    if 'assistant' not in st.session_state:
        st.session_state.assistant = RetailAssistant()
    
    st.sidebar.title("🔍 Opções de Análise")
    
    analysis_type = st.sidebar.selectbox(
        "Tipo de Análise:",
        ["Análise de Vendas por País", "Análise Temporal", "Análise de Produtos",
         "Análise de Clientes", "Análise de Faturamento"]
    )
    
    esg_focus = st.sidebar.radio(
        "Foco da Análise:",
        ["Geral", "ESG/Sustentabilidade"],
        help="Escolha entre análise geral ou com foco em sustentabilidade"
    )
    
    if 'welcome_shown' not in st.session_state:
        st.write("""
        ### 👋 Bem-vindo ao Assistente de Análise de Varejo e Sustentabilidade!
        
        #### 🎯 Capacidades:
        - Análise de dados de vendas, produtos e clientes
        - Insights de sustentabilidade e ESG
        - Recomendações práticas e acionáveis
        - Integração de métricas de impacto
        
        #### 💡 Dicas:
        - Selecione o tipo de análise desejada
        - Escolha entre foco geral ou ESG
        - Use as sugestões como guia
        Você pode fazer perguntas gerais como "O que você pode analisar?" ou específicas sobre dados e ESG
        """)
        st.session_state.welcome_shown = True
    
    try:
        current_data = st.session_state.api.get_data(analysis_type)
        
        st.write("#### ❓ Perguntas Sugeridas")
        suggestions = st.session_state.assistant.get_suggested_questions(analysis_type, esg_focus)
        
        cols = st.columns(len(suggestions))
        
        for idx, sugestao in enumerate(suggestions):
            if cols[idx].button(sugestao, key=f"sug_{idx}"):
                with st.spinner('Analisando dados...'):
                    response = st.session_state.assistant.analyze(
                        sugestao,
                        analysis_type,
                        current_data
                    )
                    st.write(f"🤖 **Análise Detalhada:**\n{response}")
        
        user_input = st.text_input(
            "💭 Sua pergunta:", 
            placeholder="Faça perguntas gerais ou específicas sobre dados e sustentabilidade..."
        )
        
        if user_input:
            with st.spinner('Processando sua solicitação...'):
                response = st.session_state.assistant.analyze(
                    user_input,
                    analysis_type,
                    current_data
                )
                st.write(f"🤖 **Análise Detalhada:**\n{response}")
    
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        st.error("Por favor, verifique sua conexão e tente novamente.")

if __name__ == "__main__":
    main()