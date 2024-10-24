import cv2
import os

from camera.HodorCamera import HodorCamera
from common.CalibrationType import CalibrationType
from common.Status import Status
from control.MotorControl import MotorControl
from core.KineticMapEntity import KineticMapEntity
from detection.HodorTagDetector import HodorTagDetector
from output.HodorVideoOutput import HodorVideoOutput


class Hodor(KineticMapEntity):
    ANGULAR_TOLERANCE = 10
    SPACE_TOLERANCE = 100  # Distancia en milimetros
    MOVEMENT_DELAY_IN_SECONDS = 1

    def __init__(self, motor_control: MotorControl, video_device_id: int, tag_size: int,
                 calibration_type: CalibrationType, enable_gui=False):
        super().__init__(0, motor_control)

        self.camera = None
        self.video_device_id = video_device_id
        self.tag_size = tag_size
        self.calibration_type = calibration_type
        self.video_output = None
        self.tag_detector = None
        self.enable_gui = enable_gui
        self.__status = Status.RESTING

        print("##############################################")
        print("####           HODOR ft. VI23            #####")
        print("##############################################")

    def setup(self):
        print("[INFO] Iniciando configuración...")

        ##### PASO 1: Inicializar instancia de cámara #####
        self.camera = HodorCamera(video_id=self.video_device_id, enable_gui=self.enable_gui)

        ##### PASO 2: Calibración #####
        if self.calibration_type == CalibrationType.SCRATCH:
            self.camera.calibrate_from_scratch()

        if self.calibration_type == CalibrationType.DATASET:
            self.camera.calibrate_from_dataset()

        if self.calibration_type == CalibrationType.LOAD:
            if os.path.exists("calibration.vi23"):
                self.camera.load_calibration("calibration.vi23")
            else:
                print("[WARN] calibration.vi23 no encontrado. Inicializando nueva calibración")
                self.camera.calibrate_from_scratch()

        self.camera.save_calibration("calibration.vi23")

        if self.enable_gui:
            self.video_output = HodorVideoOutput(self.camera)

        ##### PASO 3: Inicializar detector de april tags #####
        self.tag_detector = HodorTagDetector(self.camera, self.tag_size, enable_gui=self.enable_gui)

        print("[INFO] Configuración finalizada")

    def loop(self):
        print("[INFO] Comenzando rutina...")
        # self.go_to_target()

        while True:
            self.tag_detector.detect_apriltags(self.video_output)

        print("[INFO] Rutina finalizada")

    def set_status(self, status: Status):
        self.__status = status
        print("[INFO] Status update: " + str(status))

    def find_distance_to_target(self) -> float:
        april_tags = []

        while len(april_tags) <= 0:
            april_tags = self.tag_detector.detect_apriltags(self.video_output)

        print("[LOG] April tag encontrado. Distancia: {}".format(april_tags[0].relative_distance))

        return april_tags[0].relative_distance

    def go_to_target(self) -> bool:
        distance = self.find_distance_to_target()

        while distance < Hodor.SPACE_TOLERANCE:
            self.move_forward()
            distance = self.find_distance_to_target()

        self.stop()
        return True

    def cleanup(self):
        self.camera.close()
        cv2.destroyAllWindows()
        self.video_output.close()
