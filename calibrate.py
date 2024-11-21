from calibration.HodorCameraCalibration import HodorCameraCalibration
from settings.HodorSettings import HodorSettings

settings = HodorSettings()
settings.read_from_file("settings.json")

camera_calibration = HodorCameraCalibration(settings)

camera_calibration.calibrate_from_scratch()

camera_calibration.save_calibration("new_calibration.json")
