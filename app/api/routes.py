from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, extract
from app.database import get_db
from app.models import Transaction
from app.schemas import *
from typing import Dict

router = APIRouter()

@router.get("/analise/vendas-por-pais", response_model=AnaliseVendasPaisResponse)
def get_vendas_por_pais(db: Session = Depends(get_db)):
    try:
        resultados = (
            db.query(
                Transaction.Pais,
                func.sum(Transaction.ValorTotalFatura).label('total_vendas'),
                func.count(distinct(Transaction.IDCliente)).label('numero_clientes'),
                (func.sum(Transaction.ValorTotalFatura) / func.count(distinct(Transaction.IDCliente))).label('ticket_medio')
            )
            .group_by(Transaction.Pais)
            .order_by(func.sum(Transaction.ValorTotalFatura).desc())
            .all()
        )

        dados = [
            VendasPorPaisResponse(
                pais=r.Pais,
                total_vendas=float(r.total_vendas),
                numero_clientes=r.numero_clientes,
                ticket_medio=float(r.ticket_medio)
            )
            for r in resultados
        ]

        return AnaliseVendasPaisResponse(
            status="success",
            data=dados,
            total_paises=len(dados)
        )
    except Exception as e:
        return AnaliseVendasPaisResponse(status="error", data=[], total_paises=0)

@router.get("/analise/temporal", response_model=AnaliseTemporalResponse)
def get_analise_temporal(db: Session = Depends(get_db)):
    try:
        # Vendas por mês
        vendas_mes = (
            db.query(
                Transaction.Mes,
                func.sum(Transaction.ValorTotalFatura).label('total_vendas'),
                func.count(Transaction.NumeroFatura).label('quantidade_vendas')
            )
            .group_by(Transaction.Mes)
            .order_by(Transaction.Mes)
            .all()
        )

        # Vendas por dia da semana
        vendas_dia_semana = (
            db.query(
                Transaction.DiaSemana,
                func.sum(Transaction.ValorTotalFatura).label('total_vendas'),
                func.count(Transaction.NumeroFatura).label('quantidade_vendas')
            )
            .group_by(Transaction.DiaSemana)
            .order_by(Transaction.DiaSemana)
            .all()
        )

        # Vendas por semana
        vendas_semana = (
            db.query(
                Transaction.SemanaAno,
                func.sum(Transaction.ValorTotalFatura).label('total_vendas'),
                func.count(Transaction.NumeroFatura).label('quantidade_vendas')
            )
            .group_by(Transaction.SemanaAno)
            .order_by(Transaction.SemanaAno)
            .all()
        )

        return AnaliseTemporalResponse(
            status="success",
            vendas_por_mes=[
                VendasTemporalResponse(
                    periodo=f"Mês {r.Mes}",
                    total_vendas=float(r.total_vendas),
                    quantidade_vendas=r.quantidade_vendas,
                    ticket_medio=float(r.total_vendas/r.quantidade_vendas)
                ) for r in vendas_mes
            ],
            vendas_por_dia_semana=[
                VendasTemporalResponse(
                    periodo=f"Dia {r.DiaSemana}",
                    total_vendas=float(r.total_vendas),
                    quantidade_vendas=r.quantidade_vendas,
                    ticket_medio=float(r.total_vendas/r.quantidade_vendas)
                ) for r in vendas_dia_semana
            ],
            vendas_por_semana=[
                VendasTemporalResponse(
                    periodo=f"Semana {r.SemanaAno}",
                    total_vendas=float(r.total_vendas),
                    quantidade_vendas=r.quantidade_vendas,
                    ticket_medio=float(r.total_vendas/r.quantidade_vendas)
                ) for r in vendas_semana
            ]
        )
    except Exception as e:
        return AnaliseTemporalResponse(status="error", vendas_por_mes=[], vendas_por_dia_semana=[], vendas_por_semana=[])

