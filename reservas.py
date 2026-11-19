"""Clase Reserva: une un cliente con un servicio y controla su estado."""

import logging
from enum import Enum

from entidades import Cliente, Entidad
from excepciones import (ErrorFJ, ProcesamientoError, ReservaInvalidaError)
from servicios import Servicio
from utilidades import formato_moneda

logger = logging.getLogger("software_fj")


class EstadoReserva(Enum):
    """Los unicos estados posibles. Con Enum no se puede escribir uno mal."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"


class Reserva(Entidad):
    PREFIJO = "RES"

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        servicio.validar_parametros(duracion)  # si la duracion no sirve, falla aqui
        super().__init__()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = EstadoReserva.PENDIENTE  # toda reserva nace pendiente
        self._costo_final = None

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA, solo si el servicio esta disponible."""
        if self._estado != EstadoReserva.PENDIENTE:
            raise ReservaInvalidaError(
                f"{self.id} está {self._estado.value}: solo se confirman reservas pendientes.")
        self._servicio.validar_disponibilidad()
        self._estado = EstadoReserva.CONFIRMADA
        logger.info("Reserva %s confirmada.", self.id)

    def cancelar(self):
        """Se puede cancelar si esta PENDIENTE o CONFIRMADA (no si ya se cobro)."""
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise ReservaInvalidaError(
                f"{self.id} está {self._estado.value} y ya no se puede cancelar.")
        self._estado = EstadoReserva.CANCELADA
        logger.info("Reserva %s cancelada.", self.id)

    def procesar(self, impuesto=0.0, descuento=0.0, cupon=None):
        """CONFIRMADA -> PROCESADA: calcula el costo final y lo deja guardado."""
        try:
            # 1) si algo sale mal en este bloque, salta al except
            if self._estado != EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaError(
                    f"{self.id} está {self._estado.value}: solo se procesan reservas confirmadas.")
            costo = self._servicio.calcular_costo(
                self._duracion, impuesto, descuento, cupon)
        except ErrorFJ as causa:
            # 2) cualquier error del sistema se anota y se relanza con mas contexto
            logger.error("Fallo al procesar %s: %s", self.id, causa)
            raise ProcesamientoError(
                f"No se pudo procesar la reserva {self.id}.") from causa
        else:
            # 3) el else corre SOLO si el try termino sin errores
            self._costo_final = costo
            self._estado = EstadoReserva.PROCESADA
            logger.info("Reserva %s procesada por %s.", self.id, formato_moneda(costo))
            return costo
        finally:
            # 4) el finally corre SIEMPRE, haya salido bien o mal
            logger.debug("Terminó el intento de procesar %s.", self.id)

    def describir(self):
        costo = formato_moneda(self._costo_final) if self._costo_final else "sin cobrar"
        return (f"Reserva {self.id}: {self._cliente.nombre} → {self._servicio.nombre} "
                f"x {self._duracion} {self._servicio.UNIDAD} "
                f"[{self._estado.value}] ({costo})")
