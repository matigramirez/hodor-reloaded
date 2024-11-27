from collections import deque
from statistics import mean

from robot.camera.RobotCamera import RobotCamera
from robot.streaming.RobotVideoStream import RobotVideoStream
from robot.tags.RobotTagDetector import RobotTagDetector
from robot.scanner.ScanResult import ScanResult
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger


class RobotScanner:
    def __init__(self, camera: RobotCamera, settings: RobotSettings, video_stream: RobotVideoStream | None = None):
        self.settings = settings

        self.__far_tag_detector = RobotTagDetector(settings, camera, settings.tag_family, settings.tag_far_size,
                                                   settings.tag_far_id,
                                                   video_stream)

        self.__close_tag_detector = RobotTagDetector(settings, camera, settings.tag_family, settings.tag_close_size,
                                                     settings.tag_close_id,
                                                     video_stream)

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

        self.__latest_samples.append(distance)

        RobotLogger.log("April tag detectado [{}] (dist: {:.2f}mm  |  ang: {:.2f}°)".format(
            "corto alcance" if self.__is_nearby else "largo alcance", distance, angle))

        return ScanResult(distance, angle)

    def update_detector(self):
        if len(self.__latest_samples) < self.settings.tag_threshold_sample_size:
            return

        avg = mean(self.__latest_samples)

        if avg < self.settings.tag_threshold_distance:
            if not self.__is_nearby:
                self.tag_detector = self.__close_tag_detector
                self.__latest_samples.clear()
                self.__is_nearby = True
                RobotLogger.info("Cambiando a detector de largo alcance")
        else:
            if self.__is_nearby:
                self.tag_detector = self.__far_tag_detector
                self.__latest_samples.clear()
                self.__is_nearby = False
                RobotLogger.info("Cambiando a detector de corto alcance")
