import locale

def setup_locale():
    """Configura o locale para português do Brasil"""
    locales_to_try = ['pt_BR.UTF-8', 'pt_BR.utf8', 'portuguese_brazil', 'pt_BR', 'Portuguese_Brazil.1252']
    
    for loc in locales_to_try:
        try:
            locale.setlocale(locale.LC_ALL, loc)
            return
        except locale.Error:
            continue
    
    # Se nenhum locale específico funcionar, usa o padrão do sistema
    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error:
        pass  # Mantém o locale padrão se nada funcionar

def format_brl(value):
    """Formata um valor para o formato monetário brasileiro"""
    try:
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def format_number(value):
    """Formata um número com separadores de milhar no formato brasileiro"""
    try:
        return f"{value:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"
