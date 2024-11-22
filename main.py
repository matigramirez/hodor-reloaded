from Hodor import Hodor
from settings.HodorSettings import HodorSettings

hodor_settings = HodorSettings()
hodor_settings.read_from_file("settings.json")

hodor = Hodor(hodor_settings)

try:
    hodor.motor_control.stop()
    hodor.setup()
    hodor.loop()
finally:
    hodor.motor_control.stop()
    hodor.cleanup()
