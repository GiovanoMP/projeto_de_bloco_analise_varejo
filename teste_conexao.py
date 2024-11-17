import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")

def test_connection():
    try:
        # Inicializa o cliente Supabase
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Faz uma consulta usando os nomes exatos das colunas e da tabela
        response = supabase.table('transactions_sample').select(
            "DataFatura",
            "PrecoUnitario",
            "IDCliente",
            "Pais",
            "CategoriaProduto",
            "CategoriaPreco",
            "ValorTotalFatura",
            "NumeroFatura",
            "CodigoProduto",
            "Quantidade"
        ).limit(5).execute()
        
        print("✅ Conexão bem sucedida!")
        print("\nPrimeiros registros da tabela:")
        for row in response.data:
            print("\nRegistro:")
            for key, value in row.items():
                print(f"{key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    test_connection()
