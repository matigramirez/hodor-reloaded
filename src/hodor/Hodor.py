import time

from hodor.HodorInputHandler import HodorInputHandler
from robot.common.Status import Status
from robot.control.MotorControl import MotorControl
from robot.core.Robot import Robot
from robot.exceptions.CancellationRequestedException import CancellationRequestedException
from robot.exceptions.StopRequestedException import StopRequestedException
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger


class Hodor(Robot):
    def __init__(self, settings: RobotSettings, motor_control: MotorControl):
        self.settings = settings
        self.motor_control = motor_control
        super().__init__(settings, motor_control)
        self.input_handler = HodorInputHandler()

        self.__start_requested = False

    def setup(self):
        self.stop()

    def loop(self):
        self.__print_available_commands__()

        while True:
            try:
                self.__execute_command__()

                if self.__start_requested:
                    self.__start_requested = False
                    self.play()

                time.sleep(0.3)

            except CancellationRequestedException:
                self.stop()
                RobotLogger.info("Rutina cancelada por el usuario")
                return

            except StopRequestedException:
                self.stop()
                RobotLogger.info("Rutina detenida por el usuario")
                self.__print_available_commands__()

    @staticmethod
    def __print_available_commands__():
        RobotLogger.print("\nComandos disponibles:")
        RobotLogger.print("'s': comenzar rutina")
        RobotLogger.print("'p': detener rutina")
        RobotLogger.print("'q': cancelar ejecución")

    def play(self):
        RobotLogger.info("Iniciando rutina")

        while True:
            self.__execute_command__()

            while self.is_target_reached():
                self.__execute_command__()

                self.stop()
                self.set_status(Status.TARGET_REACHED)

            # Encontrar base
            while not self.is_target_found():
                self.__execute_command__()

                self.find_target()
                self.set_status(Status.FINDING_TARGET)

                if self.is_target_found():
                    self.stop()
                    self.set_status(Status.TARGET_FOUND)

            # Alinearse a la base
            while not self.is_aligned():
                self.__execute_command__()

                self.set_status(Status.ALIGNING_TO_TARGET)
                self.align_to_target()

                if self.is_aligned():
                    self.stop()
                    self.set_status(Status.ALIGNED_TO_TARGET)

                # Si por algún motivo perdí visión de la base, suspendo la alineación y me detengo
                if not self.is_target_found():
                    self.stop()
                    self.set_status(Status.TARGET_LOST)
                    break

            self.__execute_command__()

            # Si pierdo visión de la base dejo de moverme
            if not self.is_target_found():
                self.stop()
                self.set_status(Status.TARGET_LOST)
                continue

            self.__execute_command__()

            # Moverse hacia la base
            self.move_towards_target()
            self.set_status(Status.MOVING_TOWARDS_TARGET)

        RobotLogger.info("Rutina finalizada")

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

    def __execute_command__(self):
        command = self.__process_input_command__()

        if command is not None:
            if command == 's' or command == 'S':
                self.__start_requested = True

            elif command == 'p' or command == 'P':
                raise StopRequestedException()

            elif command == 'q' or command == 'Q':
                raise CancellationRequestedException()

            else:
                RobotLogger.warning("Comando '{}' no reconocido".format(command))
