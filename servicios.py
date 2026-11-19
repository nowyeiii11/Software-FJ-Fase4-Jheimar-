"""Clase abstracta Servicio y los tres servicios especializados."""

from abc import abstractmethod

from entidades import Entidad
from excepciones import (CalculoInconsistenteError, DatosInvalidosError,
                         ServicioNoDisponibleError)
from utilidades import formato_moneda
from validaciones import validar_numero, validar_texto

# cupones de descuento que acepta el sistema
CUPONES = {"FJ10": 0.10, "ESTUDIANTE": 0.15, "FJ20": 0.20}


class Servicio(Entidad):
    """Molde de todo servicio que ofrece Software FJ. Es abstracta: lo que cambia
    de un servicio a otro (costo base y reglas de duracion) lo define cada hija."""

    PREFIJO = "SRV"
    UNIDAD = "horas"  # cada hija puede cambiarla

    def __init__(self, nombre, tarifa_base):
        # valido primero, asi si algo falla no se gasta un id
        nombre_ok = validar_texto(nombre, "El nombre del servicio")
        tarifa_ok = validar_numero(tarifa_base, "La tarifa", minimo=0,
                                   incluye_minimo=False)
        super().__init__()
        self._nombre = nombre_ok
        self._tarifa_base = tarifa_ok
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise DatosInvalidosError("La disponibilidad debe ser True o False.")
        self._disponible = valor

    # --- lo que cada servicio debe implementar a su manera (polimorfismo) ---
    @abstractmethod
    def calcular_costo_base(self, duracion):
        """Costo sin impuestos ni descuentos, segun la regla de cada servicio."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Revisa que la duracion sirva para este servicio; si no, lanza error."""

    def validar_disponibilidad(self):
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._nombre} no está disponible por ahora.")

    # --- SOBRECARGA simulada con parametros opcionales ---
    # calcular_costo(2)                        -> solo el costo base
    # calcular_costo(2, 0.19)                  -> con impuesto
    # calcular_costo(2, 0.19, 0.10)            -> con impuesto y descuento
    # calcular_costo(2, cupon="FJ10")          -> con un cupon
    def calcular_costo(self, duracion, impuesto=0.0, descuento=0.0, cupon=None):
        self.validar_parametros(duracion)
        validar_numero(impuesto, "El impuesto", minimo=0, maximo=0.30)
        validar_numero(descuento, "El descuento", minimo=0, maximo=1)

        if cupon is not None:
            codigo = str(cupon).strip().upper()
            if codigo not in CUPONES:
                raise DatosInvalidosError(f"El cupón '{cupon}' no existe.")
            # si hay cupon y descuento a la vez, se aplica el mayor (no se suman)
            descuento = max(descuento, CUPONES[codigo])

        subtotal = self.calcular_costo_base(duracion)
        total = subtotal * (1 - descuento) * (1 + impuesto)

        # guardia contra resultados que no tienen sentido
        if total <= 0:
            raise CalculoInconsistenteError(
                f"El total calculado ({total}) debe ser mayor a cero.")
        return round(total, 2)


class SalaReunion(Servicio):
    """Reserva de salas: se cobra por hora, entre 1 y 8 horas."""

    def __init__(self, nombre, tarifa_hora, capacidad):
        validar_numero(capacidad, "La capacidad", minimo=1, maximo=50, entero=True)
        super().__init__(nombre, tarifa_hora)
        self._capacidad = int(capacidad)

    def validar_parametros(self, duracion):
        validar_numero(duracion, "La duración", minimo=1, maximo=8)
        if (duracion * 2) % 1 != 0:  # solo se permiten medias horas
            raise DatosInvalidosError(
                "La duración de la sala debe ir en pasos de media hora.")

    def calcular_costo_base(self, duracion):
        return self._tarifa_base * duracion

    def describir(self):
        return (f"Sala {self.id} '{self._nombre}' para {self._capacidad} personas, "
                f"{formato_moneda(self._tarifa_base)} por hora")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por dia (1 a 30) mas un deposito fijo."""

    UNIDAD = "días"

    def __init__(self, nombre, tarifa_dia, deposito=0):
        validar_numero(deposito, "El depósito", minimo=0)
        super().__init__(nombre, tarifa_dia)
        self._deposito = deposito

    def validar_parametros(self, duracion):
        validar_numero(duracion, "La duración", minimo=1, maximo=30, entero=True)

    def calcular_costo_base(self, duracion):
        return self._tarifa_base * duracion + self._deposito

    def describir(self):
        return (f"Equipo {self.id} '{self._nombre}', "
                f"{formato_moneda(self._tarifa_base)} por día "
                f"+ depósito {formato_moneda(self._deposito)}")


class Asesoria(Servicio):
    """Asesoria especializada: por hora (0.5 a 4), con recargo si es senior."""

    FACTORES_NIVEL = {"junior": 1.0, "senior": 1.25}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):
        especialidad_ok = validar_texto(especialidad, "La especialidad")
        nivel_ok = str(nivel).strip().lower()
        if nivel_ok not in self.FACTORES_NIVEL:
            raise DatosInvalidosError("El nivel debe ser 'junior' o 'senior'.")
        super().__init__(nombre, tarifa_hora)
        self._especialidad = especialidad_ok
        self._nivel = nivel_ok

    def validar_parametros(self, duracion):
        validar_numero(duracion, "La duración", minimo=0.5, maximo=4)
        if (duracion * 2) % 1 != 0:
            raise DatosInvalidosError(
                "La duración de la asesoría debe ir en pasos de media hora.")

    def calcular_costo_base(self, duracion):
        return self._tarifa_base * duracion * self.FACTORES_NIVEL[self._nivel]

    def describir(self):
        return (f"Asesoría {self.id} '{self._nombre}' de {self._especialidad} "
                f"(nivel {self._nivel}), {formato_moneda(self._tarifa_base)} por hora")
