from Hodor import Hodor
from common.CalibrationType import CalibrationType
from settings.HodorSettings import HodorSettings

hodor_settings = HodorSettings()
hodor_settings.read_from_file("settings.json")

hodor = Hodor(hodor_settings, CalibrationType.LOAD)

try:
    # Detener los motores
    hodor.motor_control.stop()

    # Configuración inicial
    hodor.setup()

    # Bucle principal
    hodor.loop()

finally:
    # Detener los motores
    hodor.motor_control.stop()

    # Limpieza de basura
    hodor.cleanup()
