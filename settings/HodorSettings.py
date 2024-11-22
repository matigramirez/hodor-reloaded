import json
import codecs
import os


class HodorSettings:
    def __init__(self):
        self.video_device_id: int = 8
        self.video_frame_width: int = 1280
        self.video_frame_height: int = 720
        self.video_enable_gui: bool = False
        self.tag_size: int = 145
        self.tag_family: str = "tag36h11"
        self.motor_port: str = "/dev/ttyACM0"
        self.motor_baudrate: int = 9600
        self.motor_enable_movement: bool = True
        self.control_tolerance_linear: int = 400
        self.control_tolerance_angular: int = 10
        self.movement_forward_speed_right: int = 128
        self.movement_forward_speed_left: int = 153
        self.movement_backwards_speed_right: int = 127
        self.movement_backwards_speed_left: int = 112
        self.movement_turn_right_speed_right: int = 218
        self.movement_turn_right_speed_left: int = 37
        self.movement_turn_left_speed_right: int = 52
        self.movement_turn_left_speed_left: int = 203

    @staticmethod
    def read_from_file(file_path: str):
        settings = HodorSettings()

        if not os.path.exists(file_path):
            print("[WARN] No se pudo encontrar el archivo " + file_path + ". Se utilizará la configuración por defecto")
            return settings

        settings_json_str = codecs.open(file_path, 'r', encoding='utf-8').read()
        settings_json = json.loads(settings_json_str)

        settings.video_device_id = settings_json["video"]["device_id"]
        settings.video_frame_width = settings_json["video"]["frame_width"]
        settings.video_frame_height = settings_json["video"]["frame_height"]
        settings.video_enable_gui = settings_json["video"]["enable_gui"]
        settings.tag_size = settings_json["tag"]["size"]
        settings.tag_family = settings_json["tag"]["family"]
        settings.motor_port = settings_json["motor"]["port"]
        settings.motor_baudrate = settings_json["motor"]["baudrate"]
        settings.motor_enable_movement = settings_json["motor"]["enable_movement"]
        settings.control_tolerance_linear = settings_json["control"]["tolerance"]["linear"]
        settings.control_tolerance_angular = settings_json["control"]["tolerance"]["angular"]
        settings.movement_forward_speed_right = settings_json["movement"]["forward_speed_right"]
        settings.movement_forward_speed_left = settings_json["movement"]["forward_speed_left"]
        settings.movement_backwards_speed_right = settings_json["movement"]["backwards_speed_right"]
        settings.movement_backwards_speed_left = settings_json["movement"]["backwards_speed_left"]
        settings.movement_turn_right_speed_right = settings_json["movement"]["turn_right_speed_right"]
        settings.movement_turn_right_speed_left = settings_json["movement"]["turn_right_speed_left"]
        settings.movement_turn_left_speed_right = settings_json["movement"]["turn_left_speed_right"]
        settings.movement_turn_left_speed_left = settings_json["movement"]["turn_left_speed_left"]

        print("[INFO] Settings cargadas")

        return settings
