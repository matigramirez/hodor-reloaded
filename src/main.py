from hodor.Hodor import Hodor
from hodor.HodorMotorControl import HodorMotorControl
from hodor.HodorSettings import HodorSettings
from robot.settings.RobotSettings import RobotSettings
from robot.console.RobotLogger import RobotLogger

RobotLogger.print("##############################################")
RobotLogger.print("####           HODOR ft. VI23            #####")
RobotLogger.print("##############################################")

robot_settings = RobotSettings.read_from_file("settings.json")
hodor_settings = HodorSettings.read_from_file("hodor.json")

motor_control = HodorMotorControl(robot_settings, hodor_settings)
hodor = Hodor(robot_settings, motor_control)

try:
    hodor.setup()
    hodor.loop()
finally:
    hodor.cleanup()
