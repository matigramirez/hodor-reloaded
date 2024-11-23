from control.MotorAction import MotorAction
from control.MotorControl import MotorControl
from control.MotorMode import MotorMode
from console.HodorLogger import HodorLogger


class KineticMapEntity:

    def __init__(self, motor_control: MotorControl):
        self.moving = False
        self.__motor_control = motor_control
        self.__current_action: MotorAction = MotorAction.STOP
        self.__motor_mode = MotorMode.NORMAL
        self.__mode_changed = False

    def set_motor_mode(self, mode: MotorMode):
        if mode != self.__motor_mode:
            self.__mode_changed = True

        self.__motor_mode = mode

    def move_forward(self):
        self.moving = True
        HodorLogger.info("Movimiento -> Avanzando")

        if self.__mode_changed or self.__current_action != MotorAction.FORWARD:
            self.__mode_changed = False
            self.__current_action = MotorAction.FORWARD
            self.__motor_control.forward()

    def stop(self):
        self.moving = False
        HodorLogger.info("Movimiento -> Detenido")

        if self.__mode_changed or self.__current_action != MotorAction.STOP:
            self.__mode_changed = False
            self.__current_action = MotorAction.STOP
            self.__motor_control.stop()

    def turn_left(self):
        self.moving = True
        HodorLogger.info("Movimiento -> Giro Izquierda")

        if self.__mode_changed or self.__current_action != MotorAction.LEFT:
            self.__mode_changed = False
            self.__current_action = MotorAction.LEFT
            self.__motor_control.turn_left()

    def turn_right(self):
        self.moving = True
        HodorLogger.info("Movimiento -> Giro Derecha")

        if self.__mode_changed or self.__current_action != MotorAction.RIGHT:
            self.__mode_changed = False
            self.__current_action = MotorAction.RIGHT
            self.__motor_control.turn_right()
