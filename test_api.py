import requests

def test_api_health():
    """Testa conexão básica com a API"""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao conectar: {str(e)}")
        return False

def test_analytics_endpoints():
    """Testa endpoints de analytics"""
    endpoints = [
        "/api/v1/analytics/sales?start_date=2011-01-01&end_date=2011-12-31",
        "/api/v1/analytics/sales/temporal?start_date=2011-01-01&end_date=2011-12-31&window=7"
    ]
    
    for endpoint in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            print(f"\nTesting: {url}")
            response = requests.get(url)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")  # Primeiros 200 caracteres
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Testando API...")
    if test_api_health():
        print("\nHealth check OK, testando endpoints...")
        test_analytics_endpoints()
    else:
        print("Health check falhou!")