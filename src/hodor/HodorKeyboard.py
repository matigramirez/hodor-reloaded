from hodor.HodorInputHandler import HodorInputHandler
from robot.control.MotorControl import MotorControl
from robot.core.Robot import Robot
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger


class HodorKeyboard(Robot):
    def __init__(self, settings: RobotSettings, motor_control: MotorControl):
        self.settings = settings
        self.motor_control = motor_control
        super().__init__(settings, motor_control)
        self.input_handler = HodorInputHandler()

    def setup(self):
        self.stop()

    def loop(self):
        self.__print_available_commands__()

        while True:
            command = self.__process_input_command__()

            if command == 'w':
                self.move_forward()
            elif command == 'a':
                self.turn_left()
            elif command == 'd':
                self.turn_right()
            elif command == 'p':
                self.stop()
            elif command == 'q' or command == 'x':
                return

            self.scanner.scan()

    @staticmethod
    def __print_available_commands__():
        RobotLogger.print("\nComandos disponibles:")
        RobotLogger.print("'w': avanzar")
        RobotLogger.print("'a': giro izquierda")
        RobotLogger.print("'d': giro derecha")
        RobotLogger.print("'p': detenerse")
        RobotLogger.print("'x': salir")

    def cleanup(self):
        super().cleanup()
        self.input_handler.close()

    def __process_input_command__(self):
        while self.input_handler.running:
            # Procesar comandos pendientes
            command = self.input_handler.get_next_command()
            if command:
                RobotLogger.log("Comando recibido: {}".format(command))
                return command

            return None
