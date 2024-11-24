# components/charts.py
import plotly.express as px

def create_map_chart(data):
    """Cria mapa interativo com plotly"""
    fig = px.scatter_geo(
        data,
        locations="pais",
        color="valor_vendas",
        hover_name="pais",
        size="valor_vendas",
        projection="natural earth",
        title="Distribuição Global de Vendas"
    )
    return fig

def create_time_series(data):
    """Cria gráfico de série temporal"""
    fig = px.line(
        data,
        x="data",
        y="valor",
        title="Evolução Temporal"
    )
    fig.update_layout(
        xaxis_title="Período",
        yaxis_title="Valor"
    )
    return fig

def create_bar_chart(data):
    """Cria gráfico de barras padronizado"""
    fig = px.bar(
        data,
        x="categoria",
        y="valor",
        title="Gráfico de Barras"
    )
    fig.update_layout(
        xaxis_title="Categorias",
        yaxis_title="Valor"
    )
    return fig
