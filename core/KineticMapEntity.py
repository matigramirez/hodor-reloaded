from control.MotorControl import MotorControl
from core.MapEntity import MapEntity


class KineticMapEntity(MapEntity):

    def __init__(self, motor_control: MotorControl):
        super().__init__()
        self.moving = False
        self.__motor_control = motor_control

    def move_forward(self):
        self.moving = True
        print("[INFO] Movimiento -> Avanzando")
        self.__motor_control.forward()

    def stop(self):
        self.moving = False
        print("[INFO] Movimiento -> Detenido")
        self.__motor_control.stop()

    def turn_left(self):
        self.moving = True
        print("[INFO] Movimiento -> Giro Izquierda")
        self.__motor_control.turn_left()

    def turn_right(self):
        self.moving = True
        print("[INFO] Movimiento -> Giro Derecha")
        self.__motor_control.turn_right()
