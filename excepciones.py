"""Excepciones personalizadas de Software FJ.

Todas heredan de ErrorFJ. Asi, en un solo "except ErrorFJ" se atrapan los
errores propios del sistema, sin mezclarlos con los errores de Python.
"""


class ErrorFJ(Exception):
    """Error base del sistema: de aqui salen todos los demas."""


class DatosInvalidosError(ErrorFJ):
    """Un dato llego con tipo, formato o valor incorrecto."""


class ParametroFaltanteError(DatosInvalidosError):
    """Falta un dato obligatorio (llego vacio o como None)."""


class ClienteInvalidoError(ErrorFJ):
    """No se pudo crear o registrar un cliente."""


class ServicioNoDisponibleError(ErrorFJ):
    """El servicio existe, pero en este momento no se puede reservar."""


class ReservaInvalidaError(ErrorFJ):
    """Intento de reserva incorrecto u operacion no permitida por el estado."""


class CalculoInconsistenteError(ErrorFJ):
    """El calculo de un costo dio un resultado que no tiene sentido."""


class ProcesamientoError(ErrorFJ):
    """Fallo al procesar una reserva (guarda la causa original encadenada)."""
