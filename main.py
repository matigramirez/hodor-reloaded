from Hodor import Hodor
from common.CalibrationType import CalibrationType

# ID de dispositivo de video (En el robot hodor es id=8)
VIDEO_DEVICE_ID = 0

# Tamaño del april tag en milimetros
TAG_SIZE = 145

# Configuración serial de los motores
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 9600

# Inicializar motores
# TODO: Reestablecer esto
# motor_control = MotorControl(SERIAL_PORT, SERIAL_BAUDRATE)
motor_control = None

# Iniciazar Hodor
hodor = Hodor(motor_control, VIDEO_DEVICE_ID, TAG_SIZE, CalibrationType.LOAD, enable_gui=True)

# Configuración inicial
hodor.setup()

# Bucle principal
hodor.loop()

# Limpieza de basura
hodor.cleanup()
