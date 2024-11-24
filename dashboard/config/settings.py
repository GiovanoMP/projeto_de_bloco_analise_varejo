class Settings:
    """
    Configurações da aplicação.
    
    URLs da API:
    - Desenvolvimento: http://localhost:8000
    - Produção: https://render-api-rvd7.onrender.com
    """
    
    # API Configuration
    API_BASE_URL = "https://render-api-rvd7.onrender.com"
    
    # API Endpoints
    ENDPOINT_VENDAS_PAIS = f"{API_BASE_URL}/api/v1/analise/vendas-por-pais"
    ENDPOINT_TEMPORAL = f"{API_BASE_URL}/api/v1/analise/temporal"
    ENDPOINT_PRODUTOS = f"{API_BASE_URL}/api/v1/analise/produtos"
    ENDPOINT_CLIENTES = f"{API_BASE_URL}/api/v1/analise/clientes"
    ENDPOINT_FATURAMENTO = f"{API_BASE_URL}/api/v1/analise/faturamento"

