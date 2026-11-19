"""Funciones pequenas de ayuda."""


def formato_moneda(valor):
    """Devuelve el valor como pesos colombianos: 1234567.5 -> $1.234.567,50"""
    texto = f"{valor:,.2f}"  # primero queda 1,234,567.50 (estilo ingles)
    # cambio comas por puntos y viceversa, usando "_" como paso intermedio
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"${texto}"
