from core.Hodor import Hodor
from settings.RobotSettings import RobotSettings
from console.RobotLogger import RobotLogger

RobotLogger.init("##############################################")
RobotLogger.init("####           HODOR ft. VI23            #####")
RobotLogger.init("##############################################")

settings = RobotSettings.read_from_file("settings.json")
hodor = Hodor(settings)

try:
    hodor.stop()
    hodor.setup()
    hodor.loop()
finally:
    hodor.stop()
    hodor.cleanup()
