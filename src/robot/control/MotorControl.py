from abc import ABC, abstractmethod

from robot.control.MovementMode import MovementMode


class MotorControl(ABC):
    def __init__(self):
        self.__mode: MovementMode = MovementMode.NORMAL

    def set_mode(self, mode: MovementMode):
        self.__mode = mode

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def forward(self):
        pass

    @abstractmethod
    def turn_right(self):
        pass

    @abstractmethod
    def turn_left(self):
        pass

    @abstractmethod
    def close(self):
        pass
