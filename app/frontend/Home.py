import streamlit as st

def main():
    # Configuração da página
    st.set_page_config(
        page_title="RetailSense AI",
        page_icon="🏪",
        layout="wide"
    )

    # Título principal com estilo personalizado
    st.markdown("""
        <h1 style='text-align: center; color: #FF4B4B;'>RetailSense AI</h1>
        <h3 style='text-align: center;'>Inteligência Artificial para um Varejo mais Sustentável</h3>
    """, unsafe_allow_html=True)

    # Breve descrição do projeto
    st.markdown("""
    ---
    ### 🎯 Sobre o Projeto
    
    O RetailSense AI é uma plataforma inovadora que combina análise avançada de dados 
    com práticas sustentáveis para o varejo. Nossa solução oferece insights valiosos 
    para tomada de decisões mais inteligentes e ambientalmente responsáveis.
    
    ### 🌟 Principais Funcionalidades
    
    - **📊 Análise de Transações**: Visualize e analise dados de vendas com filtros personalizáveis
    - **🌍 Análise Geográfica**: Explore o desempenho de vendas por país
    - **📈 Análise por Categoria**: Acompanhe o desempenho por categoria de produtos
    - **💡 Insights Inteligentes**: Obtenha resumos e métricas importantes do seu negócio
    
    ### 📱 Como Usar
    
    1. **Navegação**: Use o menu lateral para acessar diferentes análises
    2. **Filtros**: Utilize os filtros de data para personalizar suas análises
    3. **Visualizações**: Interaja com os gráficos para obter informações detalhadas
    4. **Exportação**: Baixe relatórios e visualizações quando disponíveis
    
    ### 🎨 Recursos Visuais
    
    - Gráficos interativos
    - Dashboards personalizáveis
    - Métricas em tempo real
    - Exportação de dados
    """)

    # Informações adicionais em colunas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📚 Documentação
        Para mais informações sobre como utilizar cada recurso, 
        consulte nossa documentação detalhada.
        """)

    with col2:
        st.markdown("""
        ### 💡 Dicas
        - Use os filtros de data para análises específicas
        - Compare períodos diferentes
        - Explore diferentes visualizações
        """)

    # Rodapé
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center;'>
            <p>Desenvolvido com ❤️ pela Equipe RetailSense AI</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
