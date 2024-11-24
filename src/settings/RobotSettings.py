import json
import codecs
import os

from console.RobotLogger import RobotLogger


class RobotSettings:
    def __init__(self):
        # Video
        self.video_device_id: int = 8
        self.video_frame_width: int = 1280
        self.video_frame_height: int = 720
        self.video_enable_gui: bool = False

        # April Tags
        self.tag_far_size: int = 120
        self.tag_far_id: int = 1
        self.tag_close_size: int = 60
        self.tag_close_id: int = 0
        self.tag_family: str = "tag36h11"
        self.tag_threshold_distance: int = 2000
        self.tag_threshold_sample_size: int = 5

        # Motors
        self.motor_port: str = "/dev/ttyACM0"
        self.motor_baudrate: int = 9600
        self.motor_enable_movement: bool = True

        # Control
        self.control_tolerance_linear: int = 400
        self.control_tolerance_angular: int = 10

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
        settings = RobotSettings()

        if not os.path.exists(file_path):
            RobotLogger.warning(
                "No se pudo encontrar el archivo " + file_path + ". Se utilizará la configuración por defecto")
            return settings

        settings_json_str = codecs.open(file_path, 'r', encoding='utf-8').read()
        settings_json = json.loads(settings_json_str)

        # Video
        settings.video_device_id = settings_json["video"]["device_id"]
        settings.video_frame_width = settings_json["video"]["frame_width"]
        settings.video_frame_height = settings_json["video"]["frame_height"]
        settings.video_enable_gui = settings_json["video"]["enable_gui"]

        # April Tags
        settings.tag_far_size = settings_json["tag"]["far_size"]
        settings.tag_far_id = settings_json["tag"]["far_id"]
        settings.tag_close_size = settings_json["tag"]["close_size"]
        settings.tag_close_id = settings_json["tag"]["close_id"]
        settings.tag_threshold_distance = settings_json["tag"]["threshold_distance"]
        settings.tag_threshold_distance = settings_json["tag"]["threshold_sample_size"]
        settings.tag_family = settings_json["tag"]["family"]

        # Motors
        settings.motor_port = settings_json["motor"]["port"]
        settings.motor_baudrate = settings_json["motor"]["baudrate"]
        settings.motor_enable_movement = settings_json["motor"]["enable_movement"]

        # Control
        settings.control_tolerance_linear = settings_json["control"]["tolerance"]["linear"]
        settings.control_tolerance_angular = settings_json["control"]["tolerance"]["angular"]

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

        RobotLogger.info("Settings cargadas")

        return settings
