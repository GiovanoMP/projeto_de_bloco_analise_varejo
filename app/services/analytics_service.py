from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import date, datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_sales_metrics(db: Session, start_date: date, end_date: date) -> dict:
    """Obtém métricas de vendas do período"""
    try:
        logger.debug(f"Consultando vendas para o período: {start_date} até {end_date}")
        
        query = text("""
            SELECT 
                COALESCE(SUM("ValorTotalFatura"), 0.0) as total_sales,
                COALESCE(AVG("ValorTotalFatura"), 0.0) as average_ticket,
                COUNT(DISTINCT "IDCliente") as total_customers,
                COUNT(DISTINCT "NumeroFatura") as total_transactions,
                MIN("DataFatura") as period_start,
                MAX("DataFatura") as period_end
            FROM transactions_sample
            WHERE DATE("DataFatura") BETWEEN :start_date AND :end_date
        """)
        
        result = db.execute(
            query, 
            {"start_date": start_date, "end_date": end_date}
        )
        
        row = result.fetchone()
        if row is None:
            return {
                "total_sales": 0.0,
                "average_ticket": 0.0,
                "total_customers": 0,
                "total_transactions": 0,
                "period_start": start_date,
                "period_end": end_date
            }
            
        return {
            "total_sales": float(row.total_sales),
            "average_ticket": float(row.average_ticket),
            "total_customers": int(row.total_customers),
            "total_transactions": int(row.total_transactions),
            "period_start": row.period_start,
            "period_end": row.period_end
        }
    except Exception as e:
        logger.error(f"Erro ao consultar vendas: {str(e)}")
        raise Exception(f"Erro ao consultar vendas: {str(e)}")

def get_product_analytics(db: Session, limit: int) -> List[Dict]:
    """Obtém análise dos produtos mais vendidos"""
    try:
        query = text("""
            SELECT 
                "CodigoProduto" as product_code,
                "Descricao" as description,
                CAST(SUM("Quantidade") as INTEGER) as total_quantity,
                CAST(SUM("ValorTotalFatura") as FLOAT) as total_revenue,
                "CategoriaProduto" as category,
                "CategoriaPreco" as price_category
            FROM transactions_sample
            GROUP BY 
                "CodigoProduto", 
                "Descricao", 
                "CategoriaProduto", 
                "CategoriaPreco"
            ORDER BY SUM("ValorTotalFatura") DESC
            LIMIT :limit
        """)
        
        result = db.execute(query, {"limit": limit})
        
        products = []
        for row in result.fetchall():
            products.append({
                "product_code": str(row.product_code),
                "description": str(row.description),
                "total_quantity": int(row.total_quantity),
                "total_revenue": float(row.total_revenue),
                "category": str(row.category),
                "price_category": str(row.price_category)
            })
        
        return products
    except Exception as e:
        logger.error(f"Erro ao consultar produtos: {str(e)}")
        raise Exception(f"Erro ao consultar produtos: {str(e)}")

def get_customer_metrics(db: Session) -> Dict:
    """Obtém métricas relacionadas aos clientes"""
    try:
        logger.debug("Iniciando consulta de métricas de clientes")
        
        # Query para métricas gerais
        metrics_query = text("""
            SELECT 
                COUNT(DISTINCT "IDCliente") as total_unique_customers,
                ROUND(AVG("ValorTotalFatura")::numeric, 2) as average_customer_value
            FROM transactions_sample
        """)
        
        logger.debug("Executando query de métricas gerais")
        metrics_result = db.execute(metrics_query)
        metrics_row = metrics_result.fetchone()
        
        if not metrics_row:
            logger.warning("Nenhuma métrica geral encontrada")
            metrics = {
                "total_unique_customers": 0,
                "average_customer_value": 0.0
            }
        else:
            metrics = {
                "total_unique_customers": int(metrics_row.total_unique_customers),
                "average_customer_value": float(metrics_row.average_customer_value)
            }
        
        # Query para países
        countries_query = text("""
            SELECT 
                "Pais" as country,
                COUNT(DISTINCT "IDCliente") as customer_count,
                ROUND(AVG("ValorTotalFatura")::numeric, 2) as average_spend
            FROM transactions_sample
            GROUP BY "Pais"
            ORDER BY COUNT(DISTINCT "IDCliente") DESC
            LIMIT 5
        """)
        
        logger.debug("Executando query de países")
        countries_result = db.execute(countries_query)
        top_countries = []
        
        for row in countries_result:
            top_countries.append({
                "country": str(row.country),
                "customer_count": int(row.customer_count),
                "average_spend": float(row.average_spend)
            })
        
        # Query para segmentos
        segments_query = text("""
            WITH customer_avg AS (
                SELECT 
                    "IDCliente",
                    AVG("ValorTotalFatura") as avg_value
                FROM transactions_sample
                GROUP BY "IDCliente"
            )
            SELECT 
                CASE 
                    WHEN avg_value <= 5 THEN 'Baixo Valor'
                    WHEN avg_value <= 20 THEN 'Médio Valor'
                    ELSE 'Alto Valor'
                END as segment_name,
                COUNT(*) as customer_count,
                ROUND(AVG(avg_value)::numeric, 2) as average_value
            FROM customer_avg
            GROUP BY 1
            ORDER BY 3 DESC
        """)
        
        logger.debug("Executando query de segmentos")
        segments_result = db.execute(segments_query)
        customer_segments = {}
        
        for row in segments_result:
            segment_name = str(row.segment_name)
            customer_segments[segment_name] = {
                "segment_name": segment_name,
                "customer_count": int(row.customer_count),
                "average_value": float(row.average_value)
            }
        
        logger.debug("Construindo resposta final")
        response = {
            "total_unique_customers": metrics["total_unique_customers"],
            "average_customer_value": metrics["average_customer_value"],
            "top_countries": top_countries,
            "customer_segments": customer_segments
        }
        
        logger.debug(f"Resposta construída: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Erro ao consultar métricas de clientes: {str(e)}")
        logger.exception("Stack trace completo:")
        raise Exception(f"Erro ao consultar métricas de clientes: {str(e)}")