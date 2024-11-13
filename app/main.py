from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from .api.errors.handlers import error_handler, APIError
from .api.routes import analytics, health
import logging
from datetime import datetime

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criação da aplicação
app = FastAPI(
    title="RetailSense AI",
    description="""
    API para análise avançada de dados de varejo com foco em:
    * Análise de vendas e métricas temporais
    * Segmentação de clientes
    * Análise de produtos
    * Insights automatizados
    
    Desenvolvido com FastAPI, SQLAlchemy e Machine Learning.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",  # Streamlit local
        "http://localhost:3000"   # Frontend local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar handler de erros
app.add_exception_handler(APIError, error_handler)

# Middleware para logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Status: {response.status_code} | "
        f"Duration: {duration:.3f}s"
    )
    
    return response

# Customização do OpenAPI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="RetailSense AI",
        version="1.0.0",
        description="""
        RetailSense AI - API para Análise Inteligente de Dados de Varejo
        
        ## Funcionalidades
        
        * 📊 **Analytics**: Métricas e análises detalhadas de vendas
        * 👥 **Clientes**: Segmentação e análise de comportamento
        * 📈 **Produtos**: Análise de desempenho e tendências
        * 🎯 **Insights**: Recomendações automáticas baseadas em dados
        
        ## Autenticação
        
        Esta API utiliza autenticação via token. Inclua o token no header:
        ```
        Authorization: Bearer {seu_token}
        ```
        
        ## Ambientes
        
        * Desenvolvimento: http://localhost:8000
        * Produção: {url_producao}
        
        ## Suporte
        
        Para suporte, contate: suporte@retailsense.ai
        """,
        routes=app.routes,
    )
    
    # Customizar tags
    openapi_schema["tags"] = [
        {
            "name": "analytics",
            "description": "Endpoints para análise de dados e métricas"
        },
        {
            "name": "health",
            "description": "Endpoints para monitoramento da saúde da API"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Incluir routers com tags
app.include_router(
    analytics.router,
    prefix="/api/v1",
    tags=["analytics"]
)
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["health"]
)

# Rota raiz com informações úteis
@app.get("/")
async def root():
    """
    Retorna informações sobre a API e seu status atual
    """
    return {
        "app": "RetailSense AI",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "health": "/api/v1/health",
        "endpoints": {
            "analytics": "/api/v1/analytics",
            "health": "/api/v1/health"
        }
    }

# Handler para erros não tratados
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.error(f"Erro não tratado: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Erro interno do servidor",
            "timestamp": datetime.now().isoformat()
        }
    )

# Startup e shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando API RetailSense AI...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Encerrando API RetailSense AI...")