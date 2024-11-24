from hodor.Hodor import Hodor
from hodor.HodorMotorControl import HodorMotorControl
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger

RobotLogger.print("##############################################")
RobotLogger.print("####           HODOR ft. VI23            #####")
RobotLogger.print("##############################################")

settings = RobotSettings.read_from_file("settings.json")
motor_control = HodorMotorControl(settings)
hodor = Hodor(settings, motor_control)

try:
    hodor.setup()
    hodor.loop()
finally:
    hodor.cleanup()
