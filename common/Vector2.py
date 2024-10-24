import math


class Vector2:

    def __init__(self):
        self.__x = 0
        self.__y = 0
        self.__angle = 0
        self.__module = 0

    def set_polar(self, module: float, angle: float):
        self.__module = module
        self.__angle = angle
        self.calculate_rectangular_position()

    def set_cartesian(self, x: float, y: float):
        self.__x = x
        self.__y = y
        self.calculate_polar_position()

    def calculate_rectangular_position(self):
        angle_radians = math.radians(self.__angle)
        self.__x = self.__module * math.cos(angle_radians)
        self.__y = self.__module * math.sin(angle_radians)

    def calculate_polar_position(self):
        self.__module = math.sqrt(self.__x ** 2 + self.__y ** 2)
        self.__angle = math.degrees(math.atan2(self.__y, self.__x))

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_module(self):
        return self.__module

    def get_angle(self):
        return self.__angle
