import cv2
import numpy as np
import json
import codecs

from settings.HodorSettings import HodorSettings


class HodorCamera:
    def __init__(self, settings: HodorSettings):
        self.__video_id = settings.video_device_id
        self.__video_capture = cv2.VideoCapture(settings.video_device_id)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, settings.video_frame_width)
        self.__video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, settings.video_frame_height)
        self.__enable_gui = settings.video_enable_gui
        self.__calibration_success = False
        self.__camera_matrix = None
        self.__dist_coeffs = None
        self.__rvecs = None
        self.__tvecs = None
        self.__fx = 0
        self.__fy = 0
        self.__cx = 0
        self.__cy = 0

    def close(self):
        self.__video_capture.release()

    def load_calibration(self, file_path: str):
        json_calibration_data = codecs.open(file_path, 'r', encoding='utf-8').read()
        calibration_data = json.loads(json_calibration_data)

        self.__camera_matrix = np.array(calibration_data['camera_matrix'])

        self.__set_parameters_from_matrix__()
        self.__calibration_success = True

        print("[INFO] Calibración cargada exitosamente. Parámetros de cámara:")
        print("f: ({}, {})".format(self.__fx, self.__fy))
        print("c: ({}, {})".format(self.__cx, self.__cy))

    def get_parameters(self):
        if self.__calibration_success:
            return self.__fx, self.__fy, self.__cx, self.__cy

    def get_frame(self):
        if not self.__calibration_success:
            print("[ERR] La cámara debe calibrarse antes de poder ser usada")
            exit()

        ret, frame = self.__video_capture.read()

        if ret:
            return frame

        return None

    def get(self, prop):
        return self.__video_capture.get(prop)

    def __set_parameters_from_matrix__(self):
        self.__fx = self.__camera_matrix[0][0]
        self.__fy = self.__camera_matrix[1][1]
        self.__cx = self.__camera_matrix[0][2]
        self.__cy = self.__camera_matrix[1][2]
