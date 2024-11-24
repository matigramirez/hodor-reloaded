import os
from abc import ABC, abstractmethod

from robot.camera.RobotCamera import RobotCamera
from robot.common.Status import Status
from robot.control.MotorControl import MotorControl
from robot.core.KineticMapEntity import KineticMapEntity
from robot.scanner.RobotScanner import RobotScanner
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger
from robot.streaming.RobotVideoStream import RobotVideoStream


class Robot(ABC, KineticMapEntity):
    def __init__(self, settings: RobotSettings, motor_control: MotorControl):
        super().__init__(motor_control)

        self.settings = settings
        self.motor_control = motor_control

        self.camera = None
        self.video_device_id = settings.video_device_id
        self.frame_width = settings.video_frame_width
        self.frame_height = settings.video_frame_height

        self.__scanner: RobotScanner | None = None

        self.__status = Status.INITIALIZING

        self.__internal_setup__()

    def __internal_setup__(self):
        self.camera = RobotCamera(self.settings)

        if os.path.exists("calibration.json"):
            self.camera.load_calibration("calibration.json")
        else:
            raise Exception("calibration.json no encontrado. No es posible comenzar la rutina.")

        self.video_stream = RobotVideoStream(self.settings)
        self.__scanner = RobotScanner(self.camera, self.settings, self.video_stream)

        RobotLogger.info("Inicialización finalizada")

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def loop(self):
        pass

    def cleanup(self):
        # Detener motores
        self.stop()

        # Liberar recursos
        self.motor_control.close()
        self.camera.close()
        self.video_stream.close()

    def set_status(self, status: Status):
        if self.__status == status:
            return

        self.__status = status
        RobotLogger.log("Status: " + str(status))

    def is_target_reached(self) -> bool:
        scan = self.__scanner.scan()

        if scan is None:
            return False

        return scan.distance <= self.settings.control_tolerance_linear

    def is_target_found(self) -> bool:
        return self.__scanner.scan() is not None

    def is_aligned(self) -> bool:
        scan = self.__scanner.scan()

        if scan is None:
            return False

        return abs(scan.angle) <= self.settings.control_tolerance_angular

    def find_target(self):
        self.turn_right()

    def align_to_target(self):
        angle = self.__scanner.scan().angle

        if angle < 0:
            self.turn_left()
        else:
            self.turn_right()

    def move_towards_target(self):
        self.move_forward()
