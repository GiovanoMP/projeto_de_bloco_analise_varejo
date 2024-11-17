from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.settings import API_TITLE, API_DESCRIPTION, API_VERSION
from .routes import metrics  # Por enquanto, só importamos metrics

# Inicialização da API
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão apenas da rota de métricas por enquanto
app.include_router(metrics.router, prefix="/api", tags=["Métricas"])

# Rota de teste
@app.get("/")
async def root():
    return {"message": "API Analytics Dashboard"}
