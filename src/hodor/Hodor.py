from robot.common.Status import Status
from robot.control.MotorControl import MotorControl
from robot.core.Robot import Robot
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger


class Hodor(Robot):
    def __init__(self, settings: RobotSettings, motor_control: MotorControl):
        self.settings = settings
        self.motor_control = motor_control
        super().__init__(settings, motor_control)

    def setup(self):
        self.stop()

    def loop(self):
        RobotLogger.info("Iniciando rutina")

        while True:
            while self.is_target_reached():
                self.stop()
                self.set_status(Status.TARGET_REACHED)

            # Encontrar base
            while not self.is_target_found():
                self.find_target()
                self.set_status(Status.FINDING_TARGET)

                if self.is_target_found():
                    self.stop()
                    self.set_status(Status.TARGET_FOUND)

            # Alinearse a la base
            while not self.is_aligned():
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

            # Si pierdo visión de la base dejo de moverme
            if not self.is_target_found():
                self.stop()
                self.set_status(Status.TARGET_LOST)
                continue

            # Moverse hacia la base
            self.move_towards_target()
            self.set_status(Status.MOVING_TOWARDS_TARGET)

        RobotLogger.info("Rutina finalizada")
