from enum import Enum


class Status(Enum):
    INITIALIZING = 0            # Cargando configuración y calibración e inicializando cámara
    FINDING_TARGET = 1          # Buscando target
    TARGET_FOUND = 2            # Target encontrado
    TARGET_LOST = 3             # Objetivo perdido
    ALIGNING_TO_TARGET = 3      # Alineandose con el target
    ALIGNED_TO_TARGET = 4       # Listo para moverse - ya estoy alineado con el target
    MOVING_TOWARDS_TARGET = 5   # Moviendome al target
    TARGET_REACHED = 6          # Target alcanzado