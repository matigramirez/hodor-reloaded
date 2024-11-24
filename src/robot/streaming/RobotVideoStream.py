from robot.console.RobotLogger import RobotLogger
from robot.settings.RobotSettings import RobotSettings


class RobotVideoStream:
    def __init__(self, settings: RobotSettings):
        self.settings = settings

        if settings.video_stream_enable:
            # TODO: Inicializar socket
            return
        else:
            RobotLogger.warning("Streaming de video deshabilitado")

    def stream(self, frame):
        if not self.settings.video_stream_enable:
            return

        # TODO: Transmitir frame

    def close(self):
        # TODO: Liberar recursos
        return
