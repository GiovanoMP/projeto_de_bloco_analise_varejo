from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from ...core.database import get_db, test_connection
from ...core.config import settings
from ...models.schemas import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
def health_check(db: Session = Depends(get_db)):
    """
    Verifica o status da API e conexão com banco de dados
    """
    return HealthCheck(
        status="online",
        timestamp=datetime.now(),
        database_connected=test_connection(),
        version=settings.VERSION
    )