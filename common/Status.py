from enum import Enum


class Status(Enum):
    RESTING = 0                 # Reposo
    FINDING_TARGET = 1          # Buscando target (base)
    TARGET_FOUND = 2            # Target encontrado
    ALIGNING_TO_TARGET = 3      # Alineandose con el target (base)
    READY_TO_GO = 4             # Listo para moverse - ya estoy alineado con el target
    NAVIGATING = 5              # Moviendome al target
    NAVIGATION_COMPLETED = 6    # Target alcanzado (exijo que suban las notas)