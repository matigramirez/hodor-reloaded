from serial import Serial

from hodor.HodorSettings import HodorSettings
from robot.control.MotorControl import MotorControl
from robot.control.MovementMode import MovementMode
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger


class HodorMotorControl(MotorControl):
    def __init__(self, robot_settings: RobotSettings, hodor_settings: HodorSettings):
        super().__init__()

        self.robot_settings = robot_settings
        self.settings = hodor_settings
        self.serial: Serial | None = None
        # Caracter 'X' que indica el inicio de un comando para la velocidad de los motores
        self.__command_start: int = int(ord("X"))

        if not robot_settings.motor_enable_movement:
            RobotLogger.warning("Control de motores deshabilitado. Conexión serial no inicializada.")
            return

        self.serial = Serial(self.settings.motor_port, self.settings.motor_baud_rate)
        RobotLogger.info("Conectado al puerto serial " + self.settings.motor_port + " con " + str(
            self.settings.motor_baud_rate) + " baudrate")

    def __send_movement__(self, right_speed: int, left_speed: int):
        if not self.robot_settings.motor_enable_movement:
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
        if self.robot_settings.motor_enable_movement:
            self.__send_movement__(0, 0)

    def forward(self):
        if self.robot_settings.motor_enable_movement:
            self.__send_movement__(128+50, 153+50)

    def turn_right(self):
        if self.robot_settings.motor_enable_movement:
            self.__send_movement__(127-25-50-50, 128+25+50+50)

    def turn_left(self):
        if self.robot_settings.motor_enable_movement:
            self.__send_movement__(128+25+50+50, 127-25-50-50)

    def close(self):
        if self.serial is not None:
            self.serial.close()
