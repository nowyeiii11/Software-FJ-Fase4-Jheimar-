# Software FJ - Gestión de clientes, servicios y reservas

Proyecto en Python (solo biblioteca estándar, sin base de datos) que gestiona
clientes, servicios y reservas aplicando abstracción, herencia, polimorfismo,
encapsulación y manejo avanzado de excepciones.

## Cómo ejecutarlo

```
python main.py
```

Corre 29 operaciones (válidas e inválidas). Los errores se muestran en pantalla
y se guardan en `eventos.log`; el programa nunca se detiene.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (todas heredan de `ErrorFJ`) |
| `validaciones.py` | Validaciones reutilizables (texto, patrones, números) |
| `entidades.py` | Clase abstracta `Entidad` y clase `Cliente` |
| `servicios.py` | Clase abstracta `Servicio` y `SalaReunion`, `AlquilerEquipo`, `Asesoria` |
| `reservas.py` | `Reserva` y `EstadoReserva` (confirmar, cancelar, procesar) |
| `gestor.py` | `GestorFJ`: listas internas y ejecución segura de operaciones |
| `registro.py` | Configuración del archivo de logs |
| `main.py` | Simulación de las 29 operaciones |

## Dónde está cada requisito

- **Clase abstracta general:** `Entidad` (`entidades.py`)
- **Cliente con validaciones y encapsulación:** `Cliente` (propiedades y setters validados)
- **Servicio abstracto + 3 hijos:** `Servicio` y sus tres clases hijas
- **Polimorfismo:** `describir()`, `calcular_costo_base()` y `validar_parametros()` cambian en cada servicio
- **Sobrecarga (parámetros opcionales):** `Servicio.calcular_costo(duracion, impuesto, descuento, cupon)`
- **try/except/else/finally:** `Reserva.procesar()` y `GestorFJ.ejecutar_operacion()`
- **Encadenamiento de excepciones (`raise ... from`):** `Cliente.__init__` y `Reserva.procesar()`
- **Archivo de logs:** `eventos.log`
