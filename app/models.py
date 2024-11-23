from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, BigInteger, Numeric, Text
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions_sample"

    created_at = Column(DateTime(timezone=True))
    NumeroFatura = Column(String, primary_key=True)
    CodigoProduto = Column(String)
    Descricao = Column(Text)
    Quantidade = Column(BigInteger)
    DataFatura = Column(DateTime)
    PrecoUnitario = Column(Numeric)
    IDCliente = Column(String)
    Pais = Column(String)
    CategoriaProduto = Column(String)
    CategoriaPreco = Column(String)
    ValorTotalFatura = Column(Numeric)
    FaturaUnica = Column(Boolean)
    Ano = Column(BigInteger)
    Mes = Column(BigInteger)
    Dia = Column(BigInteger)
    DiaSemana = Column(BigInteger)
    SemanaAno = Column(BigInteger)
