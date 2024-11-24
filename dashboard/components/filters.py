# components/filters.py
import streamlit as st
from datetime import datetime, timedelta

def date_range_filter():
    """
    Cria um filtro de intervalo de datas
    Retorna: data_inicio, data_fim
    """
    # Data final padrão é hoje
    data_fim = datetime.now()
    # Data inicial padrão é 30 dias atrás
    data_inicio = data_fim - timedelta(days=30)
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input(
            "Data Inicial",
            value=data_inicio,
            format="DD/MM/YYYY"
        )
    
    with col2:
        data_fim = st.date_input(
            "Data Final",
            value=data_fim,
            format="DD/MM/YYYY"
        )
    
    return data_inicio, data_fim

def category_filter(categories):
    """
    Cria um filtro de categorias
    Params:
        categories: lista de categorias disponíveis
    Retorna: lista de categorias selecionadas
    """
    return st.multiselect(
        "Categorias",
        options=categories,
        default=categories
    )
