class Settings:
    """
    Configurações da aplicação.
    
    URLs da API:
    - Desenvolvimento (atual): http://localhost:8000
    - Produção (futuro): https://seu-backend.onrender.com
    """
    
    # API Configuration
    API_BASE_URL = "http://localhost:8000"  # TODO: Alterar para URL do Render após deploy
    
    # API Endpoints
    ENDPOINT_VENDAS_PAIS = f"{API_BASE_URL}/api/v1/analise/vendas-por-pais"
    ENDPOINT_TEMPORAL = f"{API_BASE_URL}/api/v1/analise/temporal"
    ENDPOINT_PRODUTOS = f"{API_BASE_URL}/api/v1/analise/produtos"
    ENDPOINT_CLIENTES = f"{API_BASE_URL}/api/v1/analise/clientes"
    ENDPOINT_FATURAMENTO = f"{API_BASE_URL}/api/v1/analise/faturamento"  # Endpoint que faltava
