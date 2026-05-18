# energy_core.py
import math


EV_PER_NM = 1239.8420
EV_PER_CM = EV_PER_NM * 1e-7
THZ_PER_EV = 241.7989
H_EV_FS = 4.135668
KB_EV_PER_K = 8.61733e-5
EV_PER_J = 1 / 1.60218e-19
EV_PER_KJ = 1 / 1.60218e-22
TWOPI = 2 * math.pi


def format_number(value: float) -> str:
    superscripts = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
    if value == 0:
        return "0"

    abs_val = abs(value)
    if 1e-3 <= abs_val <= 1e5:
        return f"{value:.5g}"

    formatted = f"{value:.4e}"
    base, exp = formatted.split("e")
    exp = int(exp)
    return f"{base} × 10{str(exp).translate(superscripts)}"


def energy_converter(value, unit):
    unit_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: EV_PER_NM / x,
        'cm-1': lambda x: x * EV_PER_CM,
        'THz': lambda x: x / THZ_PER_EV,
        'ps(period)': lambda x: H_EV_FS * 1e-3 / x,
        'fs(period)': lambda x: H_EV_FS / x,
        'ps(tau)': lambda x: H_EV_FS * 1e-3 / (TWOPI * x),
        'fs(tau)': lambda x: H_EV_FS / (TWOPI * x),
        'K': lambda x: KB_EV_PER_K * x,
        'J': lambda x: x * EV_PER_J,
        'kJ': lambda x: x * EV_PER_KJ,
        'kcal/mol': lambda x: x * 0.0433634,
        'kJ/mol': lambda x: x * 0.0103643,
    }
    inverse_conversions = {
        'eV': lambda x: x,
        'nm': lambda x: EV_PER_NM / x,
        'cm-1': lambda x: x / EV_PER_CM,
        'THz': lambda x: x * THZ_PER_EV,
        'ps(period)': lambda x: H_EV_FS * 1e-3 / x,
        'fs(period)': lambda x: H_EV_FS / x,
        'ps(tau)': lambda x: H_EV_FS * 1e-3 / (TWOPI * x),
        'fs(tau)': lambda x: H_EV_FS / (TWOPI * x),
        'K': lambda x: x / KB_EV_PER_K,
        'J': lambda x: x / EV_PER_J,
        'kJ': lambda x: x / EV_PER_KJ,
        'kcal/mol': lambda x: x / 0.0433634,
        'kJ/mol': lambda x: x / 0.0103643,
    }
    symbol = {
        'eV': 'E',
        'nm': 'λ',
        'cm-1': 'ν̃',
        'THz': 'ν',
        'ps(period)': 'T',
        'fs(period)': 'T',
        'ps(tau)': 'τ',
        'fs(tau)': 'τ',
        'K': 'θ',
        'J': 'E',
        'kJ': 'E',
        'kcal/mol': 'E',
        'kJ/mol': 'E',
    }

    if unit not in unit_conversions:
        return []

    results = []
    energy_ev = unit_conversions[unit](value)
    for u in inverse_conversions:
        val = inverse_conversions[u](energy_ev)
        results.append((symbol[u], format_number(val), u))
    return results
