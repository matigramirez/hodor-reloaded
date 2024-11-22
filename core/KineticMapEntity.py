from control.MotorAction import MotorAction
from control.MotorControl import MotorControl
from core.MapEntity import MapEntity


class KineticMapEntity(MapEntity):

    def __init__(self, motor_control: MotorControl):
        super().__init__()
        self.moving = False
        self.__motor_control = motor_control
        self.__current_action: MotorAction = MotorAction.STOP

    def move_forward(self):
        self.moving = True
        print("[INFO] Movimiento -> Avanzando")

        if self.__current_action != MotorAction.FORWARD:
            self.__current_action = MotorAction.FORWARD
            self.__motor_control.forward()

    def stop(self):
        self.moving = False
        print("[INFO] Movimiento -> Detenido")

        if self.__current_action != MotorAction.STOP:
            self.__current_action = MotorAction.STOP
            self.__motor_control.stop()

    def turn_left(self):
        self.moving = True
        print("[INFO] Movimiento -> Giro Izquierda")

        if self.__current_action != MotorAction.LEFT:
            self.__current_action = MotorAction.LEFT
            self.__motor_control.turn_left()

    def turn_right(self):
        self.moving = True
        print("[INFO] Movimiento -> Giro Derecha")

        if self.__current_action != MotorAction.RIGHT:
            self.__current_action = MotorAction.RIGHT
            self.__motor_control.turn_right()
