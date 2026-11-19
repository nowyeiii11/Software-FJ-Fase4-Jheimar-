"""Configuracion del archivo de logs (registro de eventos y errores)."""

import logging
from pathlib import Path

NOMBRE_LOGGER = "software_fj"


def configurar_log(nombre_archivo="eventos.log"):
    """Crea el logger que escribe en un archivo junto a este programa."""
    logger = logging.getLogger(NOMBRE_LOGGER)

    # si ya estaba configurado no le agrego otro manejador (saldrian lineas repetidas)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    ruta = Path(__file__).parent / nombre_archivo
    # mode="w": cada ejecucion empieza con un log limpio (asi la evidencia es de esa corrida)
    manejador = logging.FileHandler(ruta, mode="w", encoding="utf-8")
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    )
    logger.addHandler(manejador)
    return logger
