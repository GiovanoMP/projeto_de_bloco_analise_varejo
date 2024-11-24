import streamlit as st

def main():
    # Configurações da página
    st.set_page_config(
        page_title="Dashboard de Vendas",
        page_icon="📊",
        layout="wide"
    )

    # Cabeçalho
    st.title("📊 Dashboard de Análise de Vendas")
    
    # Subtítulo com descrição
    st.markdown("""
    ### Bem-vindo ao Dashboard de Análise de Vendas
    
    Este dashboard oferece uma visão completa das vendas, com análises detalhadas em três áreas principais:
    
    1. **📍 Análise Geográfica**
        * Distribuição de vendas por país
        * Performance regional
        * Mapeamento de clientes
    
    2. **📈 Análise Temporal e Produtos**
        * Tendências de vendas
        * Performance de produtos
        * Sazonalidade
    
    3. **👥 Análise de Clientes**
        * Segmentação de clientes
        * Comportamento de compra
        * Métricas de faturamento
    
    *Utilize o menu lateral para navegar entre as diferentes análises.*
    """)
    
    # Rodapé
    st.markdown("---")
    st.markdown("*Desenvolvido por Giovano M Panatta - Infnet - 2024*")

if __name__ == "__main__":
    main()
