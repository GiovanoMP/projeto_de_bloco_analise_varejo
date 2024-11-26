from typing import Any
from supabase import create_client
import pandas as pd
from langchain.tools import BaseTool

class DatabaseAnalysisTool(BaseTool):
    name = "database_analysis"
    description = """
    Ferramenta para análise completa dos dados de transações de varejo.
    Use esta ferramenta quando precisar analisar os dados da tabela 'transactions_sample'.
    Fornece análises detalhadas sobre vendas, produtos, clientes e padrões temporais.
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        super().__init__()
        self.supabase = create_client(supabase_url, supabase_key)

    def _agg_query(self):
        return """
        SELECT 
            -- Métricas Gerais
            COUNT(*) as total_transactions,
            COUNT(DISTINCT "NumeroFatura") as total_invoices,
            COUNT(DISTINCT "CodigoProduto") as total_products,
            COUNT(DISTINCT "IDCliente") as total_customers,
            COUNT(DISTINCT "Pais") as total_countries,
            
            -- Métricas de Valor
            ROUND(SUM("ValorTotalFatura")::numeric, 2) as total_revenue,
            ROUND(AVG("ValorTotalFatura")::numeric, 2) as avg_invoice_value,
            ROUND(MIN("PrecoUnitario")::numeric, 2) as min_unit_price,
            ROUND(MAX("PrecoUnitario")::numeric, 2) as max_unit_price,
            ROUND(AVG("PrecoUnitario")::numeric, 2) as avg_unit_price,
            
            -- Métricas de Quantidade
            SUM("Quantidade") as total_quantity,
            ROUND(AVG("Quantidade")::numeric, 2) as avg_quantity_per_transaction
        FROM transactions_sample
        """

    def _category_analysis_query(self):
        return """
        SELECT 
            "CategoriaProduto",
            COUNT(*) as total_sales,
            ROUND(SUM("ValorTotalFatura")::numeric, 2) as total_revenue,
            COUNT(DISTINCT "IDCliente") as unique_customers
        FROM transactions_sample
        GROUP BY "CategoriaProduto"
        ORDER BY total_revenue DESC
        """

    def _price_category_query(self):
        return """
        SELECT 
            "CategoriaPreco",
            COUNT(*) as total_sales,
            ROUND(AVG("PrecoUnitario")::numeric, 2) as avg_price,
            ROUND(SUM("ValorTotalFatura")::numeric, 2) as total_revenue
        FROM transactions_sample
        GROUP BY "CategoriaPreco"
        ORDER BY avg_price DESC
        """

    def _temporal_patterns_query(self):
        return """
        SELECT 
            "DiaSemana",
            COUNT(*) as total_transactions,
            ROUND(AVG("ValorTotalFatura")::numeric, 2) as avg_daily_revenue
        FROM transactions_sample
        GROUP BY "DiaSemana"
        ORDER BY "DiaSemana"
        """

    def _run(self, query: str = None) -> str:
        try:
            # Estatísticas gerais
            agg_result = self.supabase.query(self._agg_query()).execute()
            stats = agg_result.data[0]

            # Análise por categoria de produto
            cat_result = self.supabase.query(self._category_analysis_query()).execute()
            cat_stats = cat_result.data

            # Análise por categoria de preço
            price_result = self.supabase.query(self._price_category_query()).execute()
            price_stats = price_result.data

            # Padrões temporais
            temporal_result = self.supabase.query(self._temporal_patterns_query()).execute()
            temporal_stats = temporal_result.data

            analysis = f"""
            ANÁLISE DETALHADA DAS TRANSAÇÕES DE VAREJO

            1. VISÃO GERAL
            - Total de transações: {stats['total_transactions']:,}
            - Total de faturas únicas: {stats['total_invoices']:,}
            - Total de produtos distintos: {stats['total_products']:,}
            - Base de clientes: {stats['total_customers']:,}
            - Países atendidos: {stats['total_countries']}

            2. MÉTRICAS FINANCEIRAS
            - Faturamento total: R$ {stats['total_revenue']:,.2f}
            - Valor médio por fatura: R$ {stats['avg_invoice_value']:,.2f}
            - Preço unitário:
              * Médio: R$ {stats['avg_unit_price']:,.2f}
              * Mínimo: R$ {stats['min_unit_price']:,.2f}
              * Máximo: R$ {stats['max_unit_price']:,.2f}

            3. MÉTRICAS DE VOLUME
            - Quantidade total vendida: {stats['total_quantity']:,}
            - Quantidade média por transação: {stats['avg_quantity_per_transaction']:,.1f}

            4. ANÁLISE POR CATEGORIA DE PRODUTO
            Top 3 categorias por receita:"""

            for cat in cat_stats[:3]:
                analysis += f"""
            - {cat['CategoriaProduto']}:
              * Receita: R$ {cat['total_revenue']:,.2f}
              * Vendas: {cat['total_sales']:,}
              * Clientes únicos: {cat['unique_customers']:,}"""

            analysis += "\n\n5. ANÁLISE POR CATEGORIA DE PREÇO"
            for price_cat in price_stats:
                analysis += f"""
            - {price_cat['CategoriaPreco']}:
              * Preço médio: R$ {price_cat['avg_price']:,.2f}
              * Receita total: R$ {price_cat['total_revenue']:,.2f}
              * Total de vendas: {price_cat['total_sales']:,}"""

            analysis += "\n\n6. PADRÕES TEMPORAIS"
            dias_semana = {
                0: 'Segunda', 1: 'Terça', 2: 'Quarta', 
                3: 'Quinta', 4: 'Sexta', 5: 'Sábado', 6: 'Domingo'
            }
            for temp in temporal_stats:
                analysis += f"""
            - {dias_semana[temp['DiaSemana']]}:
              * Transações: {temp['total_transactions']:,}
              * Receita média: R$ {temp['avg_daily_revenue']:,.2f}"""

            return analysis

        except Exception as e:
            return f"Erro ao analisar os dados: {str(e)}"

    def _arun(self, query: str = None) -> Any:
        raise NotImplementedError("Esta ferramenta não suporta execução assíncrona.")
