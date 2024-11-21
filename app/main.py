from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Transações",
    description="API para análise de dados de transações comerciais",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["transactions"]
)

@app.get("/")
def read_root():
    return {
        "message": "Bem-vindo à API de Transações",
        "docs": "/docs",
        "endpoints": {
            "transactions": "/api/v1/transactions/",
            "summary": "/api/v1/transactions/summary",
            "by_category": "/api/v1/transactions/by-category",
            "by_country": "/api/v1/transactions/by-country"
        }
    }




