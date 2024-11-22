from detection.HodorTagDetector import HodorTagDetector
from scanner.ScanResult import ScanResult


class HodorScanner:
    @staticmethod
    def scan(tag_detector: HodorTagDetector) -> ScanResult | None:
        april_tags = tag_detector.detect_apriltags()

        if len(april_tags) <= 0:
            return None

        distance = april_tags[0].distance
        angle = april_tags[0].angle

        print("[LOG] April tag detectado (dist: {}mm  |  ang: {}°)".format(distance, angle))

        return ScanResult(distance, angle)
