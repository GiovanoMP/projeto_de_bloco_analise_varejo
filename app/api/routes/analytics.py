from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List
import logging

from ...core.database import get_db
from ...models.schemas import SalesMetrics, ProductAnalytics, CustomerMetrics
from ...services.analytics_service import get_sales_metrics, get_product_analytics, get_customer_metrics

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/sales", response_model=SalesMetrics)
def get_sales_analysis(
    start_date: date = Query(..., description="Data inicial da análise"),
    end_date: date = Query(..., description="Data final da análise"),
    db: Session = Depends(get_db)
):
    """
    Retorna métricas de vendas para o período especificado
    """
    try:
        logger.debug(f"Recebida requisição de análise de vendas: {start_date} até {end_date}")
        result = get_sales_metrics(db, start_date, end_date)
        logger.debug(f"Resultado da análise: {result}")
        return result
    except Exception as e:
        logger.error(f"Erro ao processar análise de vendas: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products", response_model=List[ProductAnalytics])
def get_product_analysis(
    limit: int = Query(10, description="Número de produtos a retornar"),
    db: Session = Depends(get_db)
):
    """
    Retorna análise dos produtos mais vendidos
    """
    try:
        return get_product_analytics(db, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customers", response_model=CustomerMetrics)
def get_customer_analysis(db: Session = Depends(get_db)):
    """
    Retorna métricas relacionadas aos clientes
    """
    try:
        return get_customer_metrics(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))