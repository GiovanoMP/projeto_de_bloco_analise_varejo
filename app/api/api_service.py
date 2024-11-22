# app/api/api_service.py
import requests
from datetime import date
from typing import Dict, List, Any, Optional
from ..frontend.utils.config import API_BASE_URL
from requests.exceptions import RequestException, ConnectionError, Timeout

class RetailAPI:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if exists
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'
        }
        self.timeout = 30  # timeout em segundos

    def _handle_response(self, response: requests.Response) -> Dict:
        """Trata as respostas da API e possíveis erros"""
        try:
            response.encoding = 'utf-8'
            response.raise_for_status()
            return response.json()
        except ConnectionError:
            return {"error": "Erro de conexão com a API. Verifique se o servidor está online."}
        except Timeout:
            return {"error": "Timeout na requisição. Tente novamente."}
        except RequestException as e:
            return {"error": f"Erro na requisição: {str(e)}"}
        except ValueError as e:  # Erro no parsing do JSON
            return {"error": f"Erro ao processar resposta da API: {str(e)}"}

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Método centralizado para fazer requisições"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            return self._handle_response(response)
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}

    def get_transactions(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        pais: Optional[str] = None, 
        categoria: Optional[str] = None,
        data_inicio: date = date(2011, 1, 4),
        data_fim: date = date(2011, 12, 31)
    ) -> List:
        """Obtém lista de transações com filtros"""
        params = {
            "skip": skip,
            "limit": limit,
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        if pais:
            params["pais"] = pais.strip()
        if categoria:
            params["categoria"] = categoria.strip()

        return self._make_request("/transactions/", params)

    def get_summary(
        self, 
        data_inicio: date = date(2011, 1, 4),
        data_fim: date = date(2011, 12, 31)
    ) -> Dict:
        """Obtém o resumo das transações no período especificado"""
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        return self._make_request("/transactions/summary", params)

    def get_categories_summary(
        self, 
        data_inicio: date = date(2011, 1, 4),
        data_fim: date = date(2011, 12, 31)
    ) -> List:
        """Obtém o resumo por categorias no período especificado"""
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        return self._make_request("/transactions/by-category", params)

    def get_countries_summary(
        self, 
        data_inicio: date = date(2011, 1, 4),
        data_fim: date = date(2011, 12, 31)
    ) -> List:
        """Obtém o resumo por países no período especificado"""
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        return self._make_request("/transactions/by-country", params)
