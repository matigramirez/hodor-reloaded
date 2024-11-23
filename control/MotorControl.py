from serial import Serial

from control.MotorMode import MotorMode
from settings.HodorSettings import HodorSettings


class MotorControl:
    def __init__(self, settings: HodorSettings):
        self.settings = settings
        self.serial: Serial | None = None
        self.__mode: MotorMode = MotorMode.NORMAL

        # Caracter 'X' que indica el inicio de un comando para la velocidad de los motores
        self.__command_start: int = int(ord("X"))

        if not self.settings.motor_enable_movement:
            print("[INFO] Control de motores deshabilitado. Conexión serial no inicializada.")
            return

        self.serial = Serial(settings.motor_port, settings.motor_baudrate)
        print("[INFO] Conectado al puerto serial " + settings.motor_port + " con " + str(
            settings.motor_baudrate) + " baudrate")

    def set_mode(self, mode: MotorMode):
        self.__mode = mode

    def __send_movement__(self, right_speed: int, left_speed: int):
        if not self.settings.motor_enable_movement:
            return

        # Mismo "hack" que tenía el robot para evitar convertir la velocidad 0xA en el caracter \n
        if right_speed == 0xA:
            right_speed = 0xB

        if left_speed == 0xA:
            left_speed = 0xB

        # Limitar velocidades a el valor máximo de 1 signed byte
        if right_speed > 0xFF:
            right_speed = 0xFF

        if left_speed > 0xFF:
            left_speed = 0xFF

        # Enviar comando de movimiento mediante conexión serial
        command = bytearray([self.__command_start, right_speed, left_speed])
        self.serial.write(command)

    def stop(self):
        if self.settings.motor_enable_movement:
            self.__send_movement__(0, 0)

    def forward(self):
        if self.settings.motor_enable_movement:
            if self.__mode == MotorMode.SLOW:
                self.__send_movement__(self.settings.movement_slow_forward_speed_right,
                                       self.settings.movement_slow_forward_speed_left)
            else:
                self.__send_movement__(self.settings.movement_normal_forward_speed_right,
                                       self.settings.movement_normal_forward_speed_left)

    def turn_right(self):
        if self.settings.motor_enable_movement:
            if self.__mode == MotorMode.SLOW:
                self.__send_movement__(self.settings.movement_slow_turn_right_speed_right,
                                       self.settings.movement_slow_turn_right_speed_left)
            else:
                self.__send_movement__(self.settings.movement_normal_turn_right_speed_right,
                                       self.settings.movement_normal_turn_right_speed_left)

    def turn_left(self):
        if self.settings.motor_enable_movement:
            if self.__mode == MotorMode.SLOW:
                self.__send_movement__(self.settings.movement_slow_turn_left_speed_right,
                                       self.settings.movement_slow_turn_left_speed_right)
            else:
                self.__send_movement__(self.settings.movement_normal_turn_left_speed_right,
                                       self.settings.movement_normal_turn_left_speed_right)
