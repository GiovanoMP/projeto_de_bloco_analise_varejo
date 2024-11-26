from crewai import Task
from textwrap import dedent

class AnalysisTasks:
    def analyze_retail_data(self, agent):
        return Task(
            description=dedent("""
            Analise detalhadamente os dados de vendas do varejo e forneça um relatório completo seguindo estas etapas:

            1. VISÃO GERAL DO DESEMPENHO:
               - Análise de vendas totais e por categoria
               - Identificação das categorias mais e menos performantes
               - Análise de tendências temporais relevantes

            2. ANÁLISE PROFUNDA:
               - Comportamento de vendas por categoria e subcategoria
               - Análise de margens e rentabilidade
               - Identificação de padrões sazonais
               - Correlações importantes entre categorias

            3. OPORTUNIDADES E RISCOS:
               - Identificar categorias com potencial de crescimento
               - Apontar pontos de atenção e riscos
               - Análise de gaps de performance

            4. RECOMENDAÇÕES ESTRATÉGICAS:
               - Sugestões específicas para cada categoria
               - Estratégias de mix de produtos
               - Recomendações de pricing quando aplicável
               - Ações práticas para implementação imediata

            Requisitos específicos:
            - Use dados concretos e números para suportar suas análises
            - Formate sua resposta de maneira clara e estruturada
            - Priorize insights acionáveis
            - Inclua visualizações ou tabelas quando relevante
            
            Seu relatório deve ser completo mas direto, focando em informações 
            que podem gerar valor real para o negócio.
            """),
            agent=agent
        )
