"""Validaciones reutilizables. Todas lanzan DatosInvalidosError si algo falla."""

import math
import re

from excepciones import DatosInvalidosError, ParametroFaltanteError


def exigir_valor(valor, nombre):
    """Falla si el dato no llego (None) o es un texto vacio."""
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        raise ParametroFaltanteError(f"Falta el dato obligatorio: {nombre}.")
    return valor


def validar_texto(valor, nombre, minimo=3):
    """Revisa que sea texto con un minimo de letras y limpia espacios de sobra."""
    exigir_valor(valor, nombre)
    if not isinstance(valor, str):
        raise DatosInvalidosError(f"{nombre} debe ser texto.")
    limpio = " ".join(valor.split())  # "  Ana   Gomez " -> "Ana Gomez"
    if len(limpio) < minimo:
        raise DatosInvalidosError(f"{nombre} debe tener al menos {minimo} caracteres.")
    return limpio


def validar_patron(valor, nombre, patron, ayuda):
    """Revisa que el texto cumpla una expresion regular (formato)."""
    exigir_valor(valor, nombre)
    if not isinstance(valor, str):
        raise DatosInvalidosError(f"{nombre} debe ser texto.")
    limpio = valor.strip()
    if not re.fullmatch(patron, limpio):
        raise DatosInvalidosError(f"{nombre} no es válido: {ayuda}.")
    return limpio


def validar_numero(valor, nombre, minimo=None, maximo=None,
                   incluye_minimo=True, entero=False):
    """Revisa que sea un numero real (no texto, no bool, no NaN) dentro del rango."""
    exigir_valor(valor, nombre)
    # en Python True y False cuentan como int, por eso los rechazo aparte
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise DatosInvalidosError(f"{nombre} debe ser un número.")
    if math.isnan(valor) or math.isinf(valor):
        raise DatosInvalidosError(f"{nombre} no puede ser NaN ni infinito.")
    if entero and not float(valor).is_integer():
        raise DatosInvalidosError(f"{nombre} debe ser un número entero.")
    if minimo is not None:
        if valor < minimo or (not incluye_minimo and valor == minimo):
            raise DatosInvalidosError(f"{nombre} debe ser mayor{'' if not incluye_minimo else ' o igual'} a {minimo}.")
    if maximo is not None and valor > maximo:
        raise DatosInvalidosError(f"{nombre} no puede ser mayor a {maximo}.")
    return valor
