from dotenv import load_dotenv
from agents.analyst_agent import AnalystAgent
import os

def test_analyst():
    load_dotenv()
    
    # Criar instância do agente
    analyst = AnalystAgent(
        supabase_url=os.getenv('SUPABASE_URL'),
        supabase_key=os.getenv('SUPABASE_KEY')
    )
    
    # Obter o agente
    agent = analyst.get_agent()
    
    # Testar uma análise simples
    result = agent.execute("Faça uma análise básica dos dados de vendas por categoria")
    
    print("\n=== RESULTADO DO TESTE ===")
    print(result)

if __name__ == "__main__":
    test_analyst()
