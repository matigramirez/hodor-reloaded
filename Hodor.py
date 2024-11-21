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
from settings.HodorSettings import HodorSettings
from typing import List


class Hodor(KineticMapEntity):
    def __init__(self, settings: HodorSettings, calibration_type: CalibrationType):

        self.settings = settings
        self.motor_control = MotorControl(settings)

        super().__init__(self.motor_control)

        self.camera = None
        self.video_device_id = settings.video_device_id
        self.frame_width = settings.video_frame_width
        self.frame_height = settings.video_frame_height
        self.enable_gui = settings.video_enable_gui
        self.video_output: HodorVideoOutput | None = None

        self.tag_size = settings.tag_size
        self.tag_family = settings.tag_family
        self.tag_detector: HodorTagDetector | None = None

        self.calibration_type = calibration_type
        self.__status = Status.RESTING

        print("""##############################################\n
                ####           HODOR ft. VI23            #####\n
                ##############################################""")

    def setup(self):
        print("[INFO] Iniciando configuración...")

        ##### PASO 1: Inicializar instancia de cámara #####
        self.camera = HodorCamera(self.settings)

        ##### PASO 2: Calibración #####
        if self.calibration_type == CalibrationType.SCRATCH:
            self.camera.calibrate_from_scratch()
            self.camera.save_calibration("calibration.json")

        if self.calibration_type == CalibrationType.DATASET:
            self.camera.calibrate_from_dataset()
            self.camera.save_calibration("calibration.json")

        if self.calibration_type == CalibrationType.LOAD:
            if os.path.exists("calibration.json"):
                self.camera.load_calibration("calibration.json")
            else:
                print("[WARN] calibration.json no encontrado. Inicializando nueva calibración")
                self.camera.calibrate_from_scratch()

        if self.enable_gui:
            self.video_output = HodorVideoOutput(self.camera)

        ##### PASO 3: Inicializar detector de april tags #####
        self.tag_detector = HodorTagDetector(self.camera, self.tag_size, self.tag_family, enable_gui=self.enable_gui)

        print("[INFO] Configuración finalizada")

    def loop(self):
        print("[INFO] Comenzando rutina...")

        self.find_april_tags()
        self.go_to_target()

        print("[INFO] Rutina finalizada")

    def set_status(self, status: Status):
        self.__status = status
        print("[INFO] Status update: " + str(status))

    # def find_april_tags(self) -> List[HodorAprilTag]:
    #     april_tags = []

    #     while len(april_tags) <= 0:
    #         april_tags = self.tag_detector.detect_apriltags(self.video_output)

    #         if self.__status != Status.FINDING_TARGET:
    #             self.set_status(Status.FINDING_TARGET)
    #             self.turn_right()

    #         if len(april_tags) > 0:
    #             print(april_tags[0].angle)

    #     self.stop()
    #     self.set_status(Status.READY_TO_GO)
    #     return april_tags

    def find_april_tags(self) -> List[HodorAprilTag]:
        april_tags = []
        angle = 10000

        while abs(angle) > self.settings.control_tolerance_angular:
            april_tags = self.tag_detector.detect_apriltags(self.video_output)

            if self.__status != Status.FINDING_TARGET:
                self.set_status(Status.FINDING_TARGET)
                self.turn_right()

            if len(april_tags) > 0:
                angle = april_tags[0].angle
            else:
                angle = 10000

        self.stop()
        self.set_status(Status.READY_TO_GO)
        return april_tags

    def find_distance_to_target(self) -> float:
        april_tags = []

        while len(april_tags) <= 0:
            april_tags = self.tag_detector.detect_apriltags(self.video_output)

        print("[LOG] April tag encontrado. Distancia: {}  -  Angulo: {}".format(april_tags[0].relative_distance,
                                                                                april_tags[0].angle))

        return april_tags[0].relative_distance

    def go_to_target(self) -> bool:
        distance = self.find_distance_to_target()

        while distance > self.settings.control_tolerance_linear:
            if self.__status != Status.NAVIGATING:
                self.move_forward()
                self.__status = Status.NAVIGATING

            distance = self.find_distance_to_target()

        self.__status = Status.NAVIGATION_COMPLETED

        self.stop()
        return True

    def cleanup(self):
        self.camera.close()
        cv2.destroyAllWindows()

        if self.video_output is not None:
            self.video_output.close()
