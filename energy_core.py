# energy_core.py
def format_number(value: float) -> str:
    superscripts = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    if value == 0:
        return "0"
    abs_val = abs(value)
    if 1e-3 <= abs_val <= 1e5:
        return f"{value:.5g}"
    else:
        formatted = f"{value:.4e}"
        base, exp = formatted.split("e")
        exp = int(exp)
        return f"{base} × 10{str(exp).translate(superscripts)}"

def energy_converter(value, unit):
    unit_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: 1239.8420 / x,
        'cm-1': lambda x: x * 1239.8420e-7,
        'THz': lambda x: x / 241.7989,
        'ps': lambda x: 4.135668e-3/x,
        'fs': lambda x: 4.135668/x,
        'K': lambda x: 8.61733e-5*x,
        'J': lambda x: x/1.60218e-19,
        'kJ': lambda x: x/1.60218e-22,
        'kcal/mol': lambda x: x * 0.0433634, # 1 kcal/mol = 0.0433634 eV
        'kJ/mol':   lambda x: x * 0.0103643, # 1 kJ/mol   = 0.0103643 eV
    }
    ir_unit_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: 1239.8420 / x,
        'cm-1': lambda x: x / 1239.8420e-7,
        'THz': lambda x: x * 241.7989,
        'ps': lambda x: 4.135668e-3/x,
        'fs': lambda x: 4.135668/x,
        'K': lambda x: x/8.61733e-5,
        'J': lambda x: x*1.60218e-19,
        'kJ': lambda x: x*1.60218e-22,
        'kcal/mol': lambda x: x / 0.0433634,
        'kJ/mol':   lambda x: x / 0.0103643,
    }
    symbol = {
        'eV': 'E', 
        'nm': 'λ', 
        'cm-1': 'ν', 
        'THz': 'f',
        'ps': 'T', 
        'fs': 'T', 
        'K': 'Temp', 
        'J': 'E', 
        'kJ': 'E',
        'kcal/mol': 'E',
        'kJ/mol': 'E',
    }

    if unit not in unit_conversions:
        return []

    results = []
    E = unit_conversions[unit](value)
    for u in ir_unit_conversions:
        val = ir_unit_conversions[u](E)
        results.append((symbol[u], format_number(val), u))
    return results
