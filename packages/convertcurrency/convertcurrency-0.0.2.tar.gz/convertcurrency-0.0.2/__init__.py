from forex_python.converter import CurrencyRates

def convert_currency(amount, from_currency, to_currency):
    
    c = CurrencyRates()
    exchange_rate = c.get_rate(from_currency, to_currency)
    converted_amount = amount * exchange_rate
    return converted_amount
