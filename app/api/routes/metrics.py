from fastapi import APIRouter, HTTPException
from ..services.database import get_supabase_client

router = APIRouter()
supabase = get_supabase_client()

@router.get("/metrics")
async def get_metrics():
    """Retorna métricas gerais do dashboard"""
    try:
        # Total de vendas
        total_sales = supabase.table("transactions_sample")\
            .select("ValorTotalFatura")\
            .execute()
        
        # Número de clientes únicos
        unique_customers = supabase.table("transactions_sample")\
            .select("IDCliente")\
            .execute()
        
        # Número total de produtos únicos
        unique_products = supabase.table("transactions_sample")\
            .select("CodigoProduto")\
            .execute()
        
        return {
            "total_sales": sum([row['ValorTotalFatura'] for row in total_sales.data]),
            "unique_customers": len(set([row['IDCliente'] for row in unique_customers.data])),
            "unique_products": len(set([row['CodigoProduto'] for row in unique_products.data])),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
