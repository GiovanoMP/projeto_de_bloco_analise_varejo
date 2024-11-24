# utils/helpers.py
from typing import Union
import locale
from datetime import datetime

# Configurar locale para formatação de moeda em PT-BR
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_currency(value: float) -> str:
    """
    Formata valores monetários para o padrão brasileiro
    Exemplo: R$ 1.234,56
    """
    return locale.currency(value, grouping=True, symbol='R$')

def calculate_growth(old_value: float, new_value: float) -> float:
    """
    Calcula taxa de crescimento entre dois valores
    Retorna a porcentagem de crescimento
    """
    if old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def format_large_number(value: Union[int, float]) -> str:
    """
    Formata números grandes de forma mais legível
    Exemplo: 1000000 -> 1M, 1500 -> 1.5K
    """
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:.0f}"

def get_period_label(date: datetime) -> str:
    """
    Retorna label formatado para período
    Exemplo: Janeiro/2024
    """
    return date.strftime("%B/%Y")

# Exemplo de uso:
# valor_formatado = format_currency(1234.56)  # R$ 1.234,56
# crescimento = calculate_growth(100, 150)    # 50.0
# numero_formatado = format_large_number(1500000)  # 1.5M
