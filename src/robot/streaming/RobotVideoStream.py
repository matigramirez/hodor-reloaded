import cv2
import socket
import struct
import threading
from collections import deque

from robot.common.CancellationToken import CancellationToken
from robot.console.RobotLogger import RobotLogger
from robot.settings.RobotSettings import RobotSettings


class RobotVideoStream:
    def __init__(self, settings: RobotSettings, cancellation_token: CancellationToken):
        self.settings = settings
        self.server_socket: socket.socket | None = None
        self.conn = None
        self.addr = None
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), settings.video_compression_level]

        self.stream_queue = deque()
        self.thread: threading.Thread | None = None
        self.cancellation_token = cancellation_token

        if settings.video_stream_enable:
            self.__start_stream_thread__()
        else:
            RobotLogger.warning("Streaming de video deshabilitado")

    def __start_stream_thread__(self):
        self.thread = threading.Thread(target=self.__start_listener__)
        self.thread.start()

    def __start_listener__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', self.settings.video_stream_port))
        self.server_socket.listen(1)
        self.__accept_connection__()

    def __accept_connection__(self):
        RobotLogger.info("Esperando conexión.")
        while True:
            try:
                if self.cancellation_token.is_cancellation_requested:
                    raise Exception("Cancelación solicitada")

                self.conn, self.addr = self.server_socket.accept()
                self.stream_queue.clear()
                RobotLogger.info(f"Conexión establecida con {self.addr}.")

                while True:
                    if self.cancellation_token.is_cancellation_requested:
                        raise Exception("Cancelación solicitada")
                    self.__internal__stream__()

            except Exception:
                # Cuando hay una excepción acá es porque el main thread cerró la conexión y esta excepción
                # hace que termine la ejecución del thread de la transmisión
                return

    def stream(self, frame):
        if not self.settings.video_stream_enable:
            return

        if self.conn is None:
            return

        self.stream_queue.append(frame)

    def __internal__stream__(self):
        if len(self.stream_queue) <= 0:
            return

        if self.conn is None:
            return

        frame = self.stream_queue.popleft()

        try:
            result, encoded_frame = cv2.imencode('.jpg', frame, self.encode_param)
            frame_bytes = encoded_frame.tobytes()
            size = len(frame_bytes)
            self.conn.sendall(struct.pack(">L", size) + frame_bytes)
        except (BrokenPipeError, ConnectionResetError):
            RobotLogger.warning("Conexión perdida con el cliente")
            self.conn.close()
            self.__accept_connection__()

    def close(self):
        if self.conn is not None:
            self.conn.close()

        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()
