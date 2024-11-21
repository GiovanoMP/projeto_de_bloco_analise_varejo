# app/api/api_service.py
import requests
from datetime import date
from typing import Dict, List, Any
from ..frontend.utils.config import API_BASE_URL

class RetailAPI:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url

    def get_summary(self, data_inicio: date = date(2011, 1, 4), 
                   data_fim: date = date(2011, 12, 31)) -> Dict:
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        response = requests.get(f"{self.base_url}/transactions/summary", params=params)
        return response.json()

    def get_categories_summary(self, data_inicio: date = date(2011, 1, 4), 
                             data_fim: date = date(2011, 12, 31)) -> List:
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        response = requests.get(f"{self.base_url}/transactions/by-category", params=params)
        return response.json()

    def get_countries_summary(self, data_inicio: date = date(2011, 1, 4), 
                            data_fim: date = date(2011, 12, 31)) -> List:
        params = {
            "data_inicio": data_inicio.isoformat(),
            "data_fim": data_fim.isoformat()
        }
        response = requests.get(f"{self.base_url}/transactions/by-country", params=params)
        return response.json()
