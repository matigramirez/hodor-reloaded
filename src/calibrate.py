from calibration.RobotCameraCalibration import RobotCameraCalibration
from settings.RobotSettings import RobotSettings

settings = RobotSettings()
settings.read_from_file("settings.json")

camera_calibration = RobotCameraCalibration(settings)

camera_calibration.calibrate_from_scratch()

camera_calibration.save_calibration("new_calibration.json")
