from common.Vector2 import Vector2


class MapEntity:
    def __init__(self, radius: float):
        self.__position = Vector2()
        self.__RADIUS = radius

    def get_x(self):
        return self.__position.get_x()

    def get_y(self):
        return self.__position.get_y()

    def get_module(self):
        return self.__position.get_module()

    def get_angle(self):
        return self.__position.get_angle()
