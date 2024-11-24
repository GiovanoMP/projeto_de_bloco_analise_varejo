import streamlit as st

def main():
    st.set_page_config(
        page_title="Documentação - Análise de Sentimentos",
        page_icon="📚",
        layout="wide"
    )

    st.title("📚 Documentação do Projeto de Análise de Sentimentos")

    # Introdução
    st.markdown("""
    # Exemplo de uso local de LLM para Análise de Sentimentos

    Este é um exemplo de implementação de análise de sentimentos usando o modelo BERT multilíngue
    localmente. O código demonstra como criar uma interface interativa com Streamlit para análise
    de sentimentos em tempo real.

    ## Estrutura do Modelo
    O modelo utiliza BERT (Bidirectional Encoder Representations from Transformers) em sua versão
    multilíngue, permitindo análise de textos em diversos idiomas.

    ## Funcionalidades Implementadas
    - Análise de sentimentos em tempo real
    - Suporte a múltiplos idiomas
    - Interface interativa com Streamlit
    - Histórico de análises
    - Estatísticas de uso

    ## Como Usar
    1. Digite seu texto na área designada
    2. Clique em "Analisar Sentimento"
    3. Visualize os resultados e estatísticas
    """)

    # Código Completo
    st.subheader("💻 Código Completo")
    
    codigo_completo = '''
# Imports
import streamlit as st
from transformers import pipeline
from datetime import datetime
import pandas as pd


# Configuração inicial do modelo
@st.cache_resource
def load_model():
    """Carrega o modelo BERT multilíngue para análise de sentimento"""
    try:
        model = pipeline(
            "sentiment-analysis",
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
        )
        return model
    except Exception as e:
        st.error(f"Erro ao carregar o modelo: {str(e)}")
        return None

def analyze_sentiment(text, analyzer):
    """Analisa o sentimento do texto fornecido"""
    try:
        sentiment_result = analyzer(text)[0]
        
        label = sentiment_result['label']
        score = float(sentiment_result['score'])
        
        polarity = (float(label.split()[0]) - 3) / 2
        
        if polarity > 0:
            sentiment = "Positivo"
            color = "🟢"
        elif polarity < 0:
            sentiment = "Negativo"
            color = "🔴"
        else:
            sentiment = "Neutro"
            color = "⚪"

        return {
            "text": text,
            "sentiment": sentiment,
            "polarity": polarity,
            "score": score,
            "color": color,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        st.error(f"Erro ao analisar texto: {str(e)}")
        return None

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Análise de Sentimentos",
        page_icon="🎭",
        layout="wide"
    )

    # Carregar modelo
    model = load_model()
    if not model:
        st.error("Não foi possível carregar o modelo. Por favor, recarregue a página.")
        return

    # Título e descrição
    st.title("🎭 Análise de Sentimentos em Tempo Real")
    st.markdown("""
    ### Analise sentimentos em textos usando Inteligência Artificial
    Esta ferramenta utiliza um modelo BERT multilíngue para detectar sentimentos em textos.
    """)

    # Layout principal
    col1, col2 = st.columns([2, 1])

    with col1:
        # Área de entrada de texto
        st.subheader("💭 Digite seu texto")
        text_input = st.text_area(
            "Digite o texto para análise",
            height=100,
            placeholder="Escreva aqui o texto que você quer analisar..."
        )

        # Histórico de análises
        if 'analysis_history' not in st.session_state:
            st.session_state.analysis_history = []

        # Botão de análise
        if st.button("🔍 Analisar Sentimento", use_container_width=True):
            if text_input.strip():
                result = analyze_sentiment(text_input, model)
                if result:
                    st.session_state.analysis_history.append(result)
                    
                    # Mostrar resultado atual
                    st.success("Análise concluída!")
                    col_res1, col_res2, col_res3 = st.columns(3)
                    with col_res1:
                        st.metric("Sentimento", f"{result['color']} {result['sentiment']}")
                    with col_res2:
                        st.metric("Confiança", f"{result['score']:.2%}")
                    with col_res3:
                        st.metric("Polaridade", f"{result['polarity']:.2f}")
            else:
                st.warning("Por favor, digite algum texto para análise.")

        # Histórico de análises em tabela
        if st.session_state.analysis_history:
            st.subheader("📊 Histórico de Análises")
            df = pd.DataFrame(st.session_state.analysis_history)
            st.dataframe(
                df[['text', 'sentiment', 'score', 'timestamp']],
                hide_index=True,
                use_container_width=True
            )

    with col2:
        st.subheader("⚙️ Controles e Informações")
        
        # Botão para limpar histórico
        if st.button("🗑️ Limpar Histórico", use_container_width=True):
            st.session_state.analysis_history = []
            st.experimental_rerun()

        # Estatísticas
        if st.session_state.analysis_history:
            st.subheader("📈 Estatísticas")
            total = len(st.session_state.analysis_history)
            positivos = sum(1 for x in st.session_state.analysis_history if x['sentiment'] == 'Positivo')
            negativos = sum(1 for x in st.session_state.analysis_history if x['sentiment'] == 'Negativo')
            neutros = total - positivos - negativos

            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Positivos", f"{positivos} ({(positivos/total)*100:.1f}%)")
            with col_stat2:
                st.metric("Negativos", f"{negativos} ({(negativos/total)*100:.1f}%)")
            with col_stat3:
                st.metric("Neutros", f"{neutros} ({(neutros/total)*100:.1f}%)")

        # Informações sobre o modelo
        st.subheader("ℹ️ Sobre o Modelo")
        st.markdown("""
        **Modelo:** BERT Multilíngue
        
        **Capacidades:**
        - Análise de textos em múltiplos idiomas
        - Detecção de sentimentos: Positivo, Negativo, Neutro
        - Pontuação de confiança para cada análise
        
        **Como interpretar:**
        - 🟢 Positivo: Sentimento favorável
        - ⚪ Neutro: Sentimento ambíguo ou neutral
        - 🔴 Negativo: Sentimento desfavorável
        
        A pontuação de confiança indica o quão seguro o modelo está da sua análise.
        """)

if __name__ == "__main__":
    main()
    '''
    
    # Exibindo o código com syntax highlighting
    st.code(codigo_completo, language='python')

    # Notas importantes
    st.subheader("⚠️ Notas Importantes")
    st.markdown("""
    1. Este código requer as seguintes bibliotecas:
        - streamlit
        - transformers
        - pandas
    
    2. O modelo BERT será baixado na primeira execução
    
    3. Recomenda-se ter pelo menos 4GB de RAM disponível
    
    4. Para executar, salve o código em um arquivo .py e use:
    ```bash
    streamlit run seu_arquivo.py
    ```
    """)

if __name__ == "__main__":
    main()
