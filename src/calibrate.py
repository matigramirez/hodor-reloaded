from robot.calibration.RobotCameraCalibration import RobotCameraCalibration
from robot.settings.RobotSettings import RobotSettings

settings = RobotSettings.read_from_file("settings.json")

camera_calibration = RobotCameraCalibration(settings)

camera_calibration.calibrate_from_scratch()

camera_calibration.save_calibration("new_calibration.json")