@router.get("/analise/produtos", response_model=AnaliseProdutosResponse)
def get_analise_produtos(db: Session = Depends(get_db)):
    try:
        # Top 10 produtos
        top_produtos = (
            db.query(
                Transaction.CodigoProduto,
                Transaction.Descricao,
                func.sum(Transaction.Quantidade).label('quantidade_vendida'),
                func.sum(Transaction.ValorTotalFatura).label('valor_total')
            )
            .group_by(Transaction.CodigoProduto, Transaction.Descricao)
            .order_by(func.sum(Transaction.ValorTotalFatura).desc())
            .limit(10)
            .all()
        )

        # Análise por categoria
        categorias = (
            db.query(
                Transaction.CategoriaProduto,
                func.sum(Transaction.ValorTotalFatura).label('valor_total'),
                func.sum(Transaction.Quantidade).label('quantidade_vendida')
            )
            .group_by(Transaction.CategoriaProduto)
            .order_by(func.sum(Transaction.ValorTotalFatura).desc())
            .all()
        )

        # Distribuição por categoria de preço
        dist_preco = (
            db.query(
                Transaction.CategoriaPreco,
                func.sum(Transaction.ValorTotalFatura).label('valor_total')
            )
            .group_by(Transaction.CategoriaPreco)
            .all()
        )

        return AnaliseProdutosResponse(
            status="success",
            top_produtos=[
                ProdutoAnalise(
                    codigo=p.CodigoProduto,
                    descricao=p.Descricao,
                    quantidade_vendida=p.quantidade_vendida,
                    valor_total=float(p.valor_total),
                    ticket_medio=float(p.valor_total/p.quantidade_vendida)
                ) for p in top_produtos
            ],
            categorias=[
                CategoriaProdutoAnalise(
                    categoria=c.CategoriaProduto,
                    valor_total=float(c.valor_total),
                    quantidade_vendida=c.quantidade_vendida,
                    ticket_medio=float(c.valor_total/c.quantidade_vendida)
                ) for c in categorias
            ],
            distribuicao_preco={
                d.CategoriaPreco: float(d.valor_total) for d in dist_preco
            }
        )
    except Exception as e:
        return AnaliseProdutosResponse(status="error", top_produtos=[], categorias=[], distribuicao_preco={})

@router.get("/analise/clientes", response_model=AnaliseClientesResponse)
def get_analise_clientes(db: Session = Depends(get_db)):
    try:
        # Top 10 clientes
        top_clientes = (
            db.query(
                Transaction.IDCliente,
                func.sum(Transaction.ValorTotalFatura).label('total_compras'),
                func.count(Transaction.NumeroFatura).label('frequencia_compras'),
                func.max(Transaction.Pais).label('pais')
            )
            .group_by(Transaction.IDCliente)
            .order_by(func.sum(Transaction.ValorTotalFatura).desc())
            .limit(10)
            .all()
        )

        # Distribuição por país
        dist_pais = dict(
            db.query(
                Transaction.Pais,
                func.count(distinct(Transaction.IDCliente))
            )
            .group_by(Transaction.Pais)
            .all()
        )

        # Média de compras por cliente
        media_compras = (
            db.query(
                func.count(Transaction.NumeroFatura) / 
                func.count(distinct(Transaction.IDCliente))
            )
            .scalar()
        )

        return AnaliseClientesResponse(
            status="success",
            top_clientes=[
                ClienteAnalise(
                    id_cliente=c.IDCliente,
                    total_compras=float(c.total_compras),
                    frequencia_compras=c.frequencia_compras,
                    ticket_medio=float(c.total_compras/c.frequencia_compras),
                    pais=c.pais
                ) for c in top_clientes
            ],
            distribuicao_por_pais=dist_pais,
            media_compras_por_cliente=float(media_compras)
        )
    except Exception as e:
        return AnaliseClientesResponse(status="error", top_clientes=[], distribuicao_por_pais={}, media_compras_por_cliente=0)

@router.get("/analise/faturamento", response_model=AnaliseFaturamentoResponse)
def get_analise_faturamento(db: Session = Depends(get_db)):
    try:
        # Média diária de faturamento
        media_diaria = (
            db.query(func.avg(Transaction.ValorTotalFatura))
            .scalar()
        )

        # Proporção de faturas únicas
        total_faturas = db.query(func.count(Transaction.NumeroFatura)).scalar()
        faturas_unicas = (
            db.query(func.count(Transaction.NumeroFatura))
            .filter(Transaction.FaturaUnica == True)
            .scalar()
        )
        proporcao = faturas_unicas / total_faturas if total_faturas > 0 else 0

        # Evolução temporal
        evolucao = (
            db.query(
                Transaction.DataFatura,
                func.sum(Transaction.ValorTotalFatura).label('valor_total'),
                func.count(Transaction.NumeroFatura).label('quantidade_faturas')
            )
            .group_by(Transaction.DataFatura)
            .order_by(Transaction.DataFatura)
            .all()
        )

        return AnaliseFaturamentoResponse(
            status="success",
            media_diaria=float(media_diaria),
            proporcao_faturas_unicas=float(proporcao),
            evolucao_temporal=[
                FaturamentoDiario(
                    data=e.DataFatura,
                    valor_total=float(e.valor_total),
                    quantidade_faturas=e.quantidade_faturas,
                    ticket_medio=float(e.valor_total/e.quantidade_faturas)
                ) for e in evolucao
            ]
        )
    except Exception as e:
        return AnaliseFaturamentoResponse(status="error", media_diaria=0, proporcao_faturas_unicas=0, evolucao_temporal=[])
