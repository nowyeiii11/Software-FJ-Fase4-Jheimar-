"""GestorFJ: guarda las listas de clientes, servicios y reservas y ejecuta
operaciones de forma segura (si algo falla, lo anota y el programa sigue)."""

import logging

from entidades import Cliente
from excepciones import ClienteInvalidoError, ErrorFJ, ReservaInvalidaError
from reservas import Reserva
from servicios import Servicio
from utilidades import formato_moneda
from validaciones import exigir_valor, validar_numero

logger = logging.getLogger("software_fj")


class GestorFJ:
    def __init__(self):
        # sin base de datos: todo vive en listas dentro de este objeto
        self._clientes = []
        self._servicios = []
        self._reservas = []
        self._operaciones = 0
        self._exitosas = 0
        self._fallidas = 0

    # ---------- busqueda ----------
    @staticmethod
    def _buscar(lista, identificador, etiqueta):
        exigir_valor(identificador, f"el id de {etiqueta}")
        for elemento in lista:
            if elemento.id == identificador:
                return elemento
        raise ReservaInvalidaError(f"No existe {etiqueta} con id {identificador}.")

    # ---------- registros ----------
    def registrar_cliente(self, nombre=None, documento=None, correo=None, telefono=None):
        # los None por defecto hacen que un dato faltante dispare ParametroFaltanteError
        cliente = Cliente(nombre, documento, correo, telefono)
        if any(c.documento == cliente.documento for c in self._clientes):
            raise ClienteInvalidoError("Ya existe un cliente con ese documento.")
        self._clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.id)
        return cliente

    def crear_servicio(self, clase, *args, **kwargs):
        """Crea el servicio con la clase indicada y lo guarda en la lista."""
        servicio = clase(*args, **kwargs)  # una clase abstracta fallaria aqui
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Solo se pueden registrar servicios.")
        self._servicios.append(servicio)
        logger.info("Servicio creado: %s", servicio.id)
        return servicio

    def cambiar_disponibilidad(self, id_servicio, disponible):
        servicio = self._buscar(self._servicios, id_servicio, "un servicio")
        servicio.disponible = disponible
        logger.info("Servicio %s disponible=%s", servicio.id, disponible)
        return servicio

    def crear_reserva(self, id_cliente=None, id_servicio=None, duracion=None):
        cliente = self._buscar(self._clientes, id_cliente, "un cliente")
        servicio = self._buscar(self._servicios, id_servicio, "un servicio")
        validar_numero(duracion, "La duración", minimo=0, incluye_minimo=False)
        reserva = Reserva(cliente, servicio, duracion)
        self._reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.id)
        return reserva

    def confirmar_reserva(self, id_reserva):
        reserva = self._buscar(self._reservas, id_reserva, "una reserva")
        reserva.confirmar()
        return reserva

    def cancelar_reserva(self, id_reserva):
        reserva = self._buscar(self._reservas, id_reserva, "una reserva")
        reserva.cancelar()
        return reserva

    def procesar_reserva(self, id_reserva, impuesto=0.0, descuento=0.0, cupon=None):
        reserva = self._buscar(self._reservas, id_reserva, "una reserva")
        return reserva.procesar(impuesto, descuento, cupon)

    # ---------- ejecucion segura ----------
    def ejecutar_operacion(self, descripcion, funcion, *args, **kwargs):
        """Corre una operacion y NUNCA deja que el programa se caiga."""
        self._operaciones += 1
        print(f"\n[{self._operaciones:02d}] {descripcion}")
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorFJ as error:
            # error esperado, propio del sistema
            self._fallidas += 1
            logger.error("Operación %02d falló: %s", self._operaciones, error)
            print(f"     ERROR controlado: {error}")
            if error.__cause__ is not None:  # muestra la causa encadenada
                print(f"     Causa original:   {error.__cause__}")
            return None
        except Exception as error:
            # cualquier otro error inesperado de Python tambien se atrapa
            self._fallidas += 1
            logger.exception("Operación %02d: error inesperado", self._operaciones)
            print(f"     ERROR inesperado ({type(error).__name__}): {error}")
            return None
        else:
            self._exitosas += 1
            logger.info("Operación %02d exitosa.", self._operaciones)
            if isinstance(resultado, float):
                print(f"     OK: total {formato_moneda(resultado)}")
            else:
                print(f"     OK: {resultado}")
            return resultado
        finally:
            logger.debug("Fin de la operación %02d.", self._operaciones)

    def resumen(self):
        print("\n" + "=" * 60)
        print("RESUMEN FINAL")
        print("=" * 60)
        print(f"Operaciones: {self._operaciones} "
              f"(exitosas: {self._exitosas}, con error controlado: {self._fallidas})")
        print(f"Clientes: {len(self._clientes)} | Servicios: {len(self._servicios)} "
              f"| Reservas: {len(self._reservas)}")
        for reserva in self._reservas:
            print("  -", reserva.describir())
