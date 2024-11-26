from crewai.tools import BaseTool
from supabase import create_client
import json

class DatabaseAnalysisTool(BaseTool):
    name = "database_analysis"
    description = "Ferramenta para análise completa dos dados de vendas, incluindo categorias, padrões temporais e clientes"

    def __init__(self, supabase_url: str, supabase_key: str):
        super().__init__()
        self._supabase = create_client(supabase_url, supabase_key)

    def _run(self, tool_input: str = "") -> str:
        try:
            # 1. Análise de Vendas por Categoria
            vendas_categoria = self._supabase.rpc(
                'analyze_categories',
                params={}
            ).execute()

            # 2. Análise Temporal
            analise_temporal = self._supabase.rpc(
                'analyze_temporal_patterns',
                params={}
            ).execute()

            # 3. Análise de Clientes
            analise_clientes = self._supabase.rpc(
                'analyze_customers',
                params={}
            ).execute()

            # Formatando o resultado
            analise = {
                "categorias": vendas_categoria.data,
                "temporal": analise_temporal.data,
                "clientes": analise_clientes.data
            }

            return json.dumps(analise, indent=2)

        except Exception as e:
            return f"Erro na análise: {str(e)}"

    async def _arun(self, tool_input: str = "") -> str:
        # Implementação assíncrona (opcional)
        raise NotImplementedError("Async não implementado")
