from hodor.HodorKeyboard import HodorKeyboard
from hodor.HodorMotorControl import HodorMotorControl
from hodor.HodorSettings import HodorSettings
from robot.settings.RobotSettings import RobotSettings

robot_settings = RobotSettings.read_from_file("settings.json")
hodor_settings = HodorSettings.read_from_file("hodor.json")

motor_control = HodorMotorControl(robot_settings, hodor_settings)
hodor = HodorKeyboard(robot_settings, motor_control)

try:
    hodor.setup()
    hodor.loop()
finally:
    hodor.cleanup()
