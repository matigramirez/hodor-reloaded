import json
import codecs
import cv2
import socket
import struct
import io
from PIL import Image
import numpy as np
from robot.settings.RobotSettings import RobotSettings


settings = RobotSettings.read_from_file("settings.json")

# Configuración del socket
SERVER_IP = settings.video_stream_ip
PORT = settings.video_stream_port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Buffer de datos
data = b""
payload_size = struct.calcsize(">L")

def pil_to_cv2(pil_image):
    numpy_image = np.array(pil_image)
    return cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)

try:
    while True:
        # Recibir el tamaño del frame y luego el frame
        while len(data) < payload_size:
            data += client_socket.recv(4096)
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4096)
        
        frame_data = data[:msg_size]
        data = data[msg_size:]
        
        pil_image = Image.open(io.BytesIO(frame_data))
        frame = pil_to_cv2(pil_image)
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    client_socket.close()
    cv2.destroyAllWindows()