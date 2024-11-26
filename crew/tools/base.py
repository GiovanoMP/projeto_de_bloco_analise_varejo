# tools/base.py
from langchain.tools import BaseTool as LangchainBaseTool

class BaseTool(LangchainBaseTool):
    name: str = "database_analysis"
    description: str = "Ferramenta para análise de dados do banco de dados"
