import time

from robot.control.MotorAction import MotorAction
from robot.control.MotorControl import MotorControl
from robot.control.MovementMode import MovementMode
from robot.console.RobotLogger import RobotLogger


class KineticMapEntity:

    def __init__(self, motor_control: MotorControl):
        self.moving = False
        self.__motor_control = motor_control
        self.__current_action: MotorAction = MotorAction.STOP
        self.__motor_mode = MovementMode.NORMAL
        self.__mode_changed = False

    def set_mode(self, mode: MovementMode):
        if mode == self.__motor_mode:
            return

        self.__mode_changed = True
        self.__motor_mode = mode
        self.__motor_control.set_mode(mode)
        RobotLogger.info("Motor mode set to {}".format(mode))

    def move_forward(self):
        if self.__mode_changed or self.__current_action != MotorAction.FORWARD:
            self.moving = True
            RobotLogger.log("Movimiento -> Avanzando")
            self.__mode_changed = False
            self.__current_action = MotorAction.FORWARD
            self.__motor_control.forward()
            time.sleep(.2)

    def stop(self):
        if self.__mode_changed or self.__current_action != MotorAction.STOP:
            self.moving = False
            RobotLogger.log("Movimiento -> Detenido")
            self.__mode_changed = False
            self.__current_action = MotorAction.STOP
            self.__motor_control.stop()
            time.sleep(.2)

    def turn_left(self):
        if self.__mode_changed or self.__current_action != MotorAction.LEFT:
            self.moving = True
            RobotLogger.log("Movimiento -> Giro Izquierda")
            self.__mode_changed = False
            self.__current_action = MotorAction.LEFT
            self.__motor_control.turn_left()
            time.sleep(.2)

    def turn_right(self):
        if self.__mode_changed or self.__current_action != MotorAction.RIGHT:
            self.moving = True
            RobotLogger.log("Movimiento -> Giro Derecha")
            self.__mode_changed = False
            self.__current_action = MotorAction.RIGHT
            self.__motor_control.turn_right()
            time.sleep(.2)
