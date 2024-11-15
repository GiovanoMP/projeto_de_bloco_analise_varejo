from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List, Dict
import logging
from sqlalchemy import text

from ...core.database import get_db
from ...models.schemas import SalesMetrics, ProductAnalytics, CustomerMetrics
from ...services.analytics_service import get_sales_metrics, get_product_analytics, get_customer_metrics
from ..errors.handlers import DatabaseError, ValidationError, NotFoundError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analytics")

@router.get("/sales", response_model=SalesMetrics)
async def get_sales_analysis(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db)
):
    try:
        if start_date > end_date:
            raise ValidationError(
                message="Data inicial deve ser anterior à data final",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        supabase_url = st.secrets["supabase"]["url"]
        supabase_key = st.secrets["supabase"]["key"]
        
        # Criar cliente Supabase
        supabase = create_client(supabase_url, supabase_key)
        
        result = await supabase.rpc('get_sales_metrics', {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }).execute()

        return result.data

    except Exception as e:
        logger.error(f"Erro ao processar análise de vendas: {str(e)}")
        raise DatabaseError(message="Erro ao processar análise de vendas", details={"error": str(e)})

@router.get("/sales/temporal")
async def get_sales_temporal(
    start_date: date = Query(..., description="Data inicial da análise"),
    end_date: date = Query(..., description="Data final da análise"),
    window: int = Query(7, description="Janela para média móvel (dias)"),
    db: Session = Depends(get_db)
):
    """Retorna análise temporal de vendas com médias móveis e tendências"""
    try:
        # Criar cliente Supabase
        supabase = create_client(
            st.secrets["supabase"]["url"],
            st.secrets["supabase"]["key"]
        )
        
        # Chamar função do Supabase
        result = await supabase.rpc(
            'get_temporal_metrics',
            {
                'p_start_date': start_date.isoformat(),
                'p_end_date': end_date.isoformat(),
                'p_window': window
            }
        ).execute()
        
        if not result.data:
            raise NotFoundError(
                message="Nenhum dado encontrado para o período especificado",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        return result.data
        
    except Exception as e:
        logger.error(f"Erro ao processar dados temporais: {str(e)}")
        raise DatabaseError(message="Erro ao processar dados temporais", details={"error": str(e)})
@router.get("/products", response_model=List[ProductAnalytics])
async def get_product_analysis(
    limit: int = Query(10, description="Número de produtos a retornar"),
    db: Session = Depends(get_db)
):
    """Retorna análise dos produtos mais vendidos"""
    try:
        result = get_product_analytics(db, limit)
        if not result:
            raise NotFoundError(message="Nenhum dado de produtos encontrado")
        return result
    except (ValidationError, NotFoundError) as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao processar análise de produtos: {str(e)}")
        raise DatabaseError(message="Erro ao processar análise de produtos", details={"error": str(e)})

@router.get("/customers", response_model=CustomerMetrics)
async def get_customer_analysis(db: Session = Depends(get_db)):
    """Retorna métricas relacionadas aos clientes"""
    try:
        result = get_customer_metrics(db)
        if not result:
            raise NotFoundError(message="Nenhum dado de clientes encontrado")
        return result
    except (ValidationError, NotFoundError) as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao processar análise de clientes: {str(e)}")
        raise DatabaseError(message="Erro ao processar análise de clientes", details={"error": str(e)})