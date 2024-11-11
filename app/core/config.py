from pydantic import BaseModel
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Configurações do Banco de Dados
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RetailSense AI"
    DESCRIPTION: str = "API para análise de varejo com foco em ESG"
    VERSION: str = "1.0.0"
    
    # Caminhos dos modelos
    SCALER_PATH: str = "models/scaler.joblib"
    MODEL_INFO_PATH: str = "models/model_info.joblib"
    
    class Config:
        arbitrary_types_allowed = True
        extra = "allow"  # Permite campos extras

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()