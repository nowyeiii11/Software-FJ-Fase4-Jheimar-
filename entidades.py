"""Clase abstracta Entidad y la clase Cliente."""

from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError, DatosInvalidosError
from validaciones import validar_patron


class Entidad(ABC):
    """Molde general: todo lo que maneja el sistema (clientes, servicios, reservas)
    tiene un id propio y sabe describirse. Es abstracta, no se puede instanciar."""

    PREFIJO = "ENT"        # cada hija pone el suyo: CLI, SRV, RES
    _consecutivos = {}     # lleva la cuenta de ids por prefijo

    def __init__(self):
        siguiente = Entidad._consecutivos.get(self.PREFIJO, 0) + 1
        Entidad._consecutivos[self.PREFIJO] = siguiente
        self._id = f"{self.PREFIJO}-{siguiente:03d}"  # ej: CLI-001

    @property
    def id(self):
        """Solo lectura: el id no se puede cambiar desde afuera."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada hija devuelve su propio texto descriptivo."""

    def __str__(self):
        return self.describir()


class Cliente(Entidad):
    """Persona que hace reservas. Sus datos son privados y se validan siempre."""

    PREFIJO = "CLI"
    # formatos aceptados
    PATRON_NOMBRE = r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]{3,60}"
    PATRON_DOCUMENTO = r"\d{6,10}"
    PATRON_CORREO = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"
    PATRON_TELEFONO = r"3\d{9}"  # celular colombiano: 10 digitos que empiezan por 3

    def __init__(self, nombre, documento, correo, telefono):
        try:
            self._nombre = validar_patron(
                nombre, "El nombre", self.PATRON_NOMBRE,
                "solo letras y espacios, de 3 a 60 caracteres")
            self._documento = validar_patron(
                documento, "El documento", self.PATRON_DOCUMENTO,
                "solo dígitos, de 6 a 10")
            self._correo = validar_patron(
                correo, "El correo", self.PATRON_CORREO,
                "debe tener la forma usuario@dominio.com")
            self._telefono = validar_patron(
                telefono, "El teléfono", self.PATRON_TELEFONO,
                "celular de 10 dígitos que empieza por 3")
        except DatosInvalidosError as causa:
            # ENCADENAMIENTO: lanzo un error mas claro y guardo el original con "from"
            raise ClienteInvalidoError(
                "No se pudo crear el cliente.") from causa
        super().__init__()  # el id se asigna solo si todo estuvo bien

    # --- encapsulacion: lectura por propiedades, escritura validada ---
    @property
    def nombre(self):
        return self._nombre

    @property
    def documento(self):
        return self._documento

    @property
    def documento_enmascarado(self):
        """Muestra solo los ultimos 3 digitos para no exponer el documento."""
        return "*" * (len(self._documento) - 3) + self._documento[-3:]

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, nuevo):
        self._correo = validar_patron(
            nuevo, "El correo", self.PATRON_CORREO,
            "debe tener la forma usuario@dominio.com")

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo):
        self._telefono = validar_patron(
            nuevo, "El teléfono", self.PATRON_TELEFONO,
            "celular de 10 dígitos que empieza por 3")

    def describir(self):
        return (f"Cliente {self.id}: {self._nombre} "
                f"(doc. {self.documento_enmascarado}, {self._correo})")
