import cv2

from camera.HodorCamera import HodorCamera


class HodorVideoOutput:
    def __init__(self, camera: HodorCamera):
        self.camera = camera

        frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

    def write(self, frame):
        self.video_writer.write(frame)

    def close(self):
        self.video_writer.release()
