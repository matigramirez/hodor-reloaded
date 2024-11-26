import cv2
import socket
import struct

from robot.console.RobotLogger import RobotLogger
from robot.settings.RobotSettings import RobotSettings


class RobotVideoStream:
    def __init__(self, settings: RobotSettings):
        self.settings = settings
        self.server_socket = None
        self.conn = None
        self.addr = None
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90] #TODO: Agregar compresión a las settings

        if settings.video_stream_enable:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', self.settings.video_stream_port))
            self.server_socket.listen(1)
            self.__accept_connection__()
            return
        else:
            RobotLogger.warning("Streaming de video deshabilitado")

    def __accept_connection__(self):
        RobotLogger.info("Esperando conexión.")
        while True:
            try:
                self.conn, self.addr = self.server_socket.accept()
                RobotLogger.info(f"Conexión establecida con {self.addr}.")
                break
            except Exception as e:
                RobotLogger.error(f"Error al aceptar conexión: {e}")        

    def stream(self, frame):
        if not self.settings.video_stream_enable:
            return

        try:
            result, encoded_frame = cv2.imencode('.jpg', frame, self.encode_param)
            frame_bytes = encoded_frame.tobytes()
            size = len(frame_bytes)
            self.conn.sendall(struct.pack(">L", size) + frame_bytes)
        except (BrokenPipeError, ConnectionResetError) as e:
            RobotLogger.error(f"Conexión perdida con el cliente: {e}")
            self.conn.close()
            self.__accept_connection__()

    def close(self):
        if self.conn is not None:
            self.conn.close()
        self.server_socket.close()
        return
