from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import get_db
from sqlalchemy import text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")

@app.get("/test")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text('SELECT COUNT(*) FROM transactions_sample')).scalar()
        return {
            "status": "success",
            "message": "Conexão estabelecida com sucesso!",
            "total_registros": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Erro na conexão: {str(e)}"
        }
@app.get("/")
async def root():
    return {
        "mensagem": "Bem-vindo à API de Análise de Transações",
        "versao": "1.0",
        "endpoints_disponíveis": {
            "Teste de Conexão": "/test",
            "Análise de Vendas por País": "/api/v1/analise/vendas-por-pais",
            "Análise Temporal": "/api/v1/analise/temporal",
            "Análise de Produtos": "/api/v1/analise/produtos",
            "Análise de Clientes": "/api/v1/analise/clientes",
            "Análise de Faturamento": "/api/v1/analise/faturamento"
        },
        "documentação": {
            "Swagger UI": "/docs",
            "ReDoc": "/redoc"
        }
    }
