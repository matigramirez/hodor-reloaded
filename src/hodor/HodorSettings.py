import json
import codecs
import os

from robot.console.RobotLogger import RobotLogger


class HodorSettings:
    def __init__(self):
        # Motors
        self.motor_port: str = "/dev/ttyACM0"
        self.motor_baud_rate: int = 9600

        # Movement
        self.movement_normal_forward_speed_right: int = 128
        self.movement_normal_forward_speed_left: int = 153
        self.movement_normal_turn_right_speed_right: int = 218
        self.movement_normal_turn_right_speed_left: int = 37
        self.movement_normal_turn_left_speed_right: int = 52
        self.movement_normal_turn_left_speed_left: int = 203

        self.movement_slow_forward_speed_right: int = 128
        self.movement_slow_forward_speed_left: int = 153
        self.movement_slow_turn_right_speed_right: int = 218
        self.movement_slow_turn_right_speed_left: int = 37
        self.movement_slow_turn_left_speed_right: int = 52
        self.movement_slow_turn_left_speed_left: int = 203

    @staticmethod
    def read_from_file(file_path: str):
        settings = HodorSettings()

        if not os.path.exists(file_path):
            RobotLogger.warning(
                "No se pudo encontrar el archivo " + file_path + ". Se utilizará la configuración por defecto")
            return settings

        settings_json_str = codecs.open(file_path, 'r', encoding='utf-8').read()
        settings_json = json.loads(settings_json_str)

        # Motors
        settings.motor_port = settings_json["motor"]["port"]
        settings.motor_baud_rate = settings_json["motor"]["baud_rate"]

        # Movement
        settings.movement_normal_forward_speed_right = settings_json["movement"]["normal"]["forward"]["speed_right"]
        settings.movement_normal_forward_speed_left = settings_json["movement"]["normal"]["forward"]["speed_left"]
        settings.movement_normal_turn_right_speed_right = settings_json["movement"]["normal"]["turn_right"][
            "speed_right"]
        settings.movement_normal_turn_right_speed_left = settings_json["movement"]["normal"]["turn_right"]["speed_left"]
        settings.movement_normal_turn_left_speed_right = settings_json["movement"]["normal"]["turn_left"]["speed_right"]
        settings.movement_normal_turn_left_speed_left = settings_json["movement"]["normal"]["turn_left"]["speed_left"]

        settings.movement_slow_forward_speed_right = settings_json["movement"]["slow"]["forward"]["speed_right"]
        settings.movement_slow_forward_speed_left = settings_json["movement"]["slow"]["forward"]["speed_left"]
        settings.movement_slow_turn_right_speed_right = settings_json["movement"]["slow"]["turn_right"]["speed_right"]
        settings.movement_slow_turn_right_speed_left = settings_json["movement"]["slow"]["turn_right"]["speed_left"]
        settings.movement_slow_turn_left_speed_right = settings_json["movement"]["slow"]["turn_left"]["speed_right"]
        settings.movement_slow_turn_left_speed_left = settings_json["movement"]["slow"]["turn_left"]["speed_left"]

        RobotLogger.info(file_path + " cargado")

        return settings
