from serial import Serial

from settings.HodorSettings import HodorSettings


class MotorControl:
    def __init__(self, settings: HodorSettings):
        self.settings = settings
        self.serial = None

        if not self.settings.motor_enable_movement:
            print("[INFO] Control de motores deshabilitado")
            return

        self.serial = Serial(settings.motor_port, settings.motor_baudrate)
        print("[INFO] Conectado al puerto serial " + settings.motor_port + " con " + str(
            settings.motor_baudrate) + " baudrate")
        self.__velocidad_motor_izquierdo = 0
        self.__velocidad_motor_derecho = 0

    def enviar_datos(self):
        if not self.settings.motor_enable_movement:
            return

        # Caracter 'X' que indica el inicio de un comando para la velocidad de los motores
        command_start = int(ord("X"))

        command = bytearray([command_start, self.__velocidad_motor_derecho, self.__velocidad_motor_izquierdo])
        self.serial.write(command)

    def enviar_movimiento(self, velocidad_motor_derecho: int, velocidad_motor_izquierdo: int):
        if not self.settings.motor_enable_movement:
            return

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
        if self.settings.motor_enable_movement:
            self.enviar_movimiento(0, 0)

    def forward(self):
        if self.settings.motor_enable_movement:
            self.enviar_movimiento(self.settings.movement_forward_speed_right,
                                   self.settings.movement_forward_speed_left)

    def back(self):
        if self.settings.motor_enable_movement:
            self.enviar_movimiento(self.settings.movement_backwards_speed_right,
                                   self.settings.movement_backwards_speed_left)

    def turn_right(self):
        if self.settings.motor_enable_movement:
            self.enviar_movimiento(self.settings.movement_turn_right_speed_right,
                                   self.settings.movement_turn_right_speed_left)

    def turn_left(self):
        if self.settings.motor_enable_movement:
            self.enviar_movimiento(self.settings.movement_turn_left_speed_right,
                                   self.settings.movement_turn_left_speed_right)
