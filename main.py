"""Software FJ - simulacion de 29 operaciones (validas e invalidas).

Ejecutar con:  python main.py
Los errores se muestran en pantalla y se guardan en eventos.log
"""

from gestor import GestorFJ
from registro import configurar_log
from servicios import Asesoria, AlquilerEquipo, SalaReunion, Servicio


def main():
    logger = configurar_log()
    logger.info("=== Inicio de la simulación ===")
    g = GestorFJ()
    op = g.ejecutar_operacion  # atajo para escribir menos

    print("=" * 60)
    print("SOFTWARE FJ - Gestión de clientes, servicios y reservas")
    print("=" * 60)

    # ---------- CLIENTES ----------
    ana = op("Registrar cliente válido (Ana)", g.registrar_cliente,
             nombre="Ana María Gómez", documento="1032456789",
             correo="ana.gomez@correo.com", telefono="3101234567")
    luis = op("Registrar cliente válido (Luis)", g.registrar_cliente,
              nombre="Luis Fernando Rojas", documento="79123456",
              correo="luis.rojas@correo.com", telefono="3209876543")
    op("Registrar cliente con correo inválido", g.registrar_cliente,
       nombre="Pedro Ruiz", documento="80111222",
       correo="pedro-sin-arroba", telefono="3001112233")
    op("Registrar cliente con documento con letras", g.registrar_cliente,
       nombre="Marta Díaz", documento="12A456",
       correo="marta@correo.com", telefono="3004445566")
    op("Registrar cliente sin teléfono (parámetro faltante)", g.registrar_cliente,
       nombre="Laura Pérez", documento="52123456", correo="laura@correo.com")
    op("Registrar cliente con documento repetido", g.registrar_cliente,
       nombre="Ana Duplicada", documento="1032456789",
       correo="otra@correo.com", telefono="3112223344")

    # ---------- SERVICIOS ----------
    sala = op("Crear sala de reuniones válida", g.crear_servicio,
              SalaReunion, "Sala Innovación", 80000, 10)
    equipo = op("Crear alquiler de equipo válido", g.crear_servicio,
                AlquilerEquipo, "Portátil Workstation", 45000, 100000)
    asesoria = op("Crear asesoría senior válida", g.crear_servicio,
                  Asesoria, "Asesoría en Python", 120000, "Python", "senior")
    op("Crear sala con tarifa negativa", g.crear_servicio,
       SalaReunion, "Sala Rota", -5000, 6)
    op("Crear asesoría con nivel inexistente", g.crear_servicio,
       Asesoria, "Asesoría X", 90000, "Redes", "experto")
    op("Intentar crear un Servicio abstracto directamente", g.crear_servicio,
       Servicio, "Servicio genérico", 1000)

    # ---------- RESERVAS ----------
    r1 = op("Crear reserva válida (Ana, sala, 2 h)", g.crear_reserva,
            ana.id, sala.id, 2)
    op("Crear reserva con duración fuera de rango (sala 12 h)", g.crear_reserva,
       ana.id, sala.id, 12)
    op("Crear reserva con cliente inexistente", g.crear_reserva,
       "CLI-999", sala.id, 2)
    op("Crear reserva con duración en texto", g.crear_reserva,
       luis.id, equipo.id, "dos")

    op("Confirmar la reserva de Ana", g.confirmar_reserva, r1.id)
    op("Procesar con IVA 19% y cupón FJ10", g.procesar_reserva,
       r1.id, impuesto=0.19, cupon="FJ10")
    op("Procesar de nuevo una reserva ya procesada", g.procesar_reserva,
       r1.id, impuesto=0.19)
    op("Cancelar una reserva ya procesada", g.cancelar_reserva, r1.id)

    r2 = op("Crear reserva de equipo (Luis, 3 días)", g.crear_reserva,
            luis.id, equipo.id, 3)
    op("Marcar el equipo como no disponible", g.cambiar_disponibilidad,
       equipo.id, False)
    op("Confirmar reserva de un servicio no disponible", g.confirmar_reserva, r2.id)
    op("Cancelar la reserva pendiente de Luis", g.cancelar_reserva, r2.id)

    r3 = op("Crear reserva de asesoría (Luis, 1.5 h)", g.crear_reserva,
            luis.id, asesoria.id, 1.5)
    op("Confirmar la asesoría", g.confirmar_reserva, r3.id)
    op("Procesar con un cupón que no existe", g.procesar_reserva,
       r3.id, impuesto=0.19, cupon="REGALADO")
    op("Procesar con descuento del 100% (cálculo inconsistente)",
       g.procesar_reserva, r3.id, descuento=1.0)
    op("Procesar la asesoría con IVA y descuento del 10%", g.procesar_reserva,
       r3.id, impuesto=0.19, descuento=0.10)

    g.resumen()
    logger.info("=== Fin de la simulación: el programa siguió activo ===")
    print("\nEl programa terminó sin caerse. Revisa el archivo eventos.log")


if __name__ == "__main__":
    main()
