from pyapriltags import Detector
import cv2
from typing import List
import numpy as np

from camera.HodorCamera import HodorCamera
from common.Vector2 import Vector2
from models.HodorAprilTag import HodorAprilTag
from output.HodorVideoOutput import HodorVideoOutput


class HodorTagDetector:
    def __init__(self, camera: HodorCamera, tag_size, enable_gui=False):
        self.__detector = Detector(families="tag36h11")
        self.__camera = camera
        self.__fx, self.__fy, self.__cx, self.__cy = camera.get_parameters()
        self.__tag_size = tag_size
        self.__enable_draw = enable_gui

    def detect_apriltags(self, video_output: HodorVideoOutput | None = None) -> List[HodorAprilTag]:
        cam_frame = None

        while cam_frame is None:
            cam_frame = self.__camera.get_frame()

        # Convert image to grayscale
        grayscale_img = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)

        # Detect april tags in image
        detections = self.__detector.detect(grayscale_img, estimate_tag_pose=True,
                                            camera_params=(self.__fx, self.__fy, self.__cx, self.__cy),
                                            tag_size=self.__tag_size)

        results = []

        for detection in detections:

            # Draw AprilTag corners
            if self.__enable_draw:
                # Get AprilTag corners
                (p1, p2, p3, p4) = detection.corners
                p2 = (int(p2[0]), int(p2[1]))
                p3 = (int(p3[0]), int(p3[1]))
                p4 = (int(p4[0]), int(p4[1]))
                p1 = (int(p1[0]), int(p1[1]))

                cv2.line(cam_frame, p1, p2, (0, 255, 0), 2)
                cv2.line(cam_frame, p2, p3, (0, 255, 0), 2)
                cv2.line(cam_frame, p3, p4, (0, 255, 0), 2)
                cv2.line(cam_frame, p4, p1, (0, 255, 0), 2)

            (cx, cy) = (int(detection.center[0]), int(detection.center[1]))

            # Draw AprilTag center
            if self.__enable_draw:
                cv2.circle(cam_frame, (cx, cy), 5, (0, 0, 255), -1)

            distance = np.linalg.norm(detection.pose_t)

            r = detection.pose_R
            yaw = np.arctan2(r[1, 0], r[0, 0])
            pitch = np.arcsin(-r[2, 0])
            roll = np.arctan2(r[2, 1], r[2, 2])

            # TODO: Revisar esto, parece no estar bien el orden
            # yaw = np.arctan2(r[1, 0], r[0, 0])
            # pitch = np.arctan2(-r[2, 0], np.sqrt(r[2, 1] ** 2 + r[2, 2] ** 2))
            # roll = np.arctan2(r[2, 1], r[2, 2])

            yaw_degrees = np.degrees(yaw)
            pitch_degrees = np.degrees(pitch)
            roll_degrees = np.degrees(roll)

            # Draw AprilTag id as text
            if self.__enable_draw:
                cv2.putText(cam_frame, "id: {}".format(detection.tag_id), (p1[0], p1[1] - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.putText(cam_frame, "dist: {0:.2f}".format(distance), (p1[0], p1[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cv2.putText(cam_frame, "pitch: {0:.2f}".format(pitch_degrees), (p1[0], p1[1] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(cam_frame, "yaw: {0:.2f}".format(yaw_degrees), (p1[0], p1[1] + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(cam_frame, "roll: {0:.2f}".format(roll_degrees), (p1[0], p1[1] + 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            vec = Vector2()
            vec.set_cartesian(cx, cy)

            results.append(HodorAprilTag(vec, detection.tag_id, distance))

        if self.__enable_draw:
            cv2.imshow('Camera', cam_frame)
            cv2.waitKey(1)

        if video_output is not None:
            video_output.write(cam_frame)

        return results
