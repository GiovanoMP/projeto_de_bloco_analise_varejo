import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import requests
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

class SerperAPI:
    def __init__(self):
        self.api_key = os.getenv('SERPER_API_KEY')
        self.base_url = "https://google.serper.dev/search"
        
    def search_esg_insights(self, industry_context):
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        query = f"latest ESG trends retail industry {industry_context} 2024"
        payload = {
            'q': query,
            'num': 3
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            results = response.json()
            return [{'title': r.get('title', '')} 
                   for r in results.get('organic', [])[:3]]
        except Exception as e:
            st.error(f"Erro na busca ESG: {str(e)}")
            return []

class RetailAPI:
    def __init__(self):
        self.base_url = "https://render-api-rvd7.onrender.com/api/v1/analise"
        
    def get_endpoint_data(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'success':
                if endpoint == '/vendas-por-pais':
                    return sorted(
                        data.get('data', []),
                        key=lambda x: x.get('total_vendas', 0),
                        reverse=True
                    )[:5]
                    
                elif endpoint == '/produtos':
                    return sorted(
                        data.get('data', []),
                        key=lambda x: x.get('valor_total', 0),
                        reverse=True
                    )[:5]
                    
                elif endpoint == '/clientes':
                    return [c for c in data.get('top_clientes', [])[:5]
                           if c.get('id_cliente') != 'Desconhecido']
                    
                elif endpoint == '/faturamento':
                    return {
                        'media_diaria': data.get('media_diaria'),
                        'crescimento': data.get('crescimento_mes_anterior')
                    }
            return []
        except Exception as e:
            st.error(f"Erro no endpoint {endpoint}: {str(e)}")
            return None
    
    def get_all_data(self):
        data = {}
        endpoints = {
            'vendas': '/vendas-por-pais',
            'produtos': '/produtos',
            'clientes': '/clientes',
            'faturamento': '/faturamento'
        }
        
        for key, endpoint in endpoints.items():
            result = self.get_endpoint_data(endpoint)
            if result:
                data[key] = result
            time.sleep(0.5)
        
        return data

class ReportGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4",
            max_tokens=2000,
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )
        self.api = RetailAPI()
        self.serper = SerperAPI()
        
        self.template_report = """
        Analise os dados de varejo de {month}/2011 e forneça um relatório executivo conciso.

        DADOS:
        {data}

        ESG INSIGHTS:
        {esg_insights}

        FOCO: {report_type}

        Estruture o relatório da seguinte forma:

        1. RESUMO EXECUTIVO
        - Principais indicadores
        - Pontos críticos

        2. ANÁLISE FOCAL ({report_type})
        - Insights principais
        - Tendências identificadas

        3. RECOMENDAÇÕES
        - 3 ações prioritárias
        - Próximos passos

        Seja direto e objetivo, focando nos pontos mais relevantes.
        """
        
        self.prompt = PromptTemplate(
            input_variables=["data", "esg_insights", "report_type", "month"],
            template=self.template_report
        )

    def generate_report(self, report_type, month):
        try:
            with st.spinner("Coletando dados..."):
                data = self.api.get_all_data()
                
                # Simplificar dados
                simplified_data = {
                    'vendas': [{'pais': x['pais'], 'total': x['total_vendas']} 
                              for x in data.get('vendas', [])],
                    'produtos': [{'nome': x['nome'], 'valor': x['valor_total']} 
                                for x in data.get('produtos', [])],
                    'clientes': [{'id': x['id_cliente'], 'total': x['total_compras']} 
                                for x in data.get('clientes', [])],
                    'faturamento': data.get('faturamento', {})
                }
            
            with st.spinner("Buscando insights ESG..."):
                esg_insights = self.serper.search_esg_insights(report_type)
            
            with st.spinner("Gerando relatório..."):
                with get_openai_callback() as cb:
                    chain = LLMChain(llm=self.llm, prompt=self.prompt)
                    report = chain.run(
                        data=json.dumps(simplified_data, ensure_ascii=False),
                        esg_insights=json.dumps(esg_insights, ensure_ascii=False),
                        report_type=report_type,
                        month=month
                    )
                    st.write(f"Tokens utilizados: {cb.total_tokens}")
            
            return report
        except Exception as e:
            raise Exception(f"Erro na geração: {str(e)}")

def main():
    st.set_page_config(
        page_title="Análise de Varejo",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Análise Estratégica de Varejo")
    
    if 'report_generator' not in st.session_state:
        st.session_state.report_generator = ReportGenerator()
    
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Tipo de Análise:",
            ["Geral", 
             "Mercado",
             "Produtos",
             "Clientes",
             "Financeiro",
             "ESG"]
        )
    
    with col2:
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                 "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        mes = st.selectbox("Mês:", meses, index=0)
        mes_numero = meses.index(mes) + 1
    
    if st.button("📝 Gerar Relatório"):
        try:
            with st.spinner("Gerando análise..."):
                report = st.session_state.report_generator.generate_report(
                    report_type=report_type,
                    month=mes_numero
                )
                
                st.success("✅ Relatório Gerado!")
                st.markdown(report)
                
                st.download_button(
                    "📥 Download Relatório",
                    report,
                    file_name=f"relatorio_{mes.lower()}_2011.txt",
                    mime="text/plain"
                )
        
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    main()
