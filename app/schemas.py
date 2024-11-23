from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

# Schemas para Análise de Vendas por País
class VendasPorPaisResponse(BaseModel):
    pais: str
    total_vendas: float
    numero_clientes: int
    ticket_medio: float

class AnaliseVendasPaisResponse(BaseModel):
    status: str
    data: List[VendasPorPaisResponse]
    total_paises: int

# Schemas para Análise Temporal
class VendasTemporalResponse(BaseModel):
    periodo: str
    total_vendas: float
    quantidade_vendas: int
    ticket_medio: float

class AnaliseTemporalResponse(BaseModel):
    status: str
    vendas_por_mes: List[VendasTemporalResponse]
    vendas_por_dia_semana: List[VendasTemporalResponse]
    vendas_por_semana: List[VendasTemporalResponse]

# Schemas para Análise de Produtos
class ProdutoAnalise(BaseModel):
    codigo: str
    descricao: str
    quantidade_vendida: int
    valor_total: float
    ticket_medio: float

class CategoriaProdutoAnalise(BaseModel):
    categoria: str
    valor_total: float
    quantidade_vendida: int
    ticket_medio: float

class AnaliseProdutosResponse(BaseModel):
    status: str
    top_produtos: List[ProdutoAnalise]
    categorias: List[CategoriaProdutoAnalise]
    distribuicao_preco: Dict[str, float]

# Schemas para Análise de Clientes
class ClienteAnalise(BaseModel):
    id_cliente: str
    total_compras: float
    frequencia_compras: int
    ticket_medio: float
    pais: str

class AnaliseClientesResponse(BaseModel):
    status: str
    top_clientes: List[ClienteAnalise]
    distribuicao_por_pais: Dict[str, int]
    media_compras_por_cliente: float

# Schemas para Análise de Faturamento
class FaturamentoDiario(BaseModel):
    data: datetime
    valor_total: float
    quantidade_faturas: int
    ticket_medio: float

class AnaliseFaturamentoResponse(BaseModel):
    status: str
    media_diaria: float
    proporcao_faturas_unicas: float
    evolucao_temporal: List[FaturamentoDiario]
