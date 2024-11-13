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
    start_date: date = Query(..., description="Data inicial da análise"),
    end_date: date = Query(..., description="Data final da análise"),
    db: Session = Depends(get_db)
):
    """Retorna métricas de vendas para o período especificado"""
    try:
        # Validação de datas
        if start_date > end_date:
            raise ValidationError(
                message="Data inicial deve ser anterior à data final",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        logger.debug(f"Recebida requisição de análise de vendas: {start_date} até {end_date}")
        result = get_sales_metrics(db, start_date, end_date)
        
        if not result:
            raise NotFoundError(
                message="Nenhum dado encontrado para o período especificado",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        logger.debug(f"Resultado da análise: {result}")
        return result
        
    except (ValidationError, NotFoundError) as e:
        raise e
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
        if start_date > end_date:
            raise ValidationError(
                message="Data inicial deve ser anterior à data final",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        query = text("""
            WITH daily_sales AS (
                SELECT 
                    DATE("DataFatura") as sale_date,
                    SUM("ValorTotalFatura") as daily_total,
                    COUNT(DISTINCT "NumeroFatura") as transaction_count,
                    COUNT(DISTINCT "IDCliente") as unique_customers
                FROM transactions_main
                WHERE DATE("DataFatura") BETWEEN :start_date AND :end_date
                GROUP BY DATE("DataFatura")
            ),
            moving_averages AS (
                SELECT 
                    sale_date,
                    daily_total,
                    transaction_count,
                    unique_customers,
                    AVG(daily_total) OVER (
                        ORDER BY sale_date 
                        ROWS BETWEEN :window PRECEDING AND CURRENT ROW
                    ) as moving_avg_sales
                FROM daily_sales
            )
            SELECT 
                sale_date as date,
                ROUND(daily_total::numeric, 2) as total_sales,
                transaction_count as transactions,
                unique_customers,
                ROUND(moving_avg_sales::numeric, 2) as moving_avg_sales,
                CASE 
                    WHEN daily_total > moving_avg_sales THEN 'up'
                    WHEN daily_total < moving_avg_sales THEN 'down'
                    ELSE 'stable'
                END as trend,
                ROUND(
                    COALESCE(
                        100 * (daily_total - LAG(daily_total) OVER (ORDER BY sale_date)) / 
                        NULLIF(LAG(daily_total) OVER (ORDER BY sale_date), 0),
                        0
                    )::numeric,
                    2
                ) as growth_rate
            FROM moving_averages
            ORDER BY date
        """)

        try:
            result = db.execute(query, {
                "start_date": start_date,
                "end_date": end_date,
                "window": window
            })
        except Exception as e:
            raise DatabaseError(
                message="Erro ao executar query temporal",
                details={"error": str(e)}
            )

        temporal_data = []
        for row in result:
            temporal_data.append({
                "date": row.date.strftime("%Y-%m-%d"),
                "total_sales": float(row.total_sales),
                "transactions": int(row.transactions),
                "unique_customers": int(row.unique_customers),
                "moving_avg_sales": float(row.moving_avg_sales),
                "trend": str(row.trend),
                "growth_rate": float(row.growth_rate)
            })

        if not temporal_data:
            raise NotFoundError(
                message="Nenhum dado encontrado para o período especificado",
                details={"start_date": str(start_date), "end_date": str(end_date)}
            )

        return temporal_data

    except (ValidationError, NotFoundError, DatabaseError) as e:
        raise e
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