# utils/api.py
import requests
import pandas as pd
from typing import Dict, Any
from config.settings import Settings

class APIClient:
    """Cliente para comunicação com a API"""
    
    def __init__(self):
        """Inicializa o cliente API com as configurações"""
        self.settings = Settings()
    
    def get_vendas_pais(self) -> Dict[str, Any]:
        """
        Obtém dados de vendas por país (retorna JSON bruto)
        Returns: Dict com dados de vendas por país
        """
        response = requests.get(self.settings.ENDPOINT_VENDAS_PAIS)
        return response.json()
    
    def get_vendas_por_pais(self) -> pd.DataFrame:
        """
        Obtém dados de vendas por país e converte para DataFrame
        Returns: DataFrame com dados de vendas por país
        """
        try:
            response = requests.get(self.settings.ENDPOINT_VENDAS_PAIS)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data['data'])
            else:
                raise Exception(f"Erro na API: {response.status_code}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição: {str(e)}")
    
    def get_analise_temporal(self, data_inicio: str = None, data_fim: str = None) -> Dict[str, Any]:
        """
        Obtém dados de análise temporal com filtro de datas
        Args:
            data_inicio: Data inicial no formato YYYY-MM-DD
            data_fim: Data final no formato YYYY-MM-DD
        Returns: Dict com dados de análise temporal
        """
        params = {}
        if data_inicio:
            params['data_inicio'] = data_inicio
        if data_fim:
            params['data_fim'] = data_fim
            
        response = requests.get(
            self.settings.ENDPOINT_TEMPORAL,
            params=params
        )
        return response.json()
    
    def get_analise_produtos(self) -> Dict[str, Any]:
        """
        Obtém dados de análise de produtos
        Returns: Dict com dados de análise de produtos
        """
        response = requests.get(self.settings.ENDPOINT_PRODUTOS)
        return response.json()
    
    def get_analise_clientes(self) -> Dict[str, Any]:
        """
        Obtém dados de análise de clientes
        Returns: Dict com dados de análise de clientes
        """
        response = requests.get(self.settings.ENDPOINT_CLIENTES)
        return response.json()
    
    def get_analise_faturamento(self) -> Dict[str, Any]:
        """
        Obtém dados de análise de faturamento
        Returns: Dict com dados de análise de faturamento
        """
        response = requests.get(self.settings.ENDPOINT_FATURAMENTO)
        return response.json()

    


# Exemplo de uso:
# client = APIClient()
# dados_vendas = client.get_vendas_pais()
