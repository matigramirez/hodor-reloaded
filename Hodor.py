import cv2
import os

from camera.HodorCamera import HodorCamera
from common.CalibrationType import CalibrationType
from common.Status import Status
from control.MotorControl import MotorControl
from core.KineticMapEntity import KineticMapEntity
from detection.HodorTagDetector import HodorTagDetector
from output.HodorVideoOutput import HodorVideoOutput
from models.HodorAprilTag import HodorAprilTag
from typing import List


class Hodor(KineticMapEntity):
    ANGULAR_TOLERANCE = 10
    SPACE_TOLERANCE = 400  # Distancia en milimetros
    MOVEMENT_DELAY_IN_SECONDS = 1

    def __init__(self, motor_control: MotorControl | None, video_device_id: int, frame_width: int, frame_height: int,
                 tag_size: int,
                 calibration_type: CalibrationType, enable_gui=False):
        super().__init__(0, motor_control)

        self.camera = None
        self.video_device_id = video_device_id
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.tag_size = tag_size
        self.calibration_type = calibration_type
        self.video_output: HodorVideoOutput | None = None
        self.tag_detector: HodorTagDetector | None = None
        self.enable_gui = enable_gui
        self.__status = Status.RESTING

        print("##############################################")
        print("####           HODOR ft. VI23            #####")
        print("##############################################")

    def setup(self):
        print("[INFO] Iniciando configuración...")

        ##### PASO 1: Inicializar instancia de cámara #####
        self.camera = HodorCamera(self.video_device_id, self.frame_width, self.frame_height, enable_gui=self.enable_gui)

        ##### PASO 2: Calibración #####
        if self.calibration_type == CalibrationType.SCRATCH:
            self.camera.calibrate_from_scratch()

        if self.calibration_type == CalibrationType.DATASET:
            self.camera.calibrate_from_dataset()

        if self.calibration_type == CalibrationType.LOAD:
            if os.path.exists("calibration.json"):
                self.camera.load_calibration("calibration.json")
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

        self.go_to_target()

        print("[INFO] Rutina finalizada")

    def set_status(self, status: Status):
        self.__status = status
        print("[INFO] Status update: " + str(status))

    def find_april_tags(self)-> List[HodorAprilTag]:
        april_tags = []

        while len(april_tags) <= 0:
            april_tags = self.tag_detector.detect_apriltags(self.video_output)
            if self.__status != Status.FINDING_TARGET:
                self.set_status(Status.FINDING_TARGET)
                self.turn_left()
        self.stop()
        self.set_status(Status.READY_TO_GO)
        return april_tags

    def find_distance_to_target(self) -> float:
        april_tags = april_tags = self.tag_detector.detect_apriltags(self.video_output)
        if len(april_tags) <= 0:
            april_tags = self.find_april_tags()

        print("[LOG] April tag encontrado. Distancia: {}".format(april_tags[0].relative_distance))

        return april_tags[0].relative_distance

    def go_to_target(self) -> bool:
        distance = self.find_distance_to_target()

        while distance > Hodor.SPACE_TOLERANCE:
            self.move_forward()
            distance = self.find_distance_to_target()

        self.stop()
        return True

    def cleanup(self):
        self.camera.close()
        cv2.destroyAllWindows()

        if self.video_output is not None:
            self.video_output.close()
