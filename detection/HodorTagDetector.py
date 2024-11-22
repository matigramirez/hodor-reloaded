from pyapriltags import Detector
import cv2
from typing import List
import numpy as np

from camera.HodorCamera import HodorCamera
from models.HodorAprilTag import HodorAprilTag


class HodorTagDetector:
    def __init__(self, camera: HodorCamera, tag_family: str, tag_size: int, tag_id: int, enable_gui: bool = False):
        self.__detector = Detector(families=tag_family)
        self.__camera = camera
        self.__fx, self.__fy, self.__cx, self.__cy = camera.get_parameters()
        self.__tag_size = tag_size
        self.__target_tag_id = tag_id
        self.__enable_draw = enable_gui

    def detect_apriltags(self) -> List[HodorAprilTag]:
        cam_frame = None

        # Tomar frame de la cámara
        while cam_frame is None:
            cam_frame = self.__camera.get_frame()

        # Convertir frame a escala de grises
        grayscale_img = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2GRAY)

        # Detectar april tags en la imagen
        detections = self.__detector.detect(grayscale_img, estimate_tag_pose=True,
                                            camera_params=(self.__fx, self.__fy, self.__cx, self.__cy),
                                            tag_size=self.__tag_size)

        results = []

        for detection in detections:
            if detection.tag_id != self.__target_tag_id:
                continue

            # Opencv usa el sistema de coordenadas  (x, -y, z) donde y es el eje de altura
            # Referencia: https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
            pos_x = detection.pose_t[0]
            pos_y = detection.pose_t[2]

            # Calcular la distancia relativa del april tag mediante la norma del vector de traslación
            distance = float(np.linalg.norm(detection.pose_t))

            # Calcular el angulo relativo entre la cámara y el april tag
            angle_rad = np.arctan2(pos_x, pos_y)
            angle_deg = np.degrees(angle_rad)[0]

            if self.__enable_draw:
                # Obtener contornos
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

                # Dibujar contornos del april tag
                cv2.circle(cam_frame, (cx, cy), 5, (0, 0, 255), -1)

                # Dibujar id, distancia y angulo al frame como texto
                cv2.putText(cam_frame, "id: {}".format(detection.tag_id), (p1[0], p1[1] - 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                cv2.putText(cam_frame, "dist: {0:.2f}".format(distance), (p1[0], p1[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cv2.putText(cam_frame, "ang: {0:.2f}°".format(angle_deg), (p1[0], p1[1] + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

            results.append(HodorAprilTag(detection.tag_id, distance, angle_deg))

            # TODO: Escribir frame para la transmisión acá
            # draw(cam_frame)

        return results
