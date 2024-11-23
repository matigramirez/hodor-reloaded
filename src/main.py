from core.Hodor import Hodor
from settings.HodorSettings import HodorSettings
from console.HodorLogger import HodorLogger

HodorLogger.init("##############################################")
HodorLogger.init("####           HODOR ft. VI23            #####")
HodorLogger.init("##############################################")

settings = HodorSettings.read_from_file("settings.json")
hodor = Hodor(settings)

try:
    hodor.stop()
    hodor.setup()
    hodor.loop()
finally:
    hodor.stop()
    hodor.cleanup()
