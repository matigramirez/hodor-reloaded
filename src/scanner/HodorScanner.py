from camera.HodorCamera import HodorCamera
from detection.HodorTagDetector import HodorTagDetector
from scanner.ScanResult import ScanResult
from settings.HodorSettings import HodorSettings
from collections import deque
from statistics import mean
from console.HodorLogger import HodorLogger


class HodorScanner:
    def __init__(self, camera: HodorCamera, settings: HodorSettings):
        self.settings = settings

        self.__far_tag_detector = HodorTagDetector(camera, settings.tag_family, settings.tag_far_size,
                                                   settings.tag_far_id,
                                                   enable_gui=settings.video_enable_gui)

        self.__close_tag_detector = HodorTagDetector(camera, settings.tag_family, settings.tag_close_size,
                                                     settings.tag_close_id,
                                                     enable_gui=settings.video_enable_gui)

        self.tag_detector = self.__far_tag_detector

        self.__latest_samples = deque(maxlen=settings.tag_threshold_sample_size)

        self.__is_nearby = False

    def scan(self) -> ScanResult | None:
        self.update_detector()

        april_tags = self.tag_detector.detect_apriltags()

        if len(april_tags) <= 0:
            return None

        distance = april_tags[0].distance
        angle = april_tags[0].angle

        HodorLogger.log("April tag detectado [{}] (dist: {}mm  |  ang: {}°)".format(
            "corto alcance" if self.__is_nearby else "largo alcance", distance, angle))

        return ScanResult(distance, angle)

    def update_detector(self):
        if len(self.__latest_samples) <= self.settings.tag_threshold_sample_size:
            return

        avg = mean(self.__latest_samples)

        if avg < self.settings.tag_threshold_distance:
            if not self.__is_nearby:
                self.tag_detector = self.__close_tag_detector
                self.__latest_samples.clear()
                self.__is_nearby = True
                HodorLogger.info("Cambiando a detector de largo alcance")
        else:
            if self.__is_nearby:
                self.tag_detector = self.__far_tag_detector
                self.__latest_samples.clear()
                self.__is_nearby = False
                HodorLogger.info("Cambiando a detector de corto alcance")
