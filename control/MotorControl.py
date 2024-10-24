from serial import Serial

# Caracter 'X' que indica el inicio de un comando para la velocidad de los motores
command_start = int(ord("X"))

# Velocidades de los motores para movimiento hacia adelante
velocidad_adelante_motor_derecho = 128
velocidad_adelante_motor_izquierdo = 128 + 25

# Velocidades de los motores para movimiento hacia atrás
velocidad_atras_motor_derecho = 127
velocidad_atras_motor_izquierdo = 127 - 15

# Velocidades de los motores para movimiento de giro hacia la derecha
velocidad_giro_derecha_motor_derecho = 128 + 90
velocidad_giro_derecha_motor_izquierdo = 127 - 90

# Velocidades de los motores para movimiento de giro hacia la izquierda
velocidad_giro_izquierda_motor_derecho = 127 - 25 - 50
velocidad_giro_izquierda_motor_izquierdo = 128 + 25 + 50


class MotorControl:
    def __init__(self, puerto: str, baudrate: int):
        self.puerto = puerto
        self.baudrate = baudrate
        self.serial = Serial(self.puerto, self.baudrate)
        print("Connected to port " + self.puerto + " with " + str(self.baudrate) + " baudrate")
        self.__velocidad_motor_izquierdo = 0
        self.__velocidad_motor_derecho = 0

    def enviar_datos(self):
        command = bytearray([command_start, self.__velocidad_motor_derecho, self.__velocidad_motor_izquierdo])
        self.serial.write(command)

    def enviar_movimiento(self, velocidad_motor_derecho: int, velocidad_motor_izquierdo: int):
        # Mismo "hack" que tenía el robot para evitar convertir la velocidad 0xA en el caracter \n
        if velocidad_motor_derecho == 0xA:
            velocidad_motor_derecho = 0x0B

        if velocidad_motor_izquierdo == 0xA:
            velocidad_motor_izquierdo = 0x0B

        # Limitar velocidades a el valor máximo de 1 byte
        if velocidad_motor_derecho > 0xFF:
            velocidad_motor_derecho = 0xFF

        if velocidad_motor_izquierdo > 0xFF:
            velocidad_motor_izquierdo = 0xFF

        self.__velocidad_motor_derecho = velocidad_motor_derecho
        self.__velocidad_motor_izquierdo = velocidad_motor_izquierdo
        self.enviar_datos()

    def stop(self):
        self.enviar_movimiento(0, 0)

    def forward(self):
        self.enviar_movimiento(velocidad_adelante_motor_derecho, velocidad_adelante_motor_izquierdo)

    def back(self):
        self.enviar_movimiento(velocidad_atras_motor_derecho, velocidad_atras_motor_izquierdo)

    def turn_right(self):
        self.enviar_movimiento(velocidad_giro_derecha_motor_derecho, velocidad_giro_derecha_motor_izquierdo)

    def turn_left(self):
        self.enviar_movimiento(velocidad_giro_izquierda_motor_derecho, velocidad_giro_izquierda_motor_izquierdo)
